# Carrossel Educativo Dev/Design  (`dev-carousel-explainer`)

Formato de carrossel educativo quadrado para dev/design: slides numerados com badge azul de progresso no canto, comparacoes antes vs depois com pills semanticas vermelho/verde, janela de codigo estilo macOS com anotacoes conectadas por linha tracejada, e um speech bubble de insight fechando cada slide. Fundo creme quente unificado do primeiro ao ultimo slide, funcionando como respiro visual consistente para conteudo tecnico.

**Quando usar:** Quando precisar explicar um conceito de UX/dev em passos (problema, causa, solucao, codigo, beneficios) num carrossel quadrado de Instagram, sem depender de video. Ideal para conteudo didatico que precisa provar a solucao com um trecho de codigo real e reforcar o antes/depois de forma visual.

## Tokens do estilo

- **Paleta assinatura:** `#F7F1E6`, `#131313`, `#7C7C7C`, `#2B57D6`, `#DD4438`, `#3AA655`, `#F0A020`, `#8355D6`, `#10203C`, `#1B1B1B`
- **Tipografia:** Headline em sans-serif bold/black arredondada e pesada (estilo Poppins ExtraBold ou geometrico similar) so nos titulos grandes de cada slide; subtitulos em sans-serif regular mais leve e cinza; codigo em fonte monoespacada (estilo JetBrains Mono/Fira Code) com syntax highlight azul para valores/keywords e verde para comentarios; rodape em sans-serif regular pequeno.
- **Layout:** Coluna unica centralizada por slide sobre fundo creme uniforme. Badge numerico azul quadrado-arredondado fixo no canto superior esquerdo funcionando como indicador de progresso do carrossel. Cards brancos com cantos arredondados e sombra suave flutuando sobre o fundo para mockups e janela de codigo. Comparacoes lado a lado com rotulos em pill acima de cada elemento (vermelho vs verde). Grid de 3-4 colunas para icones de beneficio no slide final. Rodape fixo com speech bubble de insight seguido do @handle.
- **Motion:** Carrossel estatico (sem video), mas o design sugere movimento por meio de setas de fluxo horizontais conectando estados, seta tracejada vertical indicando um elemento "subindo" sobre outro, e linhas tracejadas conectando anotacoes a trechos especificos do codigo.

## Referências visuais

Corpus externo: resolva `dev-carousel-explainer/` pela variável `DESIGN_DNA_REFERENCE_ROOT` ou pela pasta irmã documentada em `reference-ingestion.md`. Quando a fidelidade importar, inspecione 1 ou 2 itens antes de desenhar.

### 01: @flutter.developer.dart (pasta `01__flutter.developer.dart__188192`)

Carrossel educativo de 5 slides sobre UX de teclado em formularios de checkout Flutter: apresenta o problema (botao escondido pelo teclado), a causa, a solucao visual (antes/depois), o trecho de codigo real (Scaffold com resizeToAvoidBottomInset) e os beneficios finais. Combina mockups simplificados de tela, janela de codigo estilo macOS com anotacoes, icones circulares coloridos e comparacoes vermelho/verde antes/depois. Fundo creme uniforme em todos os slides, com badge numerico azul indicando a posicao no carrossel.

- **Paleta observada:**
  - `#F7F1E6`: fundo creme quente base de todos os slides
  - `#131313`: preto para headlines bold e outlines de mockup
  - `#7C7C7C`: cinza medio para subtitulos e texto secundario
  - `#2B57D6`: azul para badges numerados do carrossel e destaques
  - `#DD4438`: vermelho semantico para estados de erro/problema (X, teclado, botao escondido)
  - `#3AA655`: verde semantico para estados de sucesso/solucao (check, botao visivel)
  - `#F0A020`: laranja de icone circular (Production Ready)
  - `#8355D6`: roxo de icone circular (Higher Completion)
  - `#10203C`: azul marinho escuro da barra CTA final
  - `#1B1B1B`: fundo escuro da janela de codigo
- **Vale roubar:**
  - Badge numerico azul quadrado-arredondado no canto superior esquerdo como indicador de progresso do carrossel, mais elegante que bolinhas
  - Comparacao lado a lado com rotulos em pill semanticos (vermelho/verde) acima de cada mockup para contraste antes/depois
  - Speech bubble como elemento de fechamento/insight ao final de cada slide, sempre logo acima do rodape com @handle
  - Uso consistente de vermelho/verde semantico em icones circulares, bordas e texto para sinalizar erro vs solucao ao longo de todo o carrossel
  - Janela de codigo estilo macOS com anotacoes conectadas por linha tracejada apontando para trechos especificos, deixando o codigo didatico mesmo para quem nao programa
  - Fundo creme quente (nunca branco puro) como respiro visual consistente que unifica um carrossel de conteudo tecnico

## Vale roubar (consolidado do estilo)

- Badge numerico azul quadrado-arredondado no canto superior esquerdo como indicador de progresso, substituindo bolinhas de carrossel genericas
- Fundo creme quente unico do primeiro ao ultimo slide, criando identidade de serie sem depender de logo/moldura fixa
- Comparacao antes/depois com pills semanticas vermelho/verde acima de cada mockup, deixando o problema e a solucao legiveis de relance
- Janela de codigo estilo macOS com anotacoes em linha tracejada apontando trechos especificos, tornando o codigo didatico mesmo pra quem nao le codigo
- Speech bubble de insight fechando cada slide, logo acima do rodape com @handle, reforcando a licao do slide
- Icones circulares coloridos (um por beneficio) no slide final, cada um com uma cor semantica propria, para resumir resultados sem texto longo
