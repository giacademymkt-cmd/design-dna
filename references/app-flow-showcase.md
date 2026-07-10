# Showcase de Fluxo de App  (`app-flow-showcase`)

Formato de portfolio de UI/UX mobile: 2-3 mockups de celular lado a lado sobre fundo neutro liso ou gradiente pastel, contando uma jornada completa do app (onboarding, home/dashboard, detalhe ou checkout) numa unica imagem. O produto e o unico protagonista, sem tipografia editorial de capa e sem janela de codigo. O estilo se divide em dois polos de UI interna: light clean com acento azul unico, ou dark quase-preto com um unico acento saturado. Em ambos os polos, os aparelhos flutuam com sombra de contato suave e cada peca usa apenas um acento de cor.

**Quando usar:** Quando precisar apresentar um app mobile (saude, servico, e-commerce, reserva) mostrando a jornada de uso em uma imagem so, formato de portfolio Dribbble/Behance. Ideal para posts de produto que precisam vender o fluxo completo sem depender de video ou de codigo visivel.

## Tokens do estilo

- **Paleta assinatura (polo light):** `#E7EFFD`, `#2C6BEF`, `#FFFFFF`, `#12141A`, `#8B909A`, `#F4F6F9`
- **Paleta assinatura (polo dark):** `#111111`, `#F5C230`, `#FFFFFF`, `#EAEAEA`, `#1C1C1C`, `#8A8A8A`
- **Tipografia:** Sans-serif geometrica humanista (familia tipo SF Pro/Inter no polo light, sans bold e apertada no polo dark). Titulos curtos em peso bold, precos/numeros grandes em bold, corpo e labels em regular/medium pequeno. Hierarquia por peso mais do que por tamanho.
- **Layout:** Dois ou tres mockups de smartphone (com notch/Dynamic Island) centralizados horizontalmente e espacados igualmente sobre fundo liso ou gradiente pastel. Cada tela mostra um momento distinto da jornada: hero/onboarding, home com grid ou lista de opcoes, detalhe com informacao rica e CTA de checkout. Sombra de contato suave embaixo de cada aparelho, sem moldura pesada de device.
- **Motion:** Imagens estaticas (sem video), mas a UI sugere microinteracoes implicitas: estados ativos preenchidos em pills e badges, FAB ou seta indicando avanco de tela, elementos flutuantes sobrepostos a fotos reais. Le-se como frames de um prototipo Figma pronto para transicao de tela a tela.

## Referências visuais

Imagens originais em `/Users/williamwrage/Desenvolvimento/DESIGN CLAUDE/referencias-instagram/por-estilo/app-flow-showcase/`. Quando a fidelidade importa, leia 1-2 imagens de um post antes de desenhar.

### 01: @uiux.amina (pasta `01__uiux.amina__092370`)

Post unico mostrando tres telas de um app de agendamento odontologico (dashboard com proxima consulta, selecao de tipo de visita em grid, tela de escolha de dentista com agenda e rating) dentro de mockups de iPhone alinhados lado a lado sobre fundo azul claro degrade. UI flat, cards brancos com sombra suave e cantos bem arredondados, acento azul vibrante concentrado em botoes, badges e no card de "appointment" ativo.

- **Paleta observada:**
  - `#E7EFFD`: fundo geral em degrade pastel atras dos mockups
  - `#2C6BEF`: azul primario: card de appointment ativo, botao braces, textos de link, badge selecionado
  - `#FFFFFF`: fundo das telas do app e cards de servico
  - `#12141A`: texto primario (nomes, titulos como Appointment, Choose Your Dentist)
  - `#8B909A`: texto secundario (email, legendas, Per visit, Per session)
  - `#F4F6F9`: fundo neutro claro dos cards de servico nao destacados
- **Vale roubar:**
  - Card pill 100% arredondado em azul solido com avatar circular sobreposto a esquerda para destacar o item "ativo/proximo" (ex: proxima consulta, proximo pedido)
  - Grid 2x2 de cards de servico com icone 3D fofo, preco aproximado e badge circular de seta 45 graus no canto superior direito
  - Schedule/date picker horizontal em pills circulares com estado ativo azul preenchido, sobreposto direto sobre uma foto grande (mistura foto real e UI flutuante)
  - Badge de rating circular branco flutuante no canto de uma foto de card (ex: 4.9 estrelas)
  - Apresentacao de fluxo em 3 mockups de iPhone lado a lado sobre fundo gradiente pastel suave, ideal para mostrar jornada de app em um unico post de portfolio
  - Paleta minimalista azul, branco e preto quase puro para apps de saude/servico, transmitindo limpeza e confianca sem precisar de muitas cores

### 02: @webdesign_786 (pasta `02__webdesign_786__081321`)

Post unico mostrando tres telas de smartphone lado a lado apresentando o fluxo completo de um app de aluguel de carros (onboarding, home/dashboard, detalhe do carro com checkout). As telas tem UI escura quase preta com um unico acento amarelo saturado, flutuando com sombra suave sobre um fundo cinza claro liso. Fotos de carro recortadas em fundo branco dentro dos cards de produto.

- **Paleta observada:**
  - `#111111`: fundo das telas do app (quase preto)
  - `#F5C230`: acento unico: botoes CTA, precos, badges de desconto, icone ativo do nav
  - `#FFFFFF`: texto principal sobre fundo escuro e cards claros
  - `#EAEAEA`: fundo neutro liso atras dos mockups de celular
  - `#1C1C1C`: pilulas/inputs escuros dentro da tela clara (barra de busca)
  - `#8A8A8A`: texto secundario/legendas cinza medio
- **Vale roubar:**
  - Contar o fluxo do produto em 3 telas lado a lado numa imagem so (onboarding, home, detalhe/checkout) em vez de mostrar uma tela isolada
  - Contraste chapado preto quase-total vs. um unico amarelo saturado como acento, sem gradientes, aplicado de forma consistente a CTA/preco/badge
  - Fundo cinza claro liso e sem textura atras dos mockups, deixando o produto ser o unico heroi visual
  - Fotos de produto (carro) recortadas em fundo branco dentro dos cards, dando leitura de e-commerce premium mesmo em app escuro
  - Botao CTA em pilula preta com badge circular colorido a esquerda, texto e seta, reutilizavel como padrao de call-to-action
  - Badge octogonal de desconto sobreposto quebrando a borda do card promocional, criando ponto focal sem poluir o grid

## Vale roubar (consolidado do estilo)

- Contar a jornada completa do app (onboarding, home, detalhe/checkout) em 2-3 mockups lado a lado numa unica imagem, em vez de uma tela isolada
- Fundo liso ou gradiente pastel suave atras dos aparelhos, deixando o produto como unico heroi visual, sem ruido de fundo
- Um unico acento saturado por peca (azul no polo light, amarelo no polo dark), aplicado de forma consistente a CTA, preco e badges
- Card pill 100% arredondado com avatar ou foto sobreposta para destacar o item "ativo/proximo" da jornada
- Elementos de UI flutuando sobre fotos reais (schedule picker sobre foto de pessoa, badge de rating sobre foto de card), misturando foto e interface
- Sombra de contato suave embaixo de cada mockup, sem moldura pesada de device, para leitura de portfolio premium
