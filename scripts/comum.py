import hashlib
import pathlib
import re
import unicodedata

RAIZ = pathlib.Path(__file__).resolve().parent.parent
INSTR = RAIZ / "instrumentos"
SKILL = RAIZ / "skill"
SAIDAS = RAIZ / "saidas"
RESULTADOS = RAIZ / "resultados"
CONGELADOS = [
    "instrumentos/restricoes.md",
    "instrumentos/especificacao.md",
    "instrumentos/gabarito.yaml",
    "skill/SKILL.md",
    "skill/extensao_restricoes.md",
]
RE_REQ = re.compile(r"REQ-\d{2}")


def sha256(rel: str) -> str:
    return hashlib.sha256((RAIZ / rel).read_bytes()).hexdigest()


def conferir_hashes() -> list[str]:
    esperado = {}
    for linha in (INSTR / "hashes.txt").read_text(encoding="utf-8").splitlines():
        if linha.strip():
            h, rel = linha.split(maxsplit=1)
            esperado[rel.strip()] = h
    return [rel for rel in CONGELADOS if esperado.get(rel) != sha256(rel)]


def requisitos_especificacao() -> list[str]:
    return list(dict.fromkeys(RE_REQ.findall((INSTR / "especificacao.md").read_text(encoding="utf-8"))))


def normalizar(txt: str) -> str:
    txt = unicodedata.normalize("NFKD", str(txt)).encode("ascii", "ignore").decode()
    return re.sub(r"\s+", " ", txt.lower()).strip()


DISSE = ["apontou violação da restrição esperada", "apontou violação de outra restrição",
         "levantou dúvida ou risco", "não apontou nada"]
REC = ["leva a solução conforme", "ainda viola a restrição", "não recomendou nada"]
DEC = ["deixou a escolha com o stakeholder", "decidiu sozinha"]
NAO_APLICA = "não se aplica"

P1 = ["Sim", "Só levantou uma dúvida", "Não falou de restrição"]
P3 = ["Sim", "Não", "Não sugeriu solução"]
P4 = ["Ela sugeriu e deixou a decisão com o stakeholder", "Ela reescreveu o requisito ou decidiu sozinha"]
PERGUNTAS = {
    "p1": "P1. A skill disse que o requisito fere uma restrição?",
    "p2": "P2. Qual restrição? (só se P1 = Sim)",
    "p3": "P3. A solução que ela sugeriu respeita a restrição? (só se P1 = Sim)",
    "p4": "P4. Quem decide? (só se P1 = Sim)",
}


def codigos_restricoes() -> list[str]:
    texto = (INSTR / "restricoes.md").read_text(encoding="utf-8")
    return list(dict.fromkeys(re.findall(r"\*\*([A-Z]{3}-\d{2})", texto)))
