# Design DNA v2: arquitetura e decisões

## Resultado pretendido

A V2 preserva o gosto já codificado, mas transforma a skill de um catálogo de mandamentos em um sistema de decisão portátil, verificável e menos propenso a overfitting.

## Evidência de partida

A melhor rodada controlada da V1 está em `../design-dna-workspace/iteration-3`:

- 4 casos;
- 3 execuções por caso e configuração;
- 90,79% de aderência com skill;
- 56,56% sem skill;
- ganho de 34,23 pontos percentuais.

As nove falhas da configuração com skill estavam concentradas em paleta, acentos e gradientes decorativos. A iteração 1 também mostrou custo elevado: aproximadamente 1,94 vez mais tokens e 2,7 vezes mais tempo, sem dados posteriores confiáveis de eficiência.

## Problemas estruturais da V1

1. Sete registros misturavam estética e formato. Um app flow ou demo de código pode ser light, dark ou editorial.
2. O corpus externo era acessado por caminho absoluto e não existia em todos os estilos.
3. “Um acento” entrava em conflito com status, syntax highlight, data viz e marcas multicoloridas.
4. O contrato de saída era web-centric, embora o trigger cobrisse social, motion e criativos.
5. Livros de até 1.300 linhas podiam ser carregados em excesso.
6. A validação era descrita, mas não reproduzível por scripts versionados.
7. A suíte não testava Glow Up, acessibilidade, assets, outputs não HTML nem generalização em casos novos.

## Decisão central: três eixos

```text
intenção
  ├─ estética: soft-light | dark-technical | apple-contained | editorial-signal
  ├─ formato: product-flow | demo-code | explainer-carousel
  └─ função: page | long-form | ecommerce | UX | component | motion
```

Uma peça tem uma estética dominante. Formato e função acrescentam composição e comportamento sem importar uma segunda paleta inteira.

## Precedência

1. pedido, marca e assets reais;
2. função, conteúdo e conversão;
3. acessibilidade e integridade da interação;
4. estética e formato;
5. defaults globais.

Essa ordem resolve conflitos sem precisar criar exceções ad hoc em cada documento.

## Cor por papéis

A V2 separa:

- `accent`: família operacional dominante;
- `status`: erro, sucesso, alerta e info, sempre localizados;
- `syntax`: cores confinadas à representação de código;
- `data`: escala adicional apenas quando necessária para interpretação;
- `brand`: cores fornecidas pelo usuário, com uma eleita para interação.

Gradiente multicolorido em texto continua proibido por padrão porque foi a regressão mais consistente do benchmark. O critério não impede status, código ou dados legítimos.

## Progressive disclosure

O `SKILL.md` contém precedência, eixos, workflow e regras globais. `references/INDEX.md` roteia livros. Componentes começam numa galeria curta; livros grandes são abertos pela seção relevante. O modo `concept` impõe orçamento menor de leitura.

## Portabilidade

O corpus externo é opcional e resolvido por:

1. caminho informado;
2. `DESIGN_DNA_REFERENCE_ROOT`;
3. pasta irmã relativa;
4. assets e textos empacotados.

O repositório versiona perfil, proveniência e regras de uso, não os 35 MB de mídia de terceiros.

## QA versionado e parcialmente reproduzível

- `scripts/doctor.py`: integridade do pacote.
- `scripts/preflight.py`: heurísticas de output web.
- `scripts/reference_manifest.py`: cobertura e hashes do corpus externo.
- `references/quality-gates.md`: revisão humana por evidência.
- `tests/`: smoke tests dos validadores.

Scripts não substituem render nem julgamento visual. Eles tornam falhas recorrentes mais baratas de encontrar. A execução de modelo só é reproduzível quando commit, modelo, ambiente, prompts, outputs e timings forem registrados no workspace.

## Avaliação da V2

A suíte mantém os quatro casos históricos e acrescenta casos públicos de regressão/generalização. A comparação relevante é V1 snapshot versus V2, com outputs renderizados em desktop e mobile, critérios independentes e revisão qualitativa. Métricas sem timing ou sem braço de controle devem ser apresentadas como incompletas, não como delta válido.

## Compatibilidade

O nome da skill permanece `design-dna`, preservando o trigger e o caminho de instalação esperado. A pasta e a branch podem carregar o rótulo V2 sem mudar a identidade instalada.
