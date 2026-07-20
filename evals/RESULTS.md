# Resultados de avaliação

## Smoke test dirigido: V1 x V2

Data: 10 de julho de 2026
Base V1: commit `963d0ef`
V2: branch `v2/refined`
Execuções: 1 por versão em cada caso

| Caso | V1 | V2 | Leitura |
|---|---:|---:|---|
| Glow Up de dashboard legado | 8/9 | 9/9 | A V1 manteve um overline decorativo antes do H1; a V2 passou o gate. |
| Dashboard com status semântico | 8/8 | 8/8 | Paridade objetiva; a V2 é mais operacional, a V1 mais compacta. |
| Criativo social em SVG | 8/8 | 8/8 | Paridade objetiva; as versões escolheram direções visuais diferentes. |
| Storytelling com scroll acessível | 8/8 | 8/8 | Paridade objetiva; a V1 é mais rica, a V2 mais contida e narrativa. |
| **Total** | **32/33 (96,97%)** | **33/33 (100%)** | **+3,03 pontos percentuais para a V2.** |

## O que este resultado sustenta

- A V2 preservou a capacidade funcional da V1 nos quatro casos executados.
- Os novos gates são aplicáveis a HTML e SVG; os oito artefatos passaram no preflight, com um aviso não bloqueante apenas na V1.
- A V2 produz decisões mais sistemáticas, contidas e rastreáveis.

## O que este resultado não sustenta

- Não prova superioridade visual geral. A V1 foi mais expressiva em alguns renders.
- Não mede consistência entre execuções, pois houve uma execução por caso.
- Não é um teste cego: os casos foram criados junto da V2 e cobrem diretamente suas novas regras.
- Não reexecuta os quatro casos históricos nem captura tokens e duração de forma comparável.
- Não compara skill contra ausência de skill; compara a V1 original contra a V2 refinada.

Trate estes resultados como smoke test de regressão dirigido. Para uma afirmação forte, execute múltiplas amostras, casos independentes, avaliação visual cega e a suíte histórica completa.

## Precisão do trigger

Duas revisões independentes classificaram os 20 prompts públicos de `trigger-evals.json` com base apenas no frontmatter da skill. Ambas obtiveram 20/20 correspondências: 10 verdadeiros positivos, 10 verdadeiros negativos e nenhum falso positivo ou falso negativo.

O resultado mostra que a redação separa corretamente intenção visual de near-misses presentes na suíte, como debugging, iOS técnico, performance sem mudança visual, texto puro e implementação de design system fechado. Como os casos são públicos e a classificação foi feita por modelo, isso não equivale a telemetria do roteador real em produção.
