# Changelog

## 2.0.0 - em desenvolvimento

### Arquitetura

- Substitui a taxonomia plana de sete estilos por três eixos: estética, formato e função.
- Define precedência explícita entre marca, função, acessibilidade, estilo e defaults.
- Acrescenta modos `build`, `glow-up`, `audit`, `concept` e `ingest`.
- Introduz `references/design-registry.yaml` como registro canônico legível por máquina.

### Portabilidade e referências

- Remove caminhos absolutos do workflow da skill.
- Resolve o corpus por caminho do usuário, variável `DESIGN_DNA_REFERENCE_ROOT`, pasta irmã ou assets empacotados.
- Registra cobertura e vieses do corpus em `references/corpus-profile.yaml`.
- Acrescenta protocolo de ingestão com proveniência, direitos e regra anti-cópia.

### Qualidade

- Formaliza papéis de cor e exceções para status, syntax highlight, data viz e marcas multicoloridas.
- Bloqueia gradiente multicolorido em texto e melhora a disciplina de acento detectada nos benchmarks.
- Acrescenta gates de conteúdo, coerência, originalidade, responsividade, acessibilidade, comportamento e entrega.
- Acrescenta validadores locais para o pacote e para outputs web.

### Conteúdo

- Preserva os sete registros originais como quatro direções estéticas e três formatos.
- Integra a galeria de seis componentes vivos ao roteamento curto.
- Acrescenta sumário navegável a `references/secoes-premium.md`.
- Mantém as 18 referências originais e adiciona referências de orquestração da V2.

### Avaliação

- Preserva os quatro casos históricos para comparabilidade.
- Amplia a suíte com casos de regressão/generalização para Glow Up, ecommerce, marca com cores semânticas, React, motion acessível e peça social não HTML.
- Separa expectativas correlacionadas e reduz dependência de hex exato quando a intenção perceptual é o critério real.
- Registra um smoke test dirigido V1 x V2: 32/33 versus 33/33 expectativas, com paridade funcional e resultado visual misto.
