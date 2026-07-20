# Índice de referências da Design DNA v2

Use este arquivo como roteador, não como licença para carregar toda a biblioteca. A menor combinação suficiente costuma produzir decisões melhores e gastar menos contexto.

## Regra de carregamento

1. Leia uma direção estética quando houver decisão de look and feel.
2. Leia um formato quando a composição for específica, como app flow ou carrossel.
3. Leia apenas os pacotes funcionais necessários à entrega.
4. Antes de entregar produção, leia `quality-gates.md`.

Orçamento padrão:

- `concept`: 1 direção ou 1 formato, sem livros longos.
- `build`: 1 direção + até 1 formato + 1 ou 2 pacotes funcionais.
- `glow-up`: anterior + UX ou qualidade conforme o problema observado.
- LP longa e ecommerce são exceções: podem exigir um bundle maior, mas leia as seções relevantes pelos índices internos.

## Direções estéticas

| Arquivo | Papel | Use quando |
|---|---|---|
| `soft-neumorphism-light.md` | Light tátil e discreto | SaaS claro, app amigável, componente isolado, biblioteca de ícones |
| `dark-ui-lab.md` | Dark técnico e noturno | Dev-tool, automação, dashboard, demo de estado, glass localizado |
| `apple-premium.md` | Contenção extrema | Página de produto, luxo tecnológico, narrativa de capítulos |
| `editorial-minimal-mockup.md` | Editorial com cor como sinal | SaaS B2B, fintech, healthtech, case, dados e portfólio |

Escolha uma direção dominante. Não combine duas paletas completas. Se a marca já tem linguagem própria, use estes arquivos como repertório de técnica e preserve a marca.

## Formatos e composições

| Arquivo | Papel | Pode herdar |
|---|---|---|
| `app-flow-showcase.md` | Jornada em 2 ou 3 mockups de app | Qualquer direção light ou dark compatível |
| `dev-tutorial-code-showcase.md` | Demo viva + janela de código | Light, dark ou editorial |
| `dev-carousel-explainer.md` | Carrossel educativo e comparativo | Creme editorial por padrão; outra direção se a marca pedir |

As cores multivariadas de status ou syntax highlight permanecem confinadas ao bloco funcional. Elas não redefinem a paleta da peça.

## Estrutura, conversão e conteúdo

| Arquivo | Carregue quando | Observação |
|---|---|---|
| `secoes-premium.md` | Montar hero, prova, pricing, CTA, footer ou estados vazios | Use o índice; não leia todas as receitas por reflexo |
| `copywriting-conversao.md` | Headline, CTA, prova, benefício e objeção | Copy precisa vender ou orientar, não apenas preencher layout |
| `vies-cognitivo-persuasao.md` | Escassez, ancoragem, prova social e ética persuasiva | Respeite a lista de dark patterns proibidos |
| `lp-venda-longa.md` | Curso, infoproduto, oferta de alto compromisso | Leia depois de copy e persuasão; selecione a anatomia aplicável |
| `ecommerce-especialista.md` | PDP, PLP, carrinho e checkout | Priorize preço, prazo, estoque, variante e confiança |

Bundles recomendados:

- LP curta: `secoes-premium.md` + `copywriting-conversao.md`.
- LP longa: anterior + `vies-cognitivo-persuasao.md` + `lp-venda-longa.md`.
- Ecommerce: `ecommerce-especialista.md` + `ux-interface-principios.md`; acrescente copy apenas nas partes comerciais.

## Interface e componentes

| Arquivo | Carregue quando | Como economizar contexto |
|---|---|---|
| `ux-interface-principios.md` | Fluxos, formulários, navegação, estados, acessibilidade | Leia o princípio ligado ao problema observado |
| `component-gallery.md` | Escolher uma assinatura de interação | Comece aqui; é um catálogo curto |
| `componentes-premium.md` | Implementar a receita exata | Leia somente a seção apontada pela galeria ou pelo índice interno |

## Motion

| Arquivo | Papel | Ordem |
|---|---|---|
| `motion-principios.md` | Gosto, timing, performance, reduced motion | Sempre primeiro |
| `motion-scroll.md` | Reveal, parallax, pin, trilho e capítulos | Só se scroll for parte da narrativa |
| `motion-texto-cursor.md` | Entrada de texto, hover, cursor e spotlight | Só se esses efeitos forem necessários |
| `motion.md` | Receita curta legada | Use apenas como fallback quando o ambiente for muito simples |

Motion não é bundle obrigatório. Uma página contida pode ganhar qualidade com menos movimento, não mais.

## Processo e QA

| Arquivo | Use quando |
|---|---|
| `quality-gates.md` | Antes de entregar produção ou concluir Glow Up |
| `reference-ingestion.md` | O usuário fornecer nova referência ou pedir para alimentar a skill |
| `design-registry.yaml` | Precisar de uma fonte canônica legível por máquina para eixos, precedência e exceções |
| `corpus-profile.yaml` | Avaliar cobertura e vieses do corpus visual local |

## Documentos grandes

Os arquivos abaixo devem ser navegados pelo sumário, não lidos integralmente sem necessidade:

- `componentes-premium.md`
- `ecommerce-especialista.md`
- `lp-venda-longa.md`
- `motion-scroll.md`
- `motion-texto-cursor.md`
- `secoes-premium.md`

Se uma tarefa requer repetidamente a mesma subseção de um livro grande, extraia uma receita curta e atualize este índice em vez de duplicar o livro inteiro no `SKILL.md`.
