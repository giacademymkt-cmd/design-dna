---
name: design-dna
description: DNA de design pessoal do William, destilado de referências visuais curadas (rondesignlab, iconlypro, code.xr e outros). Use SEMPRE que o William pedir para criar, desenhar ou redesenhar qualquer peça visual: landing page, LP, página, seção, hero, componente, card, dashboard, mockup, peça para Instagram/social, criativo de anúncio, ou quando disser "no meu estilo", "estilo premium", "capricha no design", "estilo apple", "bem refinado". Use TAMBÉM quando ele pedir pra MELHORAR um site/página que já existe: "melhorar", "dar um glow up", "upar o design", "modernizar", "deixar premium", "auditar o visual" (modo Glow Up: diagnóstico visual com a bagagem + amostras antes/depois). Também use quando um pedido de página ou componente não especificar direção visual nenhuma, pois este é o padrão visual dele. Define estilos, paletas hex, tipografia, layout, motion e regras de qualidade.
---

# Design DNA — William

Este é o sistema visual pessoal do William, destilado da leitura de referências que ele curou. O objetivo não é imitar um post específico, é projetar QUALQUER peça nova como se tivesse saído da mesma prancheta.

## A direção (leia isto primeiro)

UI premium, tátil e didática. Interfaces limpas de SaaS/fintech/dev-tool com respiro generoso, cantos bem arredondados, UM acento de cor cirúrgico por peça e microinterações bem resolvidas. A biblioteca oscila entre dois polos coerentes: o **light minimal-neumórfico** e o **dark glass-tech**, unidos pela mesma obsessão: transformar componentes de interface em objetos desejáveis, cinematográficos e salváveis. Há ainda um terceiro registro sob demanda, o **apple-premium**: refinamento extremo, tipografia protagonista e contenção total, pra quando o William pedir "estilo apple" ou o máximo de sofisticação.

## Escolha o estilo (1 por peça)

| Peça pedida | Estilo | Referência |
|---|---|---|
| Conteúdo educativo dev/design, demo + código, Reels/carrossel de componente | `dev-tutorial-code-showcase` | `references/dev-tutorial-code-showcase.md` |
| LP de SaaS B2B / fintech / healthtech, case de produto, portfólio premium | `editorial-minimal-mockup` | `references/editorial-minimal-mockup.md` |
| SaaS / dashboard / app de produtividade (tela de produto, não marketing) | `soft-neumorphism-light` (claro) ou `dark-ui-lab` (escuro) conforme o produto | ambas |
| Mockup de app mobile, biblioteca de ícones/componentes, série light-mode | `soft-neumorphism-light` | `references/soft-neumorphism-light.md` |
| Demo de dev-tool, tutorial de ferramenta, comparativo bom vs ruim, dark premium | `dark-ui-lab` | `references/dark-ui-lab.md` |
| Página de produto high-end, LP institucional, "estilo apple", refinamento máximo | `apple-premium` | `references/apple-premium.md` |
| Showcase de app mobile: fluxo em 2-3 mockups de celular lado a lado (portfólio, post de produto) | `app-flow-showcase` | `references/app-flow-showcase.md` |
| Carrossel educativo dev/design: slides numerados, antes vs depois semântico, código anotado | `dev-carousel-explainer` | `references/dev-carousel-explainer.md` |
| Landing page de captura (troca por email/contato, isca digital, pré-lançamento) | `editorial-minimal-mockup` (confiança, sem escassez agressiva) | `references/editorial-minimal-mockup.md` |
| Página de produto de ecommerce (PDP: 1 produto, fotos, comprar) | `apple-premium` se o produto for o herói; `editorial-minimal-mockup` se for catálogo com preço/prova social mais denso | ambas |
| LP de venda longa (infoproduto, curso, oferta com prova social pesada, bônus, garantia) | Escolha o polo visual (light ou dark) pelo produto, e siga a anatomia estrutural completa | `references/lp-venda-longa.md` |

Ao escolher, **leia o arquivo de referência do estilo** antes de desenhar: ele traz paleta com papéis, tipografia, layout e as fichas dos posts originais. Se a fidelidade importa (o William pediu "igual às referências"), leia também 1-2 imagens da biblioteca em `/Users/williamwrage/Desenvolvimento/DESIGN CLAUDE/referencias-instagram/por-estilo/<estilo>/` com a ferramenta Read.

Se a peça não se encaixa em nenhuma linha da tabela, escolha o polo (light ou dark) pelo contexto do produto e aplique as regras globais abaixo. Elas são o DNA; os estilos são temperos.

## Antes de desenhar: alinhe o estilo com o William

Essa skill vai cobrir cada vez mais formato: SaaS, captura, venda, ecommerce, e o que mais aparecer. A tabela acima cobre os casos mais comuns, mas não é exaustiva, e o pior erro nesses casos novos é decidir sozinho e só aparecer com o resultado pronto no final. Regra: **narre a escolha antes de desenhar, não só depois.**

**Catálogo abstrato não funciona pra isso.** Já tentamos montar uma galeria de referência com swatches/vinhetas pequenas fora de contexto e o William rejeitou: ninguém decide direção de site olhando card de exemplo genérico. O que decide é ver a HERO REAL do projeto dele, com o nome e a copy verdadeira, em tamanho de verdade. Regra de ouro: **espera a ideia concreta chegar primeiro, só depois construa opções, e construa sempre com o conteúdo real do projeto, nunca com placeholder genérico.**

1. **Quando o estilo é óbvio** (bate 1 linha só da tabela, sem ambiguidade), diga o estilo/espécime escolhido e o porquê em 1-2 frases antes de escrever HTML, e siga direto pra peça completa. Ex: "Isso é uma LP de captura, vou de `editorial-minimal-mockup` porque pede confiança sem escassez agressiva."
2. **Quando há ambiguidade real** (2+ estilos servem igual bem, a peça é de um formato novo/caro de refazer, ou o William pede pra ver opções), NÃO desenhe a peça inteira de primeira: construa **2 a 3 HEROES completos e reais** do projeto dele — mesmo nome de produto, mesma copy, mesmo objetivo — um em cada estilo/espécime candidato, empilhados numa página só (ou 2-3 arquivos separados) pra comparação lado a lado. Cada hero é a seção inteira (headline, CTA, palco do produto, motion), não um card de exemplo abstrato. Aí sim ele escolhe olhando pra o produto dele de verdade, e você continua construindo o resto da página só no estilo escolhido. Os arquivos `references/<estilo>.md` (paleta, tipografia, layout, vale roubar por post) são pra VOCÊ ler antes de construir cada hero, não pra mostrar ao William.
3. **Para formatos que fogem da estética original** (checkout tradicional, ou qualquer coisa fora do que a biblioteca de receitas já cobre), avise antes de desenhar: esse DNA foi destilado de referência de SaaS/dev-tool/produto premium. LP de venda longa JÁ TEM anatomia própria em `references/lp-venda-longa.md`, não é mais um formato sem cobertura, mas ainda vale narrar que a régua de contenção visual do design-dna vai ser aplicada em cima da anatomia clássica de venda, não substituída por estética genérica de infoproduto.
4. **Depois de entregar, convide o próximo passo.** Não encerre com só "pronto, tá aqui": diga o que testaria a seguir (outro estilo, outro acento, outra estrutura de prova social) e pergunte o que ele achou. É assim que a skill aprende o gosto dele peça a peça.
5. **Exceção:** pedido pequeno e óbvio dentro de um estilo já em uso ("troca a cor desse botão", "ajusta esse padding") não precisa desse ritual inteiro, só a entrega normal.

## Glow Up: melhorar sites que já existem

A skill não serve só pra criar do zero: ela é o diretor de arte pra elevar página existente com a bagagem instalada. Gatilhos: "melhorar", "dar um glow up", "upar o design", "modernizar", "deixar premium", "auditar o visual". O foco é direção de arte, NÃO auditoria de desempenho/SEO: não traga Lighthouse, minificação ou tempo de carregamento a menos que o William peça.

1. **Veja o site de verdade antes de opinar.** Página ao vivo: navegue com as ferramentas de browser e capture screenshots das seções (desktop e mobile). Código local: leia os arquivos E abra a página renderizada. Nunca diagnostique de memória nem só pelo HTML.
2. **Diagnóstico com a bagagem, seção por seção, com três lentes:**
   - **Anti-slop e regras globais:** o que na página denuncia template/genérico (badge acima de headline, grid de fundo, 3 cards clones, acentos competindo, copy inflada, hero sem palco, densidade sem respiro).
   - **Oportunidades da biblioteca:** pra cada seção, qual receita elevaria o nível, citada PELO NOME (CTA morto vira Botão Assinatura; hero estático ganha Cortina de Texto; logos parados viram Marquee; número importante ganha Count-up; features clonadas viram bento com protagonista; footer bagunçado vira Grade Densa e Silenciosa; card importante ganha Spotlight). Leia os livros de receitas relevantes antes de sugerir.
   - **Estrutura:** compare as seções com `secoes-premium.md`. Se for página de venda/ecommerce, os livros de conversão são obrigatórios aqui também: mecânica de conversão vence estética no glow up igual.
3. **Relatório de glow up priorizado.** Lista do maior pro menor impacto visual, cada item com: o que muda, qual receita/princípio aplica, e o porquê em 1 frase. Direção de arte concreta, sem jargão.
4. **Mostre, não descreva.** A entrega que o William espera é VISUAL: reconstrua a(s) seção(ões) de maior impacto com o conteúdo REAL da página (headline verdadeira, produto verdadeiro, marca verdadeira) e apresente antes vs depois lado a lado ou empilhado com rótulos, funcionando (motion incluso). O glow up da página inteira só depois que ele aprovar a direção na amostra.
5. **Identidade da marca é sagrada.** Glow up não é trocar a marca pelo DNA: as cores da marca viram o acento único, a tipografia se adapta à hierarquia premium, o conteúdo permanece. O DNA entra como régua de execução (contenção, respiro, motion, anti-slop), não como uniforme.
6. **Página ao vivo é intocável sem aprovação.** Melhoria em página que já está rodando e gerando resultado NUNCA sobe direto: amostra local primeiro, deploy só com ok explícito do William.

## Regras globais (valem em todos os estilos)

1. **Herói flutuante.** O objeto principal (componente, card, mockup) flutua isolado num "palco" arejado, com sombra difusa, sobre fundo neutro. Nunca cole o herói na borda nem o afogue em decoração: ele é o produto.
2. **Hierarquia por cor e peso, não por tamanho.** Título com uma palavra no acento (magenta, coral, azul, lime) contra o resto quase-preto ou quase-branco. Isso cria ênfase sem inflar a tipografia.
3. **Um acento por peça.** Escolha UM acento vibrante da paleta do estilo e use com disciplina: CTA, dado em destaque, palavra-chave. Acento é sinal, não decoração. Dois acentos competindo = peça reprovada. **Isso vale para gradientes de texto também**: um `background-clip:text` com 2-3 cores diferentes (tipo azul→roxo→rosa) conta como vários acentos, não um. Pra destacar uma palavra do headline, use o acento único em bloco sólido atrás do texto, nunca gradiente multi-cor.
4. **Base neutra.** Light: off-white `#ECECEE`/`#EDECEA`/`#F4F4F2` com branco puro nos cards. Dark: quase-preto `#111111`/`#0A0C0F` com superfícies elevadas sutis `#161A1F`. Nunca cinza médio como fundo.
5. **Cantos super-arredondados (squircle/pill)** e sombras suaves ou glass translúcido. A sensação é tátil: dá vontade de apertar.
6. **Microinteração é conteúdo.** Botões e cards têm estados: idle → hover → loading/progresso → sucesso com checkmark. Se a peça tem CTA, o CTA tem comportamento. A peça-assinatura é o "Botão Assinatura" (morph de estados + checkmark que se desenha) em `references/componentes-premium.md`; springs base em `references/motion.md`.
7. **Respiro generoso.** Densidade baixa, whitespace é material de construção. Na dúvida, tire elementos em vez de encolher.
8. **Nunca use travessão (—)** em nenhum texto de copy, título ou legenda. Regra permanente do William. Use vírgula, dois-pontos ou reescreva.
9. **Peça autocontida.** Sem CDN de imagem externa: construa visual com CSS, SVG inline e gradientes. Fontes via system stack ou Google Fonts (única exceção de rede permitida).

## Biblioteca de receitas (leia sob demanda, conforme a peça)

Além dos estilos, a skill tem livros de receitas verificadas, destiladas das melhores fontes do mundo: motion e visual de Emil Kowalski, Rauno Freiberg, Josh Comeau, Olivier Larose, Codrops, Cassie Evans, e dissecação ao vivo de Linear/Vercel/Stripe/Raycast/Apple; e, pra tudo que é conversão/venda de verdade (copy, persuasão, ecommerce, usabilidade), Ogilvy, Cialdini, Kahneman, Baymard Institute e Nielsen Norman Group. Todo código já foi revisado por verificador. Leia o que a peça pedir:

| Situação | Arquivo |
|---|---|
| ANTES de animar qualquer coisa: regras de gosto (easing, duração, contenção, acessibilidade) | `references/motion-principios.md` |
| Peça com narrativa de scroll: reveals, parallax, pin, trilho horizontal, capítulos | `references/motion-scroll.md` |
| Headline com entrada animada, palavra de destaque, hover de card/botão, spotlight | `references/motion-texto-cursor.md` |
| CTA com estados, formulário, números/contadores, toasts, loading, listas, bento | `references/componentes-premium.md` |
| Montar a estrutura de uma LP/página: hero, prova social, pricing, footer, empty state | `references/secoes-premium.md` |
| Receita base de springs e microinteração (legado curto) | `references/motion.md` |
| Headline, descrição de produto, CTA, prova social ou qualquer copy que precisa vender, não só parecer bonita | `references/copywriting-conversao.md` |
| Gatilho de escassez/urgência, prova social, ancoragem de preço, ou qualquer mecânica de persuasão — inclui a lista de dark patterns proibidos | `references/vies-cognitivo-persuasao.md` |
| Página de produto (PDP), carrinho, checkout, categoria (PLP) de qualquer ecommerce | `references/ecommerce-especialista.md` |
| Qualquer peça com decisão real do usuário (não só visual): navegação, formulário, catálogo, acessibilidade, mobile-first | `references/ux-interface-principios.md` |
| LP de venda longa: infoproduto, curso, oferta de alto compromisso, com stack de oferta, bônus, garantia e FAQ | `references/lp-venda-longa.md` |

**Regra que não se negocia pra peça de venda/ecommerce:** os 5 últimos livros acima são leitura OBRIGATÓRIA antes de desenhar qualquer PDP, carrinho, checkout, categoria, LP de venda ou LP de venda longa, não é opcional como o resto da biblioteca. Essa regra existe porque já aconteceu de errar: duas heroes visualmente perfeitas (paleta certa, tipografia certa, motion certo) foram rejeitadas por não terem nenhuma mecânica de venda, nenhum selo de confiança, nenhuma copy de benefício, nenhum seletor de variante, só "clima" bonito. **Mecânica de conversão vence estética.** Se o estilo visual escolhido pedir uma coisa e a pesquisa de conversão pedir outra, a conversão ganha, só que desenhada com a mesma disciplina visual do resto do sistema (nunca virando badge colorido genérico ou poluição visual).

Regra de dose: as receitas marcadas como pontuais (scramble, jitter) entram no máximo 1 vez por página. Receita nunca dispensa os princípios: `motion-principios.md` governa tudo.

## Anti-slop: o que denuncia "cara de IA" (proibido por padrão)

O William rejeita explicitamente o uniforme de página genérica de IA. Estes padrões reprovam a peça mesmo que todo o resto esteja certo:

1. **Badge/chip/pill decorativo acima do headline** ("Novo", "AI-powered", "v2.0"). No lugar: entre direto no headline. Se houver informação real de contexto, use um overline discreto em caps pequenas, sem caixa, sem borda, sem fundo.
2. **Grid quadriculado ou dot-grid cobrindo o fundo.** É o papel de parede padrão de IA, mesmo que algumas referências originais usem grid técnico. No lugar: fundo liso com vinheta sutil, UM gradiente direcional de luz, ou noise fino a 2-3% de opacidade. Grid só se o William pedir, e ainda assim localizado num card ou palco, nunca na página inteira.
3. **Gradiente roxo-azul e orbs/blobs de glow** espalhados pelos cantos. No lugar: o acento único do estilo aplicado em elementos concretos, não em névoa decorativa.
4. **Emoji como ícone de feature.** No lugar: ícones SVG inline com stroke consistente.
5. **Três cards idênticos icon-título-texto** como seção de features automática. No lugar: bento com pesos variados, um card protagonista, ou uma demo real do produto por feature.
6. **Copy inflada** ("Potencialize", "Desbloqueie o poder", "Revolucione", "Eleve seu negócio"). No lugar: frases curtas e concretas sobre o que o produto faz de verdade.
7. **Glass genérico repetido**: card translúcido com borda branca a 10% aplicado em tudo. Glass é material de destaque de UM elemento, não papel de parede.
8. **Hero centralizado com dois botões (primário + ghost) por reflexo.** Segundo botão só se existir segunda ação real.

## Formato de saída

- **Padrão: HTML único e completo** (CSS e JS embutidos), responsivo, pronto pra subir na infra do William (deploy estático GI). Motion em CSS/IntersectionObserver.
- **Se o projeto já é React/Next:** componentes com Tailwind + Framer Motion, seguindo `references/motion.md`.
- **Peça social (post/carrossel/Reel):** HTML na proporção certa (4:5, 1:1 ou 9:16) com um frame por "slide", pra ser capturado como imagem.

## Checklist antes de entregar

Percorra rápido; qualquer "não" volta pra prancheta:

- [ ] Um único acento vibrante? (conte os acentos, sério)
- [ ] Herói flutuando com sombra difusa num palco limpo?
- [ ] Ênfase do título feita por cor/peso, não por tamanho gigante?
- [ ] Cantos arredondados consistentes e generosos?
- [ ] CTA com estados de interação funcionando?
- [ ] Zero travessão em qualquer texto?
- [ ] Zero badge/pill acima do headline?
- [ ] Fundo sem grid genérico, sem orbs de gradiente?
- [ ] Copy concreta, sem palavras de hype?
- [ ] Responsivo (mobile primeiro nas LPs)?
- [ ] Parece um objeto desejável que alguém salvaria?
