# Neumorfismo Soft Light-UI (`soft-neumorphism-light`)

Sistema serializado do iconlypro: carrosseis claros de showcase de UI e icones em neumorfismo suave. Cards e barras brancas parecendo flutuar sobre fundo cinza off-white via sombra dupla difusa, com um unico acento colorido por slide (azul, verde, coral, violeta) contra base monocromatica. Componentes de navegacao/mockup ficam dentro de um 'palco' (container tracejado ou card flutuante isolado). Moldura de marca consistente em todos os slides da identidade de serie.

**Quando usar:** Quando precisar apresentar mockups de app mobile (settings, navegacao, perfil), bibliotecas de icones/componentes ou produtos SaaS em light mode tatil e premium-discreto. Ideal para conteudo serializado (Part 1/2/3) com header/footer fixos e um acento colorido por peca.

## Tokens do estilo

- **Paleta assinatura:** `#ECECEE`, `#FFFFFF`, `#0A0A0A`, `#2C5FF6`, `#34C759`, `#22C68B`, `#F0574F`, `#FBEBD9`, `#E3E1F5`
- **Tipografia:** Sans-serif geometrica arredondada tipo Poppins/Circular/Gordita. Titulos display bold/extrabold quase preto com tracking apertado, subtitulos regular cinza medio, labels de UI em semibold pequeno. Hierarquia por peso e cor mais que por tamanho; cantos e terminais arredondados combinando com o soft-UI.
- **Layout:** Retrato 4:5 ou quadrado, muito respiro. Moldura fixa: logo no topo-esquerda, tag 'Icon Set' no topo-direita, rodape com dominio a esquerda e 'Swipe for More >' a direita. Heroi central unico (card flutuante ou mockup) sobre fundo neutro, tudo centralizado, densidade baixa. Capa quebra o padrao com pill numerada e numero gigante em marca d'agua. Tres tecnicas adicionais recorrentes: grid de comparacao outline/filled do mesmo icone lado a lado sobre fundo liso (sem gradiente) para vender variacao de estilo; variante de gradiente sutil pessego-lavanda atras do card de mockup como alternativa 'quente' ao neumorphism cinza puro; e crop macro isolando um unico componente de UI (ex: uma nav bar) com espaco negativo generoso acima, otimo para destacar microdetalhe em carrossel.

## Referências visuais

Corpus externo: resolva `soft-neumorphism-light/` pela variável `DESIGN_DNA_REFERENCE_ROOT` ou pela pasta irmã documentada em `reference-ingestion.md`. Quando a fidelidade importar, inspecione 1 ou 2 itens antes de desenhar.

### 01: @iconlypro (pasta `01__iconlypro__186787`)
Carrossel educacional Part 3 com 10 ideias de navegacao mobile (bottom nav / floating action bars) para diferentes tipos de app: crypto, messenger, cloud storage, coffee machine, task, financial, VPN, news, football, social. Capa com titulo grande e slide final de branding do produto Iconly (biblioteca de 40.000+ icones).

- **Paleta observada:** `#EDEDED` fundo principal cinza claro; `#FFFFFF` superficie das barras de navegacao / cards flutuantes; `#0A0A0A` texto de titulo e item ativo (quase preto); `#9A9AA0` texto secundario, labels inativas e icones em cinza; `#2F6BFF` azul de acento (logo, botao +, item ativo); `#7C4DFF` gradiente violeta do botao de swap crypto; `#22C68B` verde do FAB messenger / navigation; `#F0574F` vermelho coral do FAB news reader
- **Tipografia:** Sans-serif geometrica arredondada (estilo Poppins/Gordita), titulos em peso bold/extrabold quase preto com forte contraste de tamanho; subtitulos em peso regular cinza medio. Hierarquia clara em 3 niveis: badge numerico pill, titulo grande, subtitulo descritivo de 2 linhas. Labels de UI em peso medium pequeno.
- **Layout:** Formato retrato 4:5. Sistema editorial vertical rigido e repetivel: header fixo (logo Iconly a esquerda, 'Icon Set' a direita), zona central com badge numerado + titulo centralizado + subtitulo, e o mockup de navegacao flutuando dentro de um container tracejado (dashed) de cantos arredondados que funciona como 'palco'. Rodape fixo com 'iconly.pro' a esquerda e 'Swipe for More ->' a direita. Muito respiro/whitespace, densidade baixa, tudo centralizado. Capa quebra o padrao com pill 'Save This / Part 3', numero '10' gigante em marca d'agua e grid 2x2 de previews.
- **Vale roubar:** Container tracejado como 'stage' que emoldura o componente e comunica 'isto e um mockup/artboard'; Barras de navegacao pill com neumorfismo suave: sombra externa difusa + leve inner light, dando sensacao de superficie fisica flutuante; Item ativo destacado com pill preenchido + label textual enquanto os demais ficam so em icone cinza (padrao de bottom-nav expansivel); Uso pontual de UM acento colorido por slide (azul, verde, violeta, coral) contra base monocromatica, mantendo coesao e variando ritmo; FAB circular com gradiente destacado para acao primaria; Sistema de carrossel numerado com badge pill + CTA 'Swipe for More' repetido, otimo para retencao; Consistencia de header/footer como moldura de marca em todos os slides
- **Mood:** clean, minimal, profissional, tatil, leve, moderno, tech, arejado, premium discreto

### 02: @iconlypro (pasta `02__iconlypro__292365`)
Carrossel promocional da biblioteca de icones Iconly, mostrando uma tela de Settings mockada em estilo neumorphism claro, a familia de icones (linha e solido) e telas do plugin com 40.000+ icones flat/3D/animados.

- **Paleta observada:** `#ECECEE` fundo (cinza off-white neutro); `#FFFFFF` cards e superficies elevadas; `#0A0A0A` texto/icones primarios (quase preto); `#2C5FF6` acento azul (logo, FAB de busca, gradiente); `#34C759` toggle ativo verde (Push Notification); `#9A9AA0` texto secundario/legendas cinza
- **Tipografia:** Sans-serif geometrica de peso variavel, bem no espirito Poppins/Circular. Titulos display em bold pesado com tracking apertado ("Design smarter with Iconly"), labels de UI em semibold, e legendas/metadados em regular cinza claro. Hierarquia clara por peso e cor mais do que por tamanho; cantos e terminais arredondados que combinam com o soft-UI.
- **Layout:** Formato quadrado/vertical de carrossel com margens generosas e muito respiro. Sistema consistente: logo Iconly no topo-esquerdo, rotulo "Icon Set" no topo-direito, e rodape com "iconly.pro" a esquerda e "Swipe for More >" a direita, ancorando todos os slides. O heroi central e um unico card flutuante com sombra suave e difusa. Densidade baixa, tudo centralizado, grid de icones 4x2 e grids de plugin bem espacados. Composicao respira e valoriza o objeto de UI isolado sobre fundo neutro.
- **Vale roubar:** Sombra neumorphica dupla muito suave e difusa que faz cards brancos parecerem flutuar sobre fundo quase-branco; Sistema de moldura de slide consistente (logo topo-esquerda, tag topo-direita, iconly.pro + Swipe for More no rodape) que da identidade de serie; Toggle verde iOS e FAB azul com micro-gradiente como unicos pontos de cor num layout monocromatico; Par de icones linha vs solido lado a lado mostrando o range do set; Contraste de aspiracao: tipografia display gigante bold vs UI minimal delicada; Placeholder de foto de perfil realista embutido no mockup de Settings
- **Mood:** clean, premium, soft, arejado, tech-minimal, confiavel, tatil, moderno

### 03: @iconlypro (pasta `03__iconlypro__384954`)

Carrossel promocional do Iconly (biblioteca de icones): um mockup de app ficticio "Good Morning" com grid de icones em tiles cinza claro e nav bar flutuante com botao laranja gradiente; uma grade de icones em pares outline/filled sobre fundo cinza liso; um crop macro isolando so a nav bar flutuante; e um slide final de hero do site do Iconly com headline bold e screenshots do plugin empilhados. Carrossel de 4 imagens acompanhado de video (video nao assistido na analise).

- **Paleta observada:**
  - `#F0F0EF`: fundo cinza claro base (todas as imagens)
  - `#FFFFFF`: branco do cartao/base do mockup
  - `#ECECEC`: cinza claro dos tiles de icone (neumorphism)
  - `#1A1A1A`: preto para texto, logo e icones ativos
  - `#FF9A3D`: laranja gradiente do botao de destaque circular
  - `#4B5EF5`: azul-violeta do logo/monograma Iconly
  - `#FBEBD9`: pessego claro no gradiente de fundo do header do mockup
  - `#E3E1F5`: lavanda claro no gradiente de fundo do header do mockup
- **Tipografia:** Sans-serif rounded geometrica (aparencia tipo Poppins/SF Rounded), bold para headlines ("Good Morning", "Design smarter with Iconly") e regular/medium para labels de icone e subtitulos; hierarquia construida por peso e tamanho dentro da mesma familia, terminais arredondados reforcando o tom tatil.
- **Layout:** Mockup de app flutuante centralizado com sombra suave sobre fundo claro (grid 3x2 de tiles de icone + tab bar inferior); slide de grade pura de icones em pares outline/filled, 4 colunas, generosa margem e fundo liso sem gradiente; crop macro isolando um unico componente de UI (a nav bar) com espaco negativo extremo acima; slide final de hero de site com texto centralizado seguido de dois screenshots do produto empilhados sangrando nas bordas laterais.
- **Vale roubar:** Grid de comparacao outline/filled do mesmo icone lado a lado sobre fundo cinza liso, sem gradiente, para vender variacao de estilo de forma clara; Gradiente sutil pessego-para-lavanda atras do card de mockup como variante 'quente' do neumorphism puramente cinza; Crop macro isolando um unico componente de UI (ex: a nav bar) com espaco negativo generoso acima, otimo para destacar microdetalhe em carrossel; Botao de acao circular com gradiente laranja e raios internos brancos como unico ponto de cor saturada numa paleta majoritariamente neutra; Textura de grain/ruido sutil no fundo claro para nao ficar chapado; Slide de hero de site com headline bold centralizada + screenshots do produto empilhados sangrando nas bordas, util para criativos de divulgacao de skill/ferramenta
