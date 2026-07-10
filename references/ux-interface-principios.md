# Princípios de UX e Arquitetura de Informação (`ux-interface-principios`)

A camada de usabilidade do DNA: o que separa um mockup bonito de uma peça que alguém consegue navegar e decidir comprar. Leia antes de desenhar QUALQUER peça com decisão real do usuário (catálogo, PDP, carrinho, formulário, checkout), não só a parte visual. As regras de paleta/tipografia/motion vivem nos outros arquivos; aqui ficam as regras que julgam se a peça bonita também funciona. Exemplos concretos usam como referência um ecommerce pequeno de moda (poucas dezenas de peças, 2 categorias, tráfego majoritariamente mobile), o cenário mais comum de loja pequena brasileira.

## As 10 Heurísticas de Nielsen Aplicadas a Ecommerce

### Visibilidade do Status do Sistema
O que é: o sistema sempre informa o que está acontecendo, em tempo razoável e de forma visível, nunca deixando o usuário adivinhar se o clique funcionou.

- Ao clicar "Adicionar ao carrinho", o botão muda de estado (idle → confirmando → contador do carrinho atualiza) na hora, sem depender de o usuário rolar até o topo pra notar o ícone do carrinho mudou.
- Filtro aplicado, cupom validado, CEP calculado: cada ação tem uma resposta visível em menos de 1 segundo, mesmo que seja só um estado de loading no próprio elemento clicado.

Armadilha: tema WooCommerce padrão que só mostra um aviso pequeno no topo da página ("Produto adicionado ao carrinho") fora da viewport em mobile, o cliente clica de novo achando que não funcionou e duplica o item.
Fonte: Nielsen Norman Group, "10 Usability Heuristics for User Interface Design" (heurística 1)

### Correspondência entre o Sistema e o Mundo Real
O que é: a interface fala a língua do cliente, com conceitos e termos familiares, nunca jargão interno de quem construiu a loja.

- Numeração de tamanho no padrão que a cliente reconhece (P/M/G ou 38/40/42), nunca só S/M/L genérico copiado de tema americano.
- Nome de categoria como a cliente pensa ("Vestidos", "Bombachas"), nunca o slug técnico da taxonomia do WordPress vazando na tela ("categoria-2", "produto-tag-outono").

Armadilha: filtro ou breadcrumb mostrando o slug cru do WooCommerce em vez do nome amigável, porque ninguém revisou o texto depois de montar a taxonomia no admin.
Fonte: Nielsen Norman Group, "10 Usability Heuristics" (heurística 2)

### Controle e Liberdade do Usuário
O que é: todo caminho tem saída, e ações erradas são fáceis de desfazer sem precisar recomeçar do zero.

- Remover item do carrinho, trocar tamanho/cor e voltar pra listagem sem perder o filtro aplicado. Editar endereço no meio do checkout sem reiniciar o formulário inteiro.
- Cupom aplicado por engano precisa de um "remover" visível ali mesmo, sem exigir recarregar a página.

Armadilha: checkout de tema padrão sem link de "editar carrinho" visível na etapa de pagamento, forçando o cliente a usar o botão voltar do navegador, que às vezes derruba o CEP já calculado.
Fonte: Nielsen Norman Group, "10 Usability Heuristics" (heurística 3)

### Consistência e Padrões
O que é: o mesmo elemento se comporta e parece igual em toda a loja, e a loja segue convenções que o cliente já aprendeu em outros sites (carrinho no canto superior direito, botão de compra sempre na mesma cor).

- Um único estilo de botão "Comprar"/"Adicionar ao carrinho" em toda a loja, mesma cor, mesmo formato, do início ao fim da jornada.
- Preço no mesmo lugar relativo em todo card da listagem e na mesma posição relativa na PDP.

Armadilha: misturar o botão padrão do tema (retangular, cinza) com um botão customizado só na home ("Comprar agora", pill, colorido), fazendo o cliente reaprender o que é clicável em cada tela.
Fonte: Nielsen Norman Group, "10 Usability Heuristics" (heurística 4)

### Prevenção de Erros
O que é: melhor impedir o erro antes de acontecer do que só avisar depois, principalmente em decisões caras de desfazer (tamanho errado, troca por conta da cliente).

- Guia de medidas visível ANTES de escolher o tamanho, não só depois da compra feita. Botão "Adicionar ao carrinho" desabilitado (com aviso inline) até cor e tamanho estarem selecionados, em vez de deixar adicionar e só mostrar erro na página do carrinho.
- Validação do campo de CEP antes de avançar pro checkout, não só na confirmação final.

Armadilha: permitir clicar "Adicionar ao carrinho" sem variante escolhida e só mostrar o erro depois de redirecionar pra página do carrinho, obrigando a cliente a voltar e refazer o caminho.
Fonte: Nielsen Norman Group, "10 Usability Heuristics" (heurística 5)

### Reconhecimento em Vez de Memorização
O que é: a interface expõe as opções e o estado atual na tela, o cliente nunca precisa lembrar o que já escolheu ou por onde já passou.

- Filtros ativos aparecem como chips removíveis visíveis, nunca escondidos num painel que fecha depois de aplicar.
- Breadcrumb e itens "vistos recentemente" fazem o trabalho de lembrar por ela, ela só reconhece.

Armadilha: barra lateral de filtro que recolhe sozinha depois de marcar uma opção, sem indicar visualmente na tela principal qual filtro está ativo, a cliente esquece o que selecionou e acha que o catálogo é menor do que é.
Fonte: Nielsen Norman Group, "10 Usability Heuristics" (heurística 6)

### Flexibilidade e Eficiência de Uso
O que é: a loja atende tanto quem compra pela primeira vez quanto quem já é cliente frequente, sem forçar todo mundo pelo caminho mais lento.

- Checkout como convidado sempre disponível, conta é opcional e oferecida depois, nunca uma barreira antes de comprar.
- CEP e endereço com preenchimento automático (autocomplete/histórico do navegador), nunca forçando redigitar tudo a cada compra.

Armadilha: exigir criação de conta obrigatória antes de finalizar a compra. É uma das causas mais citadas de abandono de carrinho em pesquisa de ecommerce, e ainda mais grave em loja pequena onde a cliente já hesita mais por não conhecer a marca.
Fonte: Baymard Institute, "Cart Abandonment Rate Statistics"; Nielsen Norman Group, "10 Usability Heuristics" (heurística 7)

### Design Estético e Minimalista
O que é: a tela mostra só a informação relevante pra decisão do momento, cada elemento extra compete por atenção e atrasa a decisão de compra.

- Uma PDP de loja pequena precisa de foto, nome, preço, variante e CTA claros. Não precisa de contador de urgência, pop-up de saída, chat flutuante e newsletter disparando juntos na primeira visita.
- Prova social (avaliação, selo de confiança) entra com peso visual proporcional ao catálogo real, não decoração emprestada de loja grande.

Armadilha: empilhar todos os plugins de "conversão" do WooCommerce ao mesmo tempo (timer de escassez + pop-up de desconto + chat + newsletter), cada um brigando pela atenção da cliente e escondendo a foto do produto que é o que realmente vende peça de moda.
Fonte: Nielsen Norman Group, "10 Usability Heuristics" (heurística 8)

### Ajudar o Usuário a Reconhecer, Diagnosticar e Recuperar-se de Erros
O que é: mensagem de erro em linguagem simples, dizendo exatamente o que aconteceu e o que fazer, nunca um erro técnico cru.

- "CEP inválido, confira e tente de novo" em vez de mensagem genérica de erro de sistema. Campo com erro destacado visualmente, não só um texto solto no topo da página.
- Erro de pagamento recusado explica a causa provável (cartão, limite, dados) sem expor mensagem crua do gateway.

Armadilha: deixar vazar o erro técnico padrão do WooCommerce ("Error processing checkout. Please try again.") sem traduzir nem indicar qual campo tem problema, a cliente não sabe se é o cartão, o CEP ou o site que quebrou.
Fonte: Nielsen Norman Group, "10 Usability Heuristics" (heurística 9)

### Ajuda e Documentação
O que é: quando a interface sozinha não resolve a dúvida, a ajuda certa aparece perto de onde a dúvida nasce, não escondida em algum lugar distante.

- Guia de medidas acessível a partir da própria PDP (link ou modal ao lado do seletor de tamanho), não só num link perdido no rodapé.
- Contato rápido (WhatsApp) visível pra dúvida de última hora antes de fechar a compra, essencial em roupa artesanal onde caimento pode variar peça a peça.

Armadilha: guia de medidas existir só como página estática linkada no rodapé, longe do momento exato em que a cliente está decidindo o tamanho na PDP.
Fonte: Nielsen Norman Group, "10 Usability Heuristics" (heurística 10)

## Arquitetura de Informação para Catálogo Pequeno

### Navegação Direta Substitui Mega-Menu
O que é: mega-menu existe pra resolver a navegação de centenas de SKUs em dezenas de subcategorias. Com 2-3 categorias, ele vira estrutura vazia que só atrasa o clique.

- Com 2-3 categorias, mostre os links direto na barra de navegação (sem dropdown, sem hambúrguer escondendo em desktop), um clique até a listagem.
- Mega-menu só volta a fazer sentido quando o catálogo passar de umas 7-10 categorias reais, com subcategorias que ajudam de verdade a filtrar, não decoração.

Armadilha: usar o tema padrão que já vem com mega-menu e forçar a criação de subcategorias artificiais só pra preencher o menu, criando divisões que confundem mais do que ajudam num catálogo de 30 peças.
Fonte: Nielsen Norman Group, "Mega Menus Work Well for Site Navigation"; Baymard Institute, "Category Navigation Usability"

### Breadcrumb Sempre Visível
O que é: mesmo num catálogo raso (1-2 níveis), o breadcrumb ancora a posição do usuário e devolve o caminho de volta pra categoria em um clique, sem depender do botão voltar do navegador.

- Padrão Início > Categoria > Produto, sempre acima do título na PDP, nunca escondido ou removido por parecer "óbvio demais" com catálogo pequeno.
- Um bônus técnico gratuito: marcar o breadcrumb com dados estruturados ajuda o Google a mostrar o caminho no resultado de busca.

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {"@type": "ListItem", "position": 1, "name": "Início", "item": "https://loja.com/"},
    {"@type": "ListItem", "position": 2, "name": "Vestidos", "item": "https://loja.com/vestidos/"},
    {"@type": "ListItem", "position": 3, "name": "Vestido Bordô Chita", "item": "https://loja.com/vestidos/vestido-bordo-chita/"}
  ]
}
</script>
```

Armadilha: tirar o breadcrumb achando que "com só 2 categorias fica óbvio", o que sobra é depender do botão voltar do navegador, que em tema WooCommerce padrão costuma perder o filtro e a posição de scroll que a cliente tinha.
Fonte: Nielsen Norman Group, "Breadcrumbs Improve Website Navigation"

### Busca Sempre Acessível, Mesmo com Poucas Dezenas de Peças
O que é: busca não é recurso só de catálogo grande, é o atalho de quem já sabe o que quer (chegou de um anúncio ou story procurando uma peça específica) e não quer navegar categoria por categoria.

- Campo ou ícone de busca sempre visível no cabeçalho, nunca escondido dentro do menu hambúrguer exigindo passo extra.
- Autocomplete reconhecendo sinônimo regional (a cliente pode buscar "bombacha" ou "calça gaúcha" pro mesmo produto).

Armadilha: decidir "não precisa de busca, são só 30 produtos" e esconder ou remover o campo, ignorando que boa parte do tráfego chega de anúncio já procurando uma peça específica, não navegando o catálogo inteiro.
Fonte: Baymard Institute, "Ecommerce Search UX"; Nielsen Norman Group, "Search Engines"

## Padrão de Leitura e a Dobra

### Padrão Z para Seções Escaneáveis (hero, banner de categoria)
O que é: em telas com pouco texto e elementos bem espaçados (hero, banner de topo), o olho varre em Z: canto superior esquerdo, desliza até o canto superior direito, desce em diagonal, e termina no canto inferior (esquerdo ou direito, o que estiver mais forte).

- Logo/marca no início do Z (superior esquerdo), ícone de carrinho/busca no fim da primeira barra (superior direito), imagem de destaque no meio da diagonal, CTA de compra no ponto final do Z (inferior, onde o olho pousa por último).
- É por isso que o CTA "Ver coleção"/"Comprar" de um banner de categoria funciona melhor perto do fim visual da composição, não espremido no canto oposto de onde o olho termina o percurso.

Armadilha: colocar o CTA principal no canto onde o Z começa (superior esquerdo) em vez de onde ele termina, forçando o olho a voltar pra trás pra encontrar a ação.
Fonte: Nielsen Norman Group, "F-Shaped Pattern For Reading Web Content" (seção sobre padrões de leitura em página com pouco texto)

### Padrão F para Blocos de Texto Denso (descrição, FAQ)
O que é: em blocos com bastante texto corrido, o olho lê a primeira linha inteira, a segunda parcialmente, e depois só desce escaneando a lateral esquerda. Quase ninguém lê até o fim.

- Nas raras vezes que a peça tem descrição longa (tecido, composição, cuidados), a primeira frase carrega a informação mais decisiva (ex: "100% algodão, cai solto, indicado pra clima quente"), o resto é detalhe pra quem quiser aprofundar.
- Primeiras palavras de cada parágrafo/bullet carregam o substantivo mais importante (à esquerda), nunca enterrar o dado relevante no meio de uma frase longa.

Armadilha: escrever a informação mais útil (tipo de tecido, indicação de uso) no meio ou fim de um parágrafo longo, onde a maioria das clientes já parou de ler.
Fonte: Nielsen Norman Group, "F-Shaped Pattern For Reading Web Content"

### O Que Precisa Estar Acima da Dobra no Mobile
O que é: em 375px de largura (o mobile mais comum de tráfego de ecommerce brasileiro), o espaço acima da dobra é curto e caro, só cabe o que decide a compra.

- Acima da dobra (antes de rolar): foto do produto, nome, preço (com desconto já calculado, não "a partir de"), seletor de variante e o CTA de compra. Selo de confiança curto (frete grátis, troca fácil, compra segura) também cabe aqui como reforço de decisão, não como decoração isolada.
- Descrição longa, ficha técnica completa, avaliações: podem (e devem) ficar depois da dobra, são material de aprofundamento pra quem já decidiu que quer aquela peça.

Armadilha: uma foto grande de banner ocupando a tela inteira em 375px sem preço nem CTA visível, a cliente rola achando que ainda não chegou no produto e faz mais scroll do que precisaria pra decidir.
Fonte: Nielsen Norman Group, "Scrolling and Attention"; Baymard Institute, "Product Page: Above the Fold"

## Carga Cognitiva e Divulgação Progressiva

### Agrupar Cor + Tamanho + Preço + Frete, Não Espalhar em Abas
O que é: a memória de trabalho tem capacidade limitada. Se cor, tamanho, preço e prazo de entrega estão em abas separadas, a cliente precisa lembrar o que viu na aba anterior pra decidir, e a maioria simplesmente desiste antes de juntar tudo na cabeça.

- Seletor de cor, seletor de tamanho, preço final e frete/prazo calculado (não um link pra calcular depois) ficam todos no mesmo bloco visível, sem exigir clique ou troca de aba pra reunir a informação.
- Se o frete precisa de CEP pra calcular, o campo de CEP fica ali mesmo, dentro do bloco de compra, com resultado inline.

Armadilha: colocar a calculadora de frete dentro de um accordion fechado por padrão ou numa aba "Entrega" separada da área principal de compra, forçando a cliente a procurar justamente o dado que decide se ela finaliza a compra.
Fonte: Nielsen Norman Group, "Minimize Cognitive Load to Maximize Usability"; Baymard Institute, "Shipping & Returns on Product Pages"

### Divulgação Progressiva é Para Conteúdo Opcional, Nunca Para Decisão
O que é: esconder informação atrás de "ver mais"/aba/accordion é técnica correta só para conteúdo que não bloqueia a decisão imediata de compra. Preço, prazo e disponibilidade não entram nessa categoria.

- PODE ficar atrás de "ver mais": cuidados com o tecido, história da marca, tabela de medidas detalhada em cm, avaliações completas, política de troca estendida.
- NUNCA pode ficar escondido atrás de clique, aba ou hover: preço final, frete calculado, prazo de entrega, disponibilidade em estoque, desconto ativo. Isso precisa renderizar no primeiro carregamento da PDP.

Armadilha: mostrar "a partir de R$ X" na listagem e só revelar o preço real da variante depois de vários toques na PDP, ou esconder o preço até uma cor/tamanho ser escolhido sem deixar isso óbvio, mina a confiança antes mesmo de chegar no carrinho.
Fonte: Nielsen Norman Group, "Progressive Disclosure"; Baymard Institute, "Product Page UX Benchmark"

## Acessibilidade Prática para Ecommerce

### Contraste Mínimo em Texto de Preço e Desconto
O que é: WCAG 2.1 exige no mínimo 4.5:1 de contraste pra texto normal e 3:1 pra texto grande (a partir de ~18pt ou ~14pt em negrito). Preço e desconto são justamente onde o design costuma enfraquecer o contraste em nome da estética (cinza claro no preço "de", vermelho pastel no "por").

- Preço "de" riscado pode ter menos peso visual, mas ainda precisa bater pelo menos 3:1 contra o fundo. Preço final e badge de "%OFF" (a informação que fecha a venda) precisam bater 4.5:1 com folga.
- Teste com ferramenta de contraste real (ex. WebAIM Contrast Checker), nunca "a olho" na tela do notebook com brilho no máximo.

Armadilha: badge de desconto em rosa/vermelho pastel que parece ótimo no Figma a 100% de brilho no laptop, mas fica ilegível num celular a 60% de brilho, sob sol, que é exatamente onde boa parte do tráfego mobile brasileiro está comprando (rua, ônibus, intervalo do trabalho).
Fonte: WCAG 2.1, Success Criterion 1.4.3 (Contrast Minimum); Nielsen Norman Group, "Color and Contrast"

### Alvo de Toque Mínimo Para Botão de Variante em Mobile
O que é: os seletores de cor e tamanho são justamente o elemento que temas de ecommerce encolhem pra caber várias opções numa linha só, mas são controle que decide a compra, não decoração, então a área de toque importa mais aqui do que em elementos só visuais.

- Área de toque real de no mínimo 44x44px (Apple HIG) ou 48x48dp (Material), escolha um padrão e mantenha em toda a loja. Se o swatch visual for menor (ex. bolinha de cor de 32px), expanda a área de clique sem alterar o desenho.
- Se as opções não cabem numa linha só em 375px sem espremer, quebre pra segunda linha, nunca encolha o alvo pra caber tudo numa linha.

```css
.variante-swatch {
  position: relative;
  width: 32px;
  height: 32px; /* tamanho visual */
}
.variante-swatch::before {
  content: "";
  position: absolute;
  inset: -8px; /* expande a área de toque real para ~48px sem mudar o layout visual */
}
```

Armadilha: espremer P/M/G/GG numa linha só que renderiza a ~28px de largura cada em 375px, causando toque no botão vizinho por engano, um gerador clássico de troca por tamanho errado em loja de roupa pequena.
Fonte: Apple Human Interface Guidelines (touch targets); Material Design (touch target size); mesma técnica de `motion-principios.md` > Alvo Generoso (Lei de Fitts e Cantos Mágicos)

### Texto Alternativo de Imagem de Produto
O que é: alt text é infraestrutura de acessibilidade pra quem usa leitor de tela, e também é o que o Google usa pra entender e indexar a imagem, ponto que importa desde já pro dia que fotos reais substituírem os placeholders.

- Escreva descrevendo a peça de verdade: "[peça] cor [cor], [detalhe relevante]", ex. "Bombacha gaúcha feminina cor bordô com friso lateral", nunca alt vazio numa foto de produto (alt="" só é correto em imagem puramente decorativa).
- Com várias fotos do mesmo produto (frente/costas/detalhe), cada alt descreve o que aquela imagem específica mostra, não repete o mesmo texto genérico em todas.

Armadilha: deixar o alt text automático do WordPress/WooCommerce, que por padrão vira o nome cru do arquivo enviado ("IMG_2847.jpg" ou "produto-1-scaled.jpg"), inútil tanto pra leitor de tela quanto pra busca de imagem.
Fonte: WebAIM, "Alternative Text"; WCAG 2.1, Success Criterion 1.1.1

## Mobile-First Real

### Por Que Desenhar Primeiro a 375px Muda Decisões
O que é: desenhar em desktop e "adaptar" pra mobile depois deixa passar decisões que não sobrevivem num canvas de 375px (filtro em várias colunas, painel de informação lado a lado, interação que depende de hover). Começar pelo menor canvas força a decisão real de hierarquia de informação na hora, porque não sobra espaço pra empurrar o problema pra depois.

- Com a maior parte do tráfego de ecommerce pequeno brasileiro vindo de mobile, perguntas como "preço e CTA cabem acima da dobra" ou "o seletor de tamanho precisa de 2 linhas" só aparecem de verdade desenhando a 375px primeiro.
- Interação de hover (ex: "quick view" ao passar o mouse no card) simplesmente não existe em touch. Desenhar primeiro pensando em hover cria um equivalente de toque mal resolvido depois; desenhar primeiro pra toque evita esse retrabalho.

Armadilha: prototipar em 1440px no Figma, onde espaçamento generoso e layout em várias colunas parecem fáceis, e só ao chegar em 375px cortar informação, geralmente cortando frete/prazo primeiro por parecer "menos importante" quando na prática é decisivo pra fechar a compra.
Fonte: Luke Wroblewski, "Mobile First"; Nielsen Norman Group, "Mobile UX"

### Polegar Como Ponteiro (zona de alcance)
O que é: segurando o celular com uma mão em telas de 375-428px, o polegar alcança o centro-inferior da tela com facilidade; os cantos superiores exigem trocar a pega ou usar a outra mão.

- CTA de compra fixo (sticky) na parte inferior da viewport durante o scroll da PDP mantém a ação principal sempre ao alcance do polegar, mesmo depois de rolar pra ler a descrição.
- Ações frequentes (adicionar ao carrinho, aplicar filtro) ganham quando posicionadas na metade inferior da tela; ações raras (configuração de conta) podem ficar no topo sem prejuízo.

Armadilha: deixar "Adicionar ao carrinho" só na posição original perto do preço, no topo da PDP; assim que a cliente rola pra ler a descrição, a ação de compra vira um alcance de duas mãos, e cada rolagem de tela vira fricção extra pra fechar a venda.
Fonte: Nielsen Norman Group, "Thumb Zone Mapping" (pesquisa de Steven Hoober)

## Checklist de Usabilidade Antes de Entregar Qualquer Peça de Ecommerce

- [ ] O status de cada ação (adicionar ao carrinho, aplicar filtro, aplicar cupom) fica visível em menos de 1 segundo?
- [ ] A navegação usa a linguagem da cliente (P/M/G, nome real de categoria), nunca termo interno ou slug de admin?
- [ ] Dá pra editar carrinho, trocar variante e voltar sem perder o que já estava preenchido?
- [ ] Breadcrumb visível em toda página de categoria e produto?
- [ ] Busca sempre acessível no cabeçalho, mesmo com catálogo pequeno?
- [ ] Preço, frete/prazo e CTA de compra aparecem juntos, sem exigir aba ou clique extra?
- [ ] Descrição longa, ficha técnica e política de troca estão atrás de "ver mais", nunca o preço ou o prazo?
- [ ] Contraste de preço e desconto testado (ferramenta, não a olho) e passa em pelo menos 4.5:1?
- [ ] Botões de variante (cor/tamanho) têm no mínimo 44x44px reais de área de toque?
- [ ] Toda imagem de produto tem alt text específico, nunca nome de arquivo cru ou alt vazio?
- [ ] A peça foi desenhada primeiro a 375px, não adaptada de um mockup pensado pra desktop?
- [ ] O CTA de compra permanece ao alcance do polegar durante o scroll (sticky em página longa)?
