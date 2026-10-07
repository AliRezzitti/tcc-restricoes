"""Executa a skill DeFOSPAM original (O) e com a extensao de restricoes (E) via API."""
import argparse
import datetime
import json
import sys

from openai import OpenAI

from comum import INSTR, SAIDAS, SKILL, conferir_hashes, requisitos_especificacao

PROMPT = """Run a full DeFOSPAM analysis of the requirements below in Automated Pipeline Mode: \
output ONLY the openrequirements-results.json content as a single JSON object, with no chat \
formatting, no .md file and no .html file. Write the findings in Portuguese. Every finding must \
list, in a field "requirements", the identifiers (REQ-xx) of the requirements it refers to.

The organization has the following mandatory rules and policies (organizational constraints), \
which every solution must follow:

{restricoes}

Requirements:

{especificacao}
"""

REPEDIDO = """Your JSON is incomplete: {problema}. The extension requires a top-level array \
"constraint_check" with exactly one entry per requirement ({reqs}). Output the complete \
openrequirements-results.json again, as a single JSON object, keeping your analysis and fixing only this."""


def faltando_no_check(texto: str, reqs: list[str]) -> str:
    try:
        dados = json.loads(texto)
    except json.JSONDecodeError:
        return "the response is not valid JSON"
    check = dados.get("constraint_check") if isinstance(dados, dict) else None
    if not isinstance(check, list):
        return "the array constraint_check is missing"
    presentes = {str(e.get("requirement", "")).strip() for e in check if isinstance(e, dict)}
    faltam = [r for r in reqs if r not in presentes]
    return f"constraint_check is missing {', '.join(faltam)}" if faltam else ""


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repeticoes", type=int, default=3)
    ap.add_argument("--modelo", default="gpt-4o")
    ap.add_argument("--max-tokens", type=int, default=16000)
    ap.add_argument("--condicoes", default="O,E", help="O e/ou E, separadas por virgula")
    args = ap.parse_args()
    condicoes = [c.strip().upper() for c in args.condicoes.split(",") if c.strip()]
    if not set(condicoes) <= {"O", "E"}:
        sys.exit("condicoes validas: O, E")

    divergentes = conferir_hashes()
    if divergentes:
        sys.exit(f"hash diferente do congelado: {divergentes}. Nao rode; avise a pesquisadora.")

    skill = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    sistema = {
        "O": skill,
        "E": skill + "\n" + (SKILL / "extensao_restricoes.md").read_text(encoding="utf-8"),
    }
    usuario = PROMPT.format(
        restricoes=(INSTR / "restricoes.md").read_text(encoding="utf-8"),
        especificacao=(INSTR / "especificacao.md").read_text(encoding="utf-8"),
    )
    reqs = requisitos_especificacao()
    cliente = OpenAI()
    SAIDAS.mkdir(exist_ok=True)
    registro = SAIDAS / "registro_execucoes.jsonl"

    def chamar(msgs: list[dict]):
        return cliente.chat.completions.create(
            model=args.modelo,
            messages=msgs,
            response_format={"type": "json_object"},
            max_tokens=args.max_tokens,
        )

    for rep in range(1, args.repeticoes + 1):
        for cond in condicoes:
            arq = SAIDAS / f"{cond}_r{rep}.json"
            if arq.exists():
                print(f"{arq.name} ja existe, pulando")
                continue
            msgs = [{"role": "system", "content": sistema[cond]}, {"role": "user", "content": usuario}]
            resp = chamar(msgs)
            texto = resp.choices[0].message.content or ""
            tokens_e, tokens_s = resp.usage.prompt_tokens, resp.usage.completion_tokens
            problema = faltando_no_check(texto, reqs) if cond == "E" else ""
            if problema:
                (SAIDAS / f"{cond}_r{rep}_tentativa1.json").write_text(texto, encoding="utf-8")
                msgs += [{"role": "assistant", "content": texto},
                         {"role": "user", "content": REPEDIDO.format(problema=problema, reqs=", ".join(reqs))}]
                resp = chamar(msgs)
                texto = resp.choices[0].message.content or ""
                tokens_e += resp.usage.prompt_tokens
                tokens_s += resp.usage.completion_tokens
            arq.write_text(texto, encoding="utf-8")
            try:
                json.loads(texto)
                valido = True
            except json.JSONDecodeError:
                valido = False
            ainda = faltando_no_check(texto, reqs) if cond == "E" else ""
            with registro.open("a", encoding="utf-8") as f:
                f.write(json.dumps({
                    "arquivo": arq.name,
                    "condicao": cond,
                    "repeticao": rep,
                    "quando": datetime.datetime.now().isoformat(timespec="seconds"),
                    "modelo": args.modelo,
                    "modelo_resposta": resp.model,
                    "fingerprint": resp.system_fingerprint,
                    "finish_reason": resp.choices[0].finish_reason,
                    "tokens_entrada": tokens_e,
                    "tokens_saida": tokens_s,
                    "json_valido": valido,
                    "repedido": bool(problema),
                    "motivo_repedido": problema,
                    "incompleto_apos_repedido": ainda,
                }, ensure_ascii=False) + "\n")
            extra = f", repedido ({problema})" if problema else ""
            print(f"{arq.name}: {resp.choices[0].finish_reason}, json_valido={valido}, {tokens_s} tokens de saida{extra}")
    print(f"Concluido. Registro em {registro}")


if __name__ == "__main__":
    main()
