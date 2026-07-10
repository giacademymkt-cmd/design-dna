# Princípios de Motion Premium (`motion-principios`)

A bíblia de gosto do DNA em motion: o que separa animação premium de animação de template. Leia antes de animar QUALQUER peça. As receitas prontas (parallax, reveal, drag, SVG) vivem em outros arquivos; aqui ficam as regras que julgam se foram bem aplicadas.

## Gosto e Contenção

### O Filtro da Frequência
O que é: antes de animar, pergunte quantas vezes por dia a ação se repete. Repetição vira fricção; raridade sustenta o delight.

- Altíssima frequência (digitar, seta): nunca anima. Alta (dropdown, tooltip, nav, ~10x/dia): mínimo, ~80ms linear.
- Normal (~1x/dia): easing e duração padrão. Rara ou primeira impressão (hero, onboarding): pode caprichar, 400-600ms.

Armadilha: animar hover de item usado 50x/dia vira ruído; zerar motion de momentos únicos tira a alma da peça.
Fonte: emilkowal.ski/ui/great-animations e rauno.me/craft/interaction-design

### Duração por Papel do Elemento
O que é: a duração ideal depende do tamanho e do papel do elemento; quanto menor e mais perto do clique, mais rápido.

- Botão ~140ms, tooltip ~160ms, dropdown ~200ms, modal/drawer ~350ms. Quase tudo fica abaixo de 300ms.
- Saída sempre mais rápida que entrada (~60% da duração), o usuário já decidiu sair.

Armadilha: duração igual em tudo (300ms+) é o slop mais comum; saída com a mesma duração da entrada é o segundo.
Fonte: emilkowal.ski/ui/great-animations e 7-practical-animation-tips

### Nada Nasce do Zero
O que é: elemento que entra nunca começa de `scale(0)` ou sem forma. Estado inicial: scale 0.9-0.95 + opacity baixa e, na variante premium, leve blur que resolve em nitidez ("blur fade").

- `initial`: opacity 0, scale 0.9-0.95, translateY 6-8px, blur até 6-10px na variante blur fade.
- Stagger de 30-80ms só entre irmãos do MESMO grupo. `rootMargin` negativo (`-50px`/`-10%`); `unobserve` após o trigger.

Armadilha: escalar de 0 a 1 explode na tela e lê como template; blur acima de 10px custa GPU em mobile.
Fonte: emilkowal.ski/ui/7-practical-animation-tips e magicui.design/docs/components/blur-fade

### Um Sinal de Cada Vez
O que é: erro de campo, estado do botão e toast nunca disparam juntos pro mesmo evento. Cada camada de feedback tem um papel exclusivo.

- Erro de validação: só mensagem inline no campo, nunca toast, nunca sacode a página.
- Sucesso do submit: conta a história no botão primeiro (loading para sucesso); toast é reforço opcional depois.

Armadilha: toast + shake + borda vermelha + ícone juntos lê como pânico da interface, não precisão.
Fonte: nngroup.com "Button States" e filosofia do Sonner (emilkowal.ski)

## Física e Easing

### Mola Nativa CSS (linear() spring)
O que é: timing function que desenha retas entre pontos calibrados, simulando mola real (overshoot + assentamento) em CSS puro, sem JS.

- Gere os pontos em easingwizard.com a partir de stiffness/damping/mass reais, nunca invente de cabeça. Sempre com fallback `cubic-bezier`.
- Overshoot visível em só 1-2 pontos de interação por peça; no resto, curva contida.

```css
:root { --spring: cubic-bezier(0.34, 1.56, 0.64, 1); } /* fallback */
@supports (animation-timing-function: linear(0, 1)) {
  :root { --spring: linear(0, .006, .025, .101, .539, .827, .99, 1.059, 1.084, 1.081, 1.062, 1.037, 1.016, 1.003, .998, .996, .998, 1); }
}
```

Armadilha: spring interrompida no meio do gesto (hover rápido) tem duração reduzida e distorce o movimento, sempre teste com hover rápido.
Fonte: joshwcomeau.com/animation/linear-timing-function

### Easing por Contexto
O que é: a curva de easing é a decisão mais importante de uma animação; sozinha salva um movimento mal construído ou destrói um bom.

- Entra/sai da tela: ease-out forte, ex. `cubic-bezier(0.23,1,0.32,1)`. Morph no lugar: ease-in-out, ex. `cubic-bezier(0.77,0,0.175,1)`.
- Drawer/painel: curva snappy, ex. `cubic-bezier(0.32,0.72,0,1)`. Hover de cor: o ease padrão do navegador já basta.
- Nunca ease-in isolado em algo acionado pelo usuário: o movimento demora a começar bem quando o olho está mais atento.

Armadilha: `transition: all` esconde qual propriedade anima e pode capturar reflow caro sem querer.
Fonte: emilkowal.ski/ui/good-vs-great-animations

### Feedback Contínuo, Compromisso por Limiar
O que é: gestos bons respondem em tempo real durante a interação, mas só "confirmam" a ação quando um limiar é cruzado ou o gesto é solto, retendo velocidade e ângulo ao soltar.

- Calcule a velocidade real a cada `pointermove` (px/ms); use pra decidir commit por flick e escalar a duração da saída.
- Limiar comum: ~35% da largura do elemento OU flick acima de ~0.5px/ms. Zere a `transition` no `pointerdown`.
- Trate `pointercancel`/`pointerleave` como release, nunca deixe o elemento preso a meio caminho.

Armadilha: commit antes do limiar causa acidentes em ações destrutivas; duração fixa no release ignora a velocidade e quebra a física.
Fonte: rauno.me/craft/interaction-design

### Lerp é Tempero, Não Prato Principal
O que é: lerp contínuo (interpolação exponencial por frame) e `scroll-behavior: smooth` (duração fixa) são filosofias que não se misturam. Sem compensar `deltaTime`, 120Hz converge ~2x mais rápido que 60Hz com o mesmo fator.

- Scroll nativo resolve quase tudo (formulário, checkout, âncora, deep-link); se a página tem isso, não usa lerp global.
- Lerp global (sensação Lenis) só se a peça inteira é experiência coesa (hero cinematográfico, portfólio).
- Fator baixo (0.05-0.08): cinematográfico e pesado. Médio (0.1-0.12): padrão. Alto (0.18+): quase imperceptível.

```js
const lerp = (a, alvo, f, deltaMs) => a + (alvo - a) * (1 - Math.pow(1 - f, deltaMs / 16.667));
```

Armadilha: lerp global intercepta e transforma o scroll visualmente; `sticky`, `scroll-snap` e scroll-driven animations leem posição que não bate com a tela, sempre testar juntos.
Fonte: lenis.dev e blog.olivierlarose.com/tutorials/smooth-scroll

### A Regra do Sequestro de Scroll
O que é: scrolljacking intercepta o evento nativo de scroll (wheel, touchmove, teclado) e troca por lógica customizada. Armadilha número um de sites que tentam parecer premium.

- Só aceitável se adiciona contexto funcional real, nunca decoração; curto (1-2 seções, nunca a página inteira).
- Nunca combine texto longo pra ler com direção alterada; nunca em mobile. Teclado continua funcionando sempre.
- Se dá pra resolver com CSS scroll-driven (nunca bloqueia o scroll físico), prefira isso a interceptar o evento.

Armadilha: `preventDefault` em wheel/touchmove quebra teclado, scrollbar e leitor de tela ao mesmo tempo.
Fonte: Nielsen Norman Group, "Scrolljacking 101"

## Performance e Resiliência

### Disciplina do Movimento: Só Transform e Opacity
O que é: toda animação mexe só em `transform` e `opacity`, as únicas propriedades que a GPU compõe sem reflow. `will-change` com moderação, `prefers-reduced-motion` sempre presente.

- Nunca animar `width`, `height`, `left`, `top`, `margin` direto; reescreva com `translate`/`scale`.
- `will-change` só durante a interação, desligue no `transitionend`. "Reduced motion" não é "sem motion nenhum": use crossfade ou snap ao estado final, preservando a affordance.

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after { transition-duration: .001ms !important; animation-duration: .001ms !important; }
}
```

Armadilha: `transition: all` recalcula mais do que precisa; `will-change` permanente degrada memória e GPU à toa.
Fonte: joshwcomeau.com/animation/css-transitions e Codrops

### Guarda de Movimento e Performance
O que é: nenhum loop de scroll (rAF, parallax, scrub) roda sem checar `prefers-reduced-motion` em JS (não só CSS) e sem IntersectionObserver ligando/desligando o loop conforme a viewport.

- Cheque reduced-motion antes de qualquer rAF de scroll. IntersectionObserver liga o loop só com o elemento visível.
- Listener de scroll sempre `passive: true`, leitura/escrita agrupada via rAF.

Armadilha: checar reduced-motion só no CSS deixa o site quieto na aparência mas pesado por baixo.
Fonte: gsap.com/docs/v3/Plugins/ScrollTrigger e MDN prefers-reduced-motion

### Fallback com @supports + IntersectionObserver
O que é: proteção obrigatória pra scroll-driven animations nativas (`animation-timeline: view()`): detecta suporte e só aí deixa o CSS nativo animar; senão, um IntersectionObserver assume sem duplicar trabalho.

- `CSS.supports('animation-timeline: view()')` decide o ramo: nativo silencioso, fallback via IO, ou reduced-motion mostrando tudo direto.
- Nunca rodar CSS nativo e IntersectionObserver juntos no mesmo elemento (gera jank). Estado inicial sempre visível por padrão no CSS.

Armadilha: ignorar reduced-motion no fallback JS anima mesmo quando o usuário pediu menos movimento.
Fonte: MDN (animation-timeline) e Chrome for Developers (scroll-driven-animations)

## Acessibilidade e Craft de Interação

### Alvo Generoso (Lei de Fitts e Cantos Mágicos)
O que é: o tempo pra clicar depende da distância e do tamanho do alvo. Cantos e bordas da tela são "alvos infinitos", o cursor não os ultrapassa.

- Nunca alvo clicável abaixo de 44x44px reais, mesmo com desenho visual menor. Expanda a hit-area (`::before` com `inset` negativo) sem alterar o layout.
- Ações frequentes ganham quando encostadas numa borda ou canto. Clique em filho isolado (svg com onClick próprio) rouba o toque da hit-area, mova o listener pro pai.

Armadilha: "generoso" não é botão grande e clonado lado a lado, é precisão de alcance, não tamanho decorativo.
Fonte: rauno.me/craft/interaction-design

### Otimismo com Rede de Segurança
O que é: a interface assume que a ação vai dar certo e atualiza o estado no instante do clique; se falhar, reverte e avisa, com opção de desfazer.

- Só em ações reversíveis e de baixo risco: curtir, favoritar, arquivar, reordenar. Nunca em ações irreversíveis de alto risco (pagamento, exclusão) sem "Desfazer" real.
- Desenhe o caminho de reversão antes do caminho feliz, não depois.

Armadilha: alternar o estado de novo em erro (em vez de forçar o valor anterior) pode deixar o botão errado se o usuário clicou de novo nesse meio tempo.
Fonte: Simon Hearne "Optimistic UI Patterns"; Vercel Web Interface Guidelines

### Regra do Atraso Mínimo
O que é: antes de mostrar spinner/skeleton, espere um pequeno atraso; se a resposta chega antes, nada aparece. Uma vez visível, mantenha por um tempo mínimo.

- Atraso antes de mostrar: 150-300ms.
- Tempo mínimo visível uma vez mostrado: 300-500ms.

Armadilha: pular o atraso pisca skeleton em respostas rápidas; pular o mínimo faz sumir no meio do ciclo, parece travamento.
Fonte: Vercel Web Interface Guidelines e Vercel Geist Skeleton

### Traço Vivo (a base de tudo)
O que é: técnica raiz de animação de linha em SVG. `stroke-dasharray` igual ao comprimento total do path, animando `stroke-dashoffset` até zero.

- Meça antes de animar: `path.getTotalLength()` define dasharray e dashoffset inicial.
- Esconda o path com `opacity`, nunca `display: none` (`getTotalLength()` retorna 0).
- Scale não uniforme no pai distorce o `stroke-dasharray`, teste em telas grandes. Duração de referência: ~900ms, `cubic-bezier(.65,0,.35,1)`.

Armadilha: em reduced-motion, pule direto pra dashoffset 0 sem transição; o traço nunca é a única forma de entender o ícone.
Fonte: Cassie Evans, "Creating an SVG path drawing animation" (cassie.codes)

## Checklist antes de animar

- [ ] Essa ação se repete dezenas/centenas de vezes por dia? Se sim, cortei ou reduzi ao mínimo?
- [ ] A duração bate com o papel do elemento (abaixo de 300ms, saída mais rápida que a entrada)?
- [ ] Só `transform` e `opacity` estão sendo animados, nada de width/height/left/top direto?
- [ ] Existe bloco `prefers-reduced-motion` que troca o movimento por estado final, sem sumir o elemento?
- [ ] O elemento entra com forma visível (scale 0.9-0.95 + opacity), nunca de `scale(0)`?
- [ ] Só um sinal de feedback por evento, sem toast, shake e borda vermelha juntos?
- [ ] Alvos clicáveis têm pelo menos 44x44px reais de hit-area?
- [ ] Nenhum scroll, teclado ou leitor de tela foi sequestrado sem motivo funcional real?
