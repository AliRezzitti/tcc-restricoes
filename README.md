# Validação de requisitos assistida por IA: o método DeFOSPAM aplicado a restrições organizacionais

Material de replicação do Trabalho de Conclusão de Curso de Aline Rezzitti (MBA em Engenharia de Software, USP/Esalq, 2026).
O estudo aplica a skill DeFOSPAM (OpenRequirements.AI) à validação de requisitos contra restrições organizacionais
e compara a skill original com a skill acrescida de uma extensão textual, no caso fictício de um portal de cadastro
de fornecedores da Empresa Alfa.

## Conteúdo

| Pasta/arquivo | O que é |
|---|---|
| `skill/SKILL.md` | Skill DeFOSPAM original, sem alterações (OpenRequirements.AI, licença MIT, commit 40ab291). Créditos em `skill/ORIGEM.txt` e `skill/LICENSE_OpenRequirementsAI.txt`. |
| `skill/extensao_restricoes.md` | Extensão de restrições organizacionais avaliada no estudo (versão única, congelada antes da avaliação). |
| `instrumentos/restricoes.md` | As 8 restrições organizacionais da Empresa Alfa (ARQ-01 a ARQ-03, CUS-01 a CUS-03, SEG-01, DAD-01). |
| `instrumentos/especificacao.md` | Especificação com os 13 requisitos do portal. |
| `instrumentos/gabarito.yaml` | Gabarito definido antes das execuções: 6 violações, 4 armadilhas e 3 conformes. |
| `instrumentos/hashes.txt` | Resumos SHA-256 dos arquivos congelados, conferidos pelo script antes de cada execução. |
| `scripts/executar.py` | Executa as duas condições pela API da OpenAI. |
| `scripts/avaliar.py` | Gera a planilha de julgamento com códigos sorteados (E1 a E6). |
| `scripts/metricas.py` | Cruza o julgamento com o gabarito e calcula as medidas. |
| `saidas/` | Respostas reais do modelo (gpt-4o-2024-08-06, 6 de outubro de 2026) e registro das chamadas. `*_tentativa1.json` são as respostas anteriores ao novo pedido da condição E. |
| `resultados/julgamento.xlsx` | Julgamento final usado no TCC. |
| `resultados/julgamento_antes_da_revisao.xlsx` | Julgamento antes da revisão de consistência (9 linhas corrigidas; o motivo de cada uma está na coluna de observação da versão final). |
| `resultados/chave.csv` | Correspondência entre os códigos sorteados e as condições. |
| `resultados/*.csv` | Medidas por condição, por requisito e de formato. |

## Condições

- **O:** instrução de sistema com a skill original.
- **E:** instrução de sistema com a skill original seguida da extensão.
- Nas duas, a mensagem do usuário é idêntica e contém as restrições e a especificação.
- Três execuções por condição. Na condição E, se a lista `constraint_check` vier ausente ou incompleta, o script faz um único novo pedido e guarda a primeira resposta.

## Como replicar

Requisitos: Python 3.10 ou superior e uma chave da API da OpenAI.

```
pip install openai pyyaml openpyxl
export OPENAI_API_KEY=sua-chave          # no Windows (cmd): set OPENAI_API_KEY=sua-chave
python scripts/executar.py --repeticoes 3 --modelo gpt-4o
python scripts/avaliar.py
```

Para uma nova rodada, apague antes as pastas `saidas/` e `resultados/` (ou use uma cópia limpa do repositório):
o `executar.py` pula as execuções que já existem, e o `avaliar.py` sobrescreve a planilha.

Abra `resultados/julgamento.xlsx`, leia a aba "Como preencher" e responda, em cada linha, às perguntas P1 a P4
(sem abrir `resultados/chave.csv` antes de terminar). Depois:

```
python scripts/metricas.py
```

Para apenas recalcular as medidas do estudo a partir do julgamento publicado, rode somente `python scripts/metricas.py`.

## Reutilização com outras restrições

A extensão não contém nenhuma restrição. Para aplicá-la a outra organização, substitua `instrumentos/restricoes.md`
e `instrumentos/especificacao.md` (e, para avaliar, `instrumentos/gabarito.yaml`) e atualize os resumos SHA-256 em `instrumentos/hashes.txt` (por exemplo, com `sha256sum`).
