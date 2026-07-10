# Receitas de Scroll Premium (`motion-scroll`)

Livro de receitas vanilla (HTML, CSS e JS puro, sem lib) para tudo que se move em resposta ao scroll: reveals de entrada, parallax, seções presas, trilhos horizontais e transições de capítulo. Leia sempre que a peça tiver narrativa de scroll, reveals de conteúdo ou qualquer camada com sensação de profundidade.

Todo código abaixo já foi verificado e cola direto num HTML único. Todas as receitas respeitam `prefers-reduced-motion` como regra obrigatória, nunca como detalhe opcional.

---

## Índice

| Receita | Quando usar |
|---|---|
| Reveal Nativo ao Rolar | Entrada de qualquer bloco de conteúdo (headline, imagem, card) ao rolar pra dentro da tela |
| Parallax Nativo em CSS | Camada de imagem ou forma com profundidade sutil em hero ou seção editorial, sem JS de scroll |
| Traço Guiado pelo Scroll | Ícone ou linha SVG cujo desenho acompanha o progresso real do scroll numa seção longa |
| Snap Elegante sem Travar o Usuário | Galerias horizontais ou 2 a 4 seções full-viewport que devem encaixar sem travar o usuário |
| Ancoragem Suave com Foco Correto | Toda navegação por link âncora: menu de seções, sumário, voltar ao topo |
| Ícone Nasce ao Entrar na Tela | Ícones de linha (feature, como funciona) que ganham vida uma única vez ao entrar na viewport |
| Revelação em Lote com IntersectionObserver | Listas, grids ou features com múltiplos itens que revelam em cascata ao rolar |
| Parallax de Elemento com Lerp | Imagem de hero, galeria de cases ou fileira de cards com deslocamento suave e flutuante |
| Scrub via rAF com Lerp | Qualquer transformação contínua amarrada ao scroll dentro de uma seção |
| Lerp Follower Vanilla | Sensação de scroll pesado e cinematográfico em hero de estúdio ou case study, só desktop |
| Pin com Troca de Conteúdo | Storytelling em 3 a 5 etapas onde um visual fica fixo e o texto ao lado muda |
| Trilho Horizontal Pinado | Showcase de projetos ou galeria curta (3 a 5 itens) que desliza na horizontal dentro do scroll vertical |
| Transição de capítulo em wipe | Corte marcante entre grandes blocos temáticos de uma LP |

---

## Nativo sem JS (scroll-driven CSS)

### Reveal Nativo ao Rolar

Anima a entrada de um elemento (opacidade mais leve translateY) amarrada à posição real dele na viewport, via `animation-timeline: view()` nativo do CSS. Sem scroll listener, sem rAF: o navegador liga a timeline da animação ao progresso do elemento cruzando a tela.

Quando usar: toda entrada de headline, imagem editorial ou bloco de conteúdo relevante ao rolar a página. Nunca em três elementos idênticos com o mesmo range, isso é o clichê que o DNA proíbe.

```html
<style>
@keyframes reveal-up {
  from { opacity: 0; transform: translateY(24px); }
  to   { opacity: 1; transform: translateY(0); }
}

.reveal {
  animation: reveal-up linear both;
  animation-timeline: view();
  animation-range: entry 0% cover 40%;
}

/* Fallback obrigatório: sem isso, a animação nativa acima ainda roda
   como animação normal (duration 0s) e revela tudo instantaneamente no load */
@supports not (animation-timeline: view()) {
  .reveal {
    animation: none;
    opacity: 0;
    transform: translateY(24px);
    transition: opacity .6s ease, transform .6s ease;
  }
  .reveal.is-visible {
    opacity: 1;
    transform: none;
  }
}

@media (prefers-reduced-motion: reduce) {
  .reveal {
    animation: none;
    transition: none;
    opacity: 1;
    transform: none;
  }
}
</style>

<script>
// fallback só roda se o navegador não suportar scroll-driven animations
if (!CSS.supports('animation-timeline: view()')) {
  const io = new IntersectionObserver(entries => {
    entries.forEach(e => e.target.classList.toggle('is-visible', e.isIntersecting));
  }, { threshold: 0.3 });
  document.querySelectorAll('.reveal').forEach(el => io.observe(el));
}
</script>
```

Armadilhas: suporte ainda não é universal (Firefox atrás de flag), sempre usar `@supports` com fallback funcional, nunca decorativo. Nunca deixar os dois caminhos (nativo e IntersectionObserver) ativos ao mesmo tempo, isso duplica a animação. `animation-range` curto demais (tipo `entry 0% cover 10%`) faz o elemento pular em vez de revelar; varie o range por seção para não virar template reconhecível. **Bug real confirmado em Chromium**: se a página tem qualquer link âncora (nav, CTA, sumário) apontando pra uma seção mais abaixo e essa seção usa `.reveal`, saltar direto pra lá (clique ou carregar a URL já com `#id`) trava os elementos em opacidade parcial (ex: `opacity: 0.65` preso, nunca chega a 1), porque a `animation-range` é calculada uma vez no momento do salto e só recalcula com novo scroll. Se a peça tem QUALQUER navegação por âncora (ou seja, quase sempre que existe nav com links de seção), aplique o "nudge" de scroll da receita `Ancoragem Suave com Foco Correto` logo abaixo, ele existe justamente por causa desse bug.

Fontes: joshwcomeau.com/animation/scroll-driven-animations, developer.chrome.com/docs/css-ui/scroll-driven-animations, MDN (CSS scroll-driven animations e animation-range).

Variante Framer: `whileInView` com `viewport={{ once: true, amount: 0.3 }}` dispensa o `@supports` manual, o Motion cuida do fallback entre browsers.

### Parallax Nativo em CSS (scroll-timeline)

Desloca uma camada (imagem, forma, texto secundário) verticalmente em sincronia com o scroll usando `animation-timeline: scroll()` nativo, com fallback em rAF para navegadores sem suporte. A camada fica sobredimensionada dentro de um wrapper com `overflow: clip` para nunca revelar vazio nas bordas.

Quando usar: imagem de fundo de hero ou imagem editorial dentro de uma seção com mais de uma camada visual. Deslocamento sempre pequeno e discreto, nunca a técnica de banner datada dos anos 2010.

```html
<style>
.parallax-wrap {
  position: relative;
  overflow: clip;
}

.parallax-layer {
  position: absolute;
  inset: -8% 0;       /* estoura o wrapper na mesma medida do deslocamento máximo */
  width: 100%;
  height: 116%;        /* altura do wrapper mais 2x o deslocamento máximo, evita vão nas bordas */
  object-fit: cover;   /* remova se .parallax-layer não for img ou video */
  will-change: transform;
}

@supports (animation-timeline: scroll()) {
  .parallax-layer {
    animation: parallax-shift linear;
    animation-timeline: scroll(nearest block);
    animation-range: cover 0% cover 100%;
  }
}

@keyframes parallax-shift {
  from { transform: translateY(-6%); }
  to   { transform: translateY(6%); }
}

@media (prefers-reduced-motion: reduce) {
  .parallax-layer {
    animation: none !important;
    transform: none !important;
    will-change: auto;
  }
}
</style>

<script>
// fallback só roda quando o navegador não suporta animation-timeline:scroll()
// e o usuário não pediu menos movimento
if (!CSS.supports('animation-timeline', 'scroll()') &&
    !matchMedia('(prefers-reduced-motion: reduce)').matches) {
  const layers = document.querySelectorAll('.parallax-layer');
  let ticking = false;
  function update() {
    layers.forEach(layer => {
      layer.style.transform = `translateY(${Math.min(6, scrollY * 0.02)}%)`;
    });
    ticking = false;
  }
  addEventListener('scroll', () => {
    if (!ticking) { ticking = true; requestAnimationFrame(update); }
  }, { passive: true });
}
</script>
```

Armadilhas: deslocamento acima de 8 a 12% (ou 60px) lembra parallax datado e quebra o princípio anti-slop de sobriedade. Esquecer `overflow: clip` no wrapper ou o oversize da camada revela vão vazio na borda durante o scroll, essa é a armadilha mais comum. Suporte a `animation-timeline: scroll()` ainda é parcial, sempre ter fallback com rAF e throttle (`ticking`). `will-change` permanente custa memória de GPU, desligar em reduced motion.

Fontes: MDN (animation-timeline/scroll), scroll-driven-animations.style de Bramus Van Damme, brad-holmes.co.uk sobre por que a maioria dos scroll animations erra o que a Apple acerta.

### Traço Guiado pelo Scroll

Em vez de disparar o desenho de um traço SVG uma vez ao entrar na tela, o próprio progresso do scroll controla o `stroke-dashoffset` via `animation-timeline: view()`, com fallback em JS por throttle de rAF. O atributo `pathLength="1"` vai direto no `<path>` do SVG, igual na técnica do checkmark.

Quando usar: linha do tempo vertical, indicador de progresso de leitura ou traço decorativo que acompanha uma seção longa de storytelling. Não vale a pena em ícones pequenos, o efeito só se percebe com espaço de scroll suficiente.

```html
<style>
.linha-scroll { stroke-dasharray: 1; stroke-dashoffset: 1; }

@supports (animation-timeline: view()) {
  .linha-scroll {
    animation: desenhar-scroll linear both;
    animation-timeline: view();
    animation-range: entry 10% cover 60%;
  }
}
@keyframes desenhar-scroll { to { stroke-dashoffset: 0; } }
@media (prefers-reduced-motion: reduce) {
  .linha-scroll { animation: none; stroke-dashoffset: 0; }
}
</style>

<script>
// fallback só registra se o navegador não entender animation-timeline
if (!CSS.supports('animation-timeline: view()')) {
  const path = document.querySelector('.linha-scroll');
  if (path) {
    let ticking = false;

    const atualizar = () => {
      const r = path.getBoundingClientRect();
      // progresso 0 a 1 cobrindo toda a janela em que o elemento fica visível
      const percorrido = innerHeight - r.top;
      const total = innerHeight + r.height;
      const progresso = Math.min(1, Math.max(0, percorrido / total));
      path.style.strokeDashoffset = String(1 - progresso);
      ticking = false;
    };

    addEventListener('scroll', () => {
      if (ticking) return;
      ticking = true;
      requestAnimationFrame(atualizar);
    }, { passive: true });

    atualizar(); // fixa o estado certo mesmo antes do primeiro scroll
  }
}
</script>
```

Armadilhas: `animation-timeline: view()` ainda não roda em todos os navegadores, o fallback com scroll mais rAF é obrigatório, não opcional. Não deixar os dois caminhos ativos ao mesmo tempo, senão o traço anima duas vezes em conflito. `animation-range` mal calibrado (por exemplo só `cover` sem `entry`) faz o traço terminar antes do usuário acabar de ler a seção.

Fonte: MDN (Scroll-driven animation timelines), Smashing Magazine (An Introduction To CSS Scroll-Driven Animations).

Variante Framer: `useScroll` mais `useTransform` para mapear `scrollYProgress` em `pathLength`, funcionando em todos os browsers desde já, sem precisar de `@supports`.

### Snap Elegante sem Travar o Usuário

`scroll-snap-type` com `proximity` (nunca `mandatory`) mais `scroll-padding` para compensar header fixo, dando sensação de encaixe em seções ou cards sem nunca impedir o usuário de parar entre pontos de snap.

Quando usar: galerias horizontais, carrosséis de cards ou 2 a 4 seções full-viewport de storytelling curto. Evite `mandatory` onde texto longo possa ficar cortado no meio do encaixe.

```css
.snap-container {
  height: 100vh; /* ou 100dvh, sem altura definida o overflow-y:auto nunca ativa */
  overflow-y: auto;
  scroll-snap-type: y proximity; /* proximity é gentil, mandatory é agressivo */
  scroll-padding-top: var(--header-height, 0px);
  scroll-behavior: smooth;
}

.snap-section {
  scroll-snap-align: start;
  scroll-snap-stop: normal; /* 'always' força parar em cada uma, evite */
  min-height: 100dvh;
}

/* Variante horizontal para galerias e carrosséis: troque o eixo em vez de
   empilhar os dois ao mesmo tempo no mesmo elemento */
.snap-container--horizontal {
  height: auto;
  overflow-x: auto;
  overflow-y: hidden;
  scroll-snap-type: x proximity;
  scroll-padding-left: var(--gutter, 0px);
  scroll-behavior: smooth;
}
.snap-container--horizontal .snap-section {
  scroll-snap-align: start;
  min-height: auto;
}

@media (prefers-reduced-motion: reduce) {
  .snap-container,
  .snap-container--horizontal {
    scroll-behavior: auto;
  }
}
```

Armadilhas: `mandatory` combinado com `scroll-snap-stop: always` pode prender o usuário seção a seção mesmo em scroll rápido, replicando o mesmo problema do scrolljacking em CSS. Sempre testar com teclado (Page Down, seta) e trackpad rápido antes de publicar. Nunca aplicar `scroll-snap-type` no `html` ou `body` inteiro, isso quebra a expectativa de scroll de conteúdo normal.

Fonte: MDN (Basic concepts of scroll snap), CSS-Tricks (Practical CSS Scroll Snapping).

### Ancoragem Suave com Foco Correto

`scroll-behavior: smooth` nativo para links âncora, sempre movendo o foco de teclado junto com o scroll visual via evento `scrollend` (com fallback em `setTimeout` para navegadores sem suporte). Scroll suave sem gestão de foco é a falha de acessibilidade mais comum e mais invisível em sites bonitos.

Quando usar: toda navegação por âncora, menu de seções, sumário, botão voltar ao topo. Sempre, sem exceção.

```html
<style>
html {
  scroll-behavior: smooth;
}

@media (prefers-reduced-motion: reduce) {
  html {
    scroll-behavior: auto;
  }
}
</style>

<script>
(function () {
  let alvoPendente = null;

  function focarAlvoPendente() {
    if (alvoPendente) {
      alvoPendente.focus({ preventScroll: true });
      alvoPendente = null;
    }
  }

  // Corrige elementos .reveal (animation-timeline:view()) travados em opacidade
  // parcial quando a página salta pra uma âncora em vez de rolar aos poucos:
  // o "nudge" de 1px força o navegador a recalcular a timeline de scroll.
  function nudgeScrollTimelines() {
    requestAnimationFrame(() => {
      window.scrollBy(0, 1);
      requestAnimationFrame(() => window.scrollBy(0, -1));
    });
  }

  // 'scrollend' dispara no elemento que de fato rola (document/viewport),
  // nunca no elemento-alvo do link, por isso o listener vai no document
  const suportaScrollend = 'onscrollend' in window;
  if (suportaScrollend) {
    document.addEventListener('scrollend', focarAlvoPendente);
  }

  document.querySelectorAll('a[href^="#"]').forEach((link) => {
    link.addEventListener('click', () => {
      const id = decodeURIComponent(link.getAttribute('href').slice(1));
      if (!id) return;

      const alvo = document.getElementById(id);
      if (!alvo) return;

      // só força tabindex se o elemento não for focável nativamente
      if (alvo.tabIndex < 0) {
        alvo.setAttribute('tabindex', '-1');
      }

      alvoPendente = alvo;
      nudgeScrollTimelines();

      if (!suportaScrollend) {
        // fallback para navegadores sem suporte a 'scrollend' (ex: Safari antigo)
        setTimeout(focarAlvoPendente, 600);
      }
    });
  });

  // Se a página já carrega com um hash na URL (link direto, refresh, compartilhamento),
  // o navegador pula pra âncora antes desse script rodar: aplica o nudge também aqui.
  if (location.hash) {
    nudgeScrollTimelines();
  }
})();
</script>
```

Armadilhas: sem `tabindex="-1"` em elementos não focáveis (section, div, h2), `alvo.focus()` simplesmente não faz nada e o foco de teclado fica órfão na página anterior. Sem o listener de `scrollend` (ou fallback com `setTimeout` em navegadores sem suporte), o foco pula antes do scroll visual terminar. `scroll-behavior: smooth` sozinho, sem esse JS de foco, é a causa mais comum de reclamação de usuários de leitor de tela em sites com scroll suave. **Se a peça também usa a receita `Reveal Nativo ao Rolar`** (`animation-timeline:view()`), sempre inclua o `nudgeScrollTimelines()` acima, mesmo que o foco de teclado não seja uma prioridade nessa peça: é a correção pro bug de elementos travados em opacidade parcial ao saltar pra uma âncora, confirmado em teste real (Chromium via Playwright).

Fonte: CSS-Tricks (Smooth Scrolling and Accessibility), MDN (propriedade scroll-behavior).

---

## Com IntersectionObserver

### Ícone Nasce ao Entrar na Tela

Aplica a técnica de traço vivo (`stroke-dasharray`/`stroke-dashoffset`) mas só dispara quando o SVG entra na viewport, uma única vez, escalonando o desenho entre múltiplos paths do mesmo ícone.

Quando usar: ícones de feature, ilustrações de linha em seção de como funciona, qualquer SVG line-art que deve parecer ganhar vida ao rolar até ele. Não usar em elementos que já aparecem acima da dobra no carregamento.

```js
const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;

function prepararTracos(svg) {
  const paths = [...svg.querySelectorAll('path, circle, line')];
  paths.forEach(p => {
    const len = p.getTotalLength ? p.getTotalLength() : 1;
    p.style.strokeDasharray = len;
    p.style.strokeDashoffset = reduced ? 0 : len;
  });
  return paths;
}

const io = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (!entry.isIntersecting) return;

    // para de observar sempre, mesmo com reduced motion, senão o callback
    // continua disparando à toa toda vez que o ícone entra e sai da viewport
    io.unobserve(entry.target);

    if (reduced) return; // já nasceu com dashoffset 0, não anima

    const paths = [...entry.target.querySelectorAll('path, circle, line')];
    paths.forEach((p, i) => {
      p.style.transition = `stroke-dashoffset .8s cubic-bezier(.65,0,.35,1) ${i * 120}ms`;
      requestAnimationFrame(() => { p.style.strokeDashoffset = '0'; });
    });
  });
}, { threshold: 0.4 });

document.querySelectorAll('svg.linha-viva').forEach(svg => {
  prepararTracos(svg);
  io.observe(svg);
});
```

Armadilhas: preparar (setar dasharray e dashoffset) precisa acontecer antes de o observer disparar, senão o ícone pisca cheio por um frame antes de esconder o traço. Threshold baixo demais (tipo 0.1) dispara cedo demais, antes do usuário perceber o ícone entrando. Sempre dar `unobserve` depois do disparo, senão o ícone anima de novo toda vez que o usuário sobe e desce a página.

Fonte: técnica de stroke-dasharray/dashoffset documentada por Cassie Evans (cassie.codes) e CSS-Tricks; gatilho por IntersectionObserver é padrão de mercado para scroll-reveal sem biblioteca.

Variante Framer: `whileInView` com `viewport={{ once: true, amount: 0.4 }}` no `motion.svg`, e cada `motion.path` filho recebe um `custom={i}` para escalonar via variants.

### Revelação em Lote com IntersectionObserver (Stagger + Profundidade)

Um único `IntersectionObserver` observa todos os itens de uma lista ou grid, e cada um revela individualmente (opacidade, `translateY` e um leve blur que dissolve) ao cruzar o threshold, escalonado por uma custom property `--i`. É o equivalente vanilla do `ScrollTrigger.batch()` do GSAP: nunca cria um observer por elemento.

Quando usar: lista de features, grade de cards ou itens de uma seção que devem entrar em cascata curta, especialmente quando a peça quer comunicar hierarquia entre eles. Nunca em três cards clones revelando ao mesmo tempo.

```html
<style>
.reveal-item {
  opacity: 0;
  filter: blur(6px);
  transform: translateY(16px);
  transition: opacity 500ms cubic-bezier(0.16, 1, 0.3, 1),
              filter 500ms cubic-bezier(0.16, 1, 0.3, 1),
              transform 500ms cubic-bezier(0.16, 1, 0.3, 1);
  transition-delay: calc(var(--i, 0) * 70ms);
  will-change: opacity, filter, transform;
}
.reveal-item.is-in {
  opacity: 1;
  filter: blur(0);
  transform: translateY(0);
}

@media (prefers-reduced-motion: reduce) {
  .reveal-item { transition: opacity 200ms linear; }
  .reveal-item.is-in { filter: none; transform: none; }
}
</style>

<script>
// cols = quantos itens formam uma "linha" visual antes do stagger reiniciar.
// Lista vertical simples: cols = 1. Grid de N colunas: cols = N, senão o
// último item de uma lista longa espera segundos pra entrar.
const cols = 1;

const items = document.querySelectorAll('.reveal-item');
items.forEach((el, i) => el.style.setProperty('--i', i % cols));

// um único IntersectionObserver observando todos os itens: cada um revela
// ao cruzar o threshold, sem criar um observer por elemento
const io = new IntersectionObserver(entries => {
  entries.forEach(entry => {
    if (!entry.isIntersecting) return;
    entry.target.classList.add('is-in');
    io.unobserve(entry.target);
  });
}, { threshold: 0.2, rootMargin: '0px 0px -10% 0px' });

items.forEach(el => io.observe(el));
</script>
```

Variante de gatilho: quando os itens precisam nascer juntos como um conjunto só (por exemplo, três blocos da mesma frase), observe o `.reveal-group` inteiro em vez de cada `.reveal-item`, e dispare `classList.add('is-in')` em todos os filhos de uma vez quando o grupo entrar. O stagger via `transition-delay` continua criando a cascata visual mesmo com o gatilho único.

Armadilhas: criar um `IntersectionObserver` por item em vez de um único observer para todos derruba a performance em listas longas, exatamente o problema que `batch()` resolve. Usar `--i` global sem resetar por linha ou coluna faz o último item de um grid grande esperar segundos pra entrar. Exagerar no blur (acima de 8 a 10px) fica caro pra pintar e trava em listas longas, sempre desligar no reduced motion. Anti-slop: use isso pra revelar texto, listas ou números, não pra animar três cards genéricos de feature entrando juntos.

Fontes: gsap.com/docs (ScrollTrigger.batch), codepen.io/GreenSock, rauno.me/craft/interaction-design e rauno.me/craft/depth.

Variante Framer: `const container = { visible: { transition: { staggerChildren: 0.07 } } }; const item = { hidden: { opacity: 0, y: 16, filter: 'blur(6px)' }, visible: { opacity: 1, y: 0, filter: 'blur(0px)' } };` com `motion.div` usando `variants` e `whileInView`.

---

## Com requestAnimationFrame

### Parallax de Elemento com Lerp

Um elemento (ou imagem dentro de um frame sobredimensionado) se desloca numa velocidade diferente da página conforme atravessa a viewport. O progresso vem da própria posição do elemento (não do scroll do documento inteiro) e é suavizado por interpolação linear (lerp) a cada frame de `requestAnimationFrame`.

Quando usar: imagem de hero, galerias, grades de cases ou fileiras de cards que pedem profundidade sutil sem virar carrossel chamativo.

```html
<style>
.parallax-frame {
  overflow: hidden;
  position: relative;
}
.parallax-img {
  position: absolute;
  left: 0;
  top: -8%;
  width: 100%;
  height: 116%;
  object-fit: cover;
  will-change: transform;
}
@media (prefers-reduced-motion: reduce) {
  .parallax-img { transform: none !important; }
}
</style>

<script>
const clamp = (v, a, b) => Math.min(b, Math.max(a, v));
const MAX_SHIFT = 8;  // porcentagem, mantenha sutil (não passe de 12 a 15%)
const LERP = 0.08;    // fator de suavização por frame; quanto menor, mais flutuante
const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;

const items = [...document.querySelectorAll('.parallax-img')].map(el => ({
  el, current: 0, target: 0
}));

function measure() {
  const vh = innerHeight / 2;
  items.forEach(item => {
    const r = item.el.parentElement.getBoundingClientRect();
    const t = clamp((r.top + r.height / 2 - vh) / vh, -1, 1);
    item.target = -t * MAX_SHIFT;
  });
}

function loop() {
  items.forEach(item => {
    item.current += (item.target - item.current) * LERP;
    item.el.style.transform = `translate3d(0, ${item.current.toFixed(3)}%, 0)`;
  });
  requestAnimationFrame(loop);
}

// pra um deslocamento direto, sem suavização flutuante, troque LERP por 1
if (!reduced && items.length) {
  addEventListener('scroll', measure, { passive: true });
  addEventListener('resize', measure);
  measure();
  requestAnimationFrame(loop);
}
</script>
```

Nota: para um elemento único fora de galeria (uma imagem de hero, por exemplo), aplique `.parallax-img` direto num wrapper com `position: relative` e `overflow: hidden`, sem precisar de `aspect-ratio` fixo.

Armadilhas: animar `top`/`left` em vez de `transform` trava o layout e perde a GPU. Esquecer o oversize da camada (position absolute, inset negativo, altura maior que o container) revela vão vazio na borda durante o scroll, essa é a armadilha mais comum. `MAX_SHIFT` acima de 12 a 15% deixa de ser sutileza e vira efeito de slot machine. Rodar o loop com a seção fora da tela desperdiça CPU, pause com `IntersectionObserver` em galerias grandes; `will-change` permanente em muitas imagens custa memória de GPU à toa.

Fontes: blog.olivierlarose.com/tutorials/parallax-scroll, tympanus.net/codrops (creating a smooth horizontal parallax gallery).

Variante Framer: `const { scrollYProgress } = useScroll({ target: frameRef, offset: ['start end','end start'] }); const y = useTransform(scrollYProgress, [0,1], ['-8%','8%']); <motion.img style={{ y }} />`

### Scrub via rAF com Lerp

Calcula um progresso de 0 a 1 pela posição do elemento na viewport e interpola (lerp) esse valor a cada frame numa custom property CSS (`--p`). É o equivalente vanilla do `scrub` do GSAP ScrollTrigger: em vez de disparar uma vez, a transformação acompanha o scroll continuamente.

Quando usar: qualquer transformação contínua amarrada ao scroll dentro de uma seção: reveal de imagem, rotação leve de ícone, parallax sutil, escala de elemento, contador crescendo.

```js
const el = document.querySelector('.scrub-section');
const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
let current = 0, active = false;
const clamp01 = v => Math.min(1, Math.max(0, v));

function getProgress() {
  const r = el.getBoundingClientRect(), vh = innerHeight;
  return clamp01((vh - r.top) / (vh + r.height));
}

function tick() {
  if (!active) return;
  current += (getProgress() - current) * 0.12;
  el.style.setProperty('--p', current.toFixed(4));
  requestAnimationFrame(tick);
}

if (reduce) {
  // sem animação: mostra o estado final direto, nunca deixa opacity:0 travado
  el.style.setProperty('--p', '1');
} else {
  new IntersectionObserver(([e]) => {
    active = e.isIntersecting;
    if (active) requestAnimationFrame(tick);
  }, { threshold: 0 }).observe(el);
}
```

```css
.scrub-section .art {
  transform: translateY(calc((1 - var(--p, 0)) * 40px));
  opacity: var(--p, 0);
}

@media (prefers-reduced-motion: reduce) {
  .scrub-section .art {
    transform: none;
    opacity: 1;
  }
}
```

Armadilhas: rodar o rAF em loop infinito mesmo com a seção fora da viewport gasta CPU e bateria à toa, sempre ligar e desligar com `IntersectionObserver`. Fator de lerp muito alto parece atrasado, muito baixo não suaviza nada. Só anime `transform` e `opacity` via a custom property, nunca `top` ou `width`, senão o navegador recalcula layout a cada frame. Onde o suporte permitir, a alternativa nativa sem JS é `animation-timeline: view()` com `animation-range`, checando `@supports`.

Fontes: gsap.com/docs (ScrollTrigger scrub), web.dev/articles/scroll-driven-animations.

Variante Framer: `const { scrollYProgress } = useScroll({ target: ref }); const y = useTransform(scrollYProgress, [0,1], [40,0]); <motion.div style={{ y, opacity: scrollYProgress }} />`

### Lerp Follower Vanilla

Reconstrói em vanilla o motor por trás da sensação Lenis: guarda uma posição alvo (o scroll real do navegador) e uma posição atual (visual), aproximando uma da outra a cada frame por interpolação linear, aplicada via `transform` em vez de reescrever a posição de scroll.

Quando usar: só quando a peça pede deliberadamente uma sensação de peso, como um hero de estúdio ou um case study cinematográfico. Sempre com fallback total para `prefers-reduced-motion` e sempre restrito a desktop (`pointer: fine`); nunca em touch, onde o momentum nativo do sistema operacional já é superior a qualquer coisa reimplementada em JS.

```html
<div class="scroll-wrap">
  <div class="scroll-content">
    <!-- conteúdo real do hero / case study aqui -->
  </div>
</div>
<div class="scroll-spacer"></div>
```

```css
.scroll-wrap {
  position: fixed;
  inset: 0;
  overflow: hidden;
}
.scroll-content {
  will-change: transform;
}
.scroll-spacer {
  height: 0; /* setada via JS a partir da altura real do conteúdo */
}

/* Em touch e reduced motion a técnica inteira desliga: volta pro scroll nativo puro */
@media (pointer: coarse) {
  .scroll-wrap { position: static; overflow: visible; }
  .scroll-content { transform: none !important; }
  .scroll-spacer { display: none; }
}
@media (prefers-reduced-motion: reduce) {
  .scroll-wrap { position: static; overflow: visible; }
  .scroll-content { transform: none !important; }
  .scroll-spacer { display: none; }
}
```

```html
<script>
const finePointer = matchMedia('(pointer: fine)').matches;
const reduzMovimento = matchMedia('(prefers-reduced-motion: reduce)').matches;

if (finePointer && !reduzMovimento) {
  const content = document.querySelector('.scroll-content');
  const spacer  = document.querySelector('.scroll-spacer');
  const FATOR = 0.1; // 0.1 é a sensação equilibrada, tipo Lenis default

  // inicializa com o scroll real, evita salto do topo ao dar F5 no meio da página
  let atual = window.scrollY;
  let alvo  = window.scrollY;

  function syncHeight() {
    spacer.style.height = content.getBoundingClientRect().height + 'px';
  }
  syncHeight();
  new ResizeObserver(syncHeight).observe(content);
  window.addEventListener('resize', syncHeight);

  function tick() {
    alvo = window.scrollY;
    atual += (alvo - atual) * FATOR;
    if (Math.abs(alvo - atual) < 0.05) atual = alvo; // evita jitter infinitesimal
    content.style.transform = `translate3d(0, ${-atual}px, 0)`;
    requestAnimationFrame(tick);
  }
  requestAnimationFrame(tick);
}
// Em touch ou reduced motion nada disso roda: a página fica 100% no scroll nativo do SO.
</script>
```

Armadilhas: sempre usar `transform`/`translate3d` na thread de composição, nunca `top` ou `margin-top`, que forçam layout a cada frame. Sob `prefers-reduced-motion` e `pointer: coarse`, desligue a arquitetura inteira via media query (`position: fixed` vira `static`, transform vira `none`, spacer some), o momentum nativo do touch é sempre superior. Inicialize `atual`/`alvo` com o `window.scrollY` real, nunca com 0, senão gera salto visível em reload no meio da página. Qualquer `position: fixed` ou `position: sticky` dentro de `.scroll-content` quebra, porque o `transform` no ancestral cria um novo containing block; `IntersectionObserver`, ao contrário do que se pensa, funciona normalmente ali dentro, porque lê geometria já renderizada.

Fonte: darkroomengineering/lenis (README, técnica lerp e raf loop).

Variante Framer: `useScroll()` para pegar `scrollY`, `useSpring(scrollY, { stiffness, damping })` entrega a mesma sensação de lerp com física configurável em vez do fator manual, aplicado a um `useTransform` ligado ao transform do wrapper.

---

## Padrões de seção (pin, trilho horizontal, capítulo)

### Pin com Troca de Conteúdo

Uma seção alta fica presa na tela (`position: sticky`) enquanto o usuário rola; dentro dela, blocos de texto trocam de estado via crossfade de opacidade conforme a posição de scroll avança por etapas, cada etapa disparada por um `IntersectionObserver` num trigger invisível. É o padrão clássico das páginas de produto Apple, onde a imagem fica parada e o texto ao redor muda em capítulos.

Quando usar: storytelling em 3 a 5 etapas sobre um único produto ou conceito, sem trocar de tela; ideal em hero estendido ou seção de features onde cada etapa merece atenção total antes de passar pra próxima.

```html
<section class="pin" style="--steps:4">
  <div class="pin__sticky">
    <div id="visual" class="pin__visual" data-active="0">
      <div class="pin__content" data-step="0">Conteúdo da etapa 1</div>
      <div class="pin__content" data-step="1">Conteúdo da etapa 2</div>
      <div class="pin__content" data-step="2">Conteúdo da etapa 3</div>
      <div class="pin__content" data-step="3">Conteúdo da etapa 4</div>
    </div>
  </div>
  <div class="pin__triggers">
    <div class="pin__trigger" data-content="0"></div>
    <div class="pin__trigger" data-content="1"></div>
    <div class="pin__trigger" data-content="2"></div>
    <div class="pin__trigger" data-content="3"></div>
  </div>
</section>

<style>
/* altura explícita = steps x altura de viewport, senão não há distância de scroll pro pin */
.pin {
  position: relative;
  height: calc(var(--steps) * 100vh);
  height: calc(var(--steps) * 100dvh); /* fallback progressivo pra mobile */
}
.pin__sticky {
  position: sticky;
  top: 0;
  height: 100vh;
  height: 100dvh;
  display: grid;
  place-items: center;
  overflow: hidden;
}
.pin__triggers {
  position: absolute;
  inset: 0;
  display: grid;
  grid-template-rows: repeat(var(--steps), 100vh);
  pointer-events: none; /* não bloqueia clique/hover no conteúdo do visual */
}

/* o crossfade real entre etapas */
.pin__visual { position: relative; width: 100%; height: 100%; }
.pin__content {
  position: absolute;
  inset: 0;
  display: grid;
  place-items: center;
  opacity: 0;
  transition: opacity .5s ease;
}
.pin__visual[data-active="0"] .pin__content[data-step="0"],
.pin__visual[data-active="1"] .pin__content[data-step="1"],
.pin__visual[data-active="2"] .pin__content[data-step="2"],
.pin__visual[data-active="3"] .pin__content[data-step="3"] {
  opacity: 1;
}

@media (prefers-reduced-motion: reduce) {
  .pin__content { transition: none; }
}
</style>

<script>
// um observer único troca o dataset ativo por etapa
const visual = document.getElementById('visual');
const io = new IntersectionObserver(entries => {
  entries.forEach(e => {
    if (e.isIntersecting) visual.dataset.active = e.target.dataset.content;
  });
}, { threshold: 0.5 });
document.querySelectorAll('.pin__trigger').forEach(t => io.observe(t));
</script>
```

Armadilhas: a altura total da seção precisa ser proporcional ao número de etapas (`steps` vezes 100vh), senão não há distância de scroll suficiente para trocar tudo. Threshold mal calibrado troca a etapa tarde demais ou duas vezes seguidas. Anime só o conteúdo interno via opacidade, nunca o próprio elemento sticky (padding, top). Slop a evitar: usar esse padrão para navegação principal do site, ele é para storytelling pontual.

Fonte: padrão confirmado em apple.com/mac-mini e documentado em artigos sobre a estrutura de páginas de produto Apple.

Variante Framer: `const { scrollYProgress } = useScroll({ target: ref, offset: ['start start','end end'] }); const step = useTransform(scrollYProgress, [0,.33,.66,1], [0,1,2,3]);`

### Trilho Horizontal Pinado

Uma section fica presa verticalmente via `position: sticky` enquanto um trilho interno de itens desliza horizontalmente (`translateX`) em sincronia com o progresso de scroll vertical, via rAF ligado e desligado por `IntersectionObserver`. É o efeito do `ScrollTrigger` horizontal do GSAP, aqui reimplementado sem lib.

Quando usar: showcase de projetos ou produtos, timeline editorial, galeria com poucos itens (3 a 5). Nunca como navegação principal do site.

```html
<section class="h-rail">
  <div class="h-rail__sticky">
    <div class="h-rail__track">
      <div class="h-rail__item">...</div>
      <div class="h-rail__item">...</div>
      <div class="h-rail__item">...</div>
    </div>
  </div>
</section>
```

```css
.h-rail { height: 400vh; position: relative; }
.h-rail__sticky { position: sticky; top: 0; height: 100vh; overflow: hidden; }
.h-rail__track { display: flex; height: 100%; width: max-content; will-change: transform; }
.h-rail__item { width: 100vw; flex-shrink: 0; }

/* fallback obrigatório: usuário pediu menos movimento, vira lista vertical normal */
@media (prefers-reduced-motion: reduce) {
  .h-rail { height: auto; }
  .h-rail__sticky { position: static; height: auto; overflow: visible; }
  .h-rail__track { display: block; width: auto; will-change: auto; }
  .h-rail__item { width: 100%; }
}
```

```js
// liga translateX ao progresso vertical da section, IO liga/desliga o rAF
const prefersReducedMotion = matchMedia('(prefers-reduced-motion: reduce)').matches;

if (!prefersReducedMotion) {
  const section = document.querySelector('.h-rail');
  const track = document.querySelector('.h-rail__track');
  let active = false;
  let rafId = null;

  function tick() {
    if (!active) { rafId = null; return; }
    const r = section.getBoundingClientRect();
    const total = r.height - innerHeight;
    const maxX = track.scrollWidth - innerWidth;
    if (total > 0 && maxX > 0) {
      const p = Math.min(1, Math.max(0, -r.top / total));
      track.style.transform = `translate3d(${-p * maxX}px,0,0)`;
    }
    rafId = requestAnimationFrame(tick);
  }

  new IntersectionObserver(([e]) => {
    active = e.isIntersecting;
    if (active && rafId === null) rafId = requestAnimationFrame(tick);
  }, { threshold: 0 }).observe(section);
}
```

Armadilhas: a altura da section precisa ser proporcional ao número de itens (N vezes 100vh), senão o scroll acaba antes ou depois do trilho terminar. Sem `will-change: transform` o movimento pode travar em mobile, mas aplicar em elementos que nunca mudam desperdiça memória de GPU, use com moderação. Testar sempre em trackpad e touch para garantir que o gesto de scroll continua natural. Reserve esse padrão para conteúdo secundário, nunca para a navegação principal.

Fonte: gsap.com/docs (ScrollTrigger horizontal com pin), codepen.io/GreenSock.

Variante Framer: `const { scrollYProgress } = useScroll({ target: ref }); const x = useTransform(scrollYProgress, [0,1], ['0%','-75%']); <motion.div style={{ x }} className='h-rail__track' />`

### Transição de capítulo em wipe

Seções full-bleed empilhadas com `position: sticky`; a seção seguinte entra cobrindo a anterior com um `clip-path` animado (de escondida a totalmente visível), sincronizado ao scroll via `animation-timeline: view()`, criando a sensação de virar de capítulo em vez de rolar uma página comum.

Quando usar: divisão entre grandes blocos temáticos de uma LP (do hero pras features, das features pra prova social) quando se quer um corte marcante em vez de scroll contínuo.

```html
<section class="chapter">...</section>
<section class="chapter">...</section>
```

```css
.chapter{position:sticky;top:0;height:100vh;overflow:hidden}
.chapter+.chapter{clip-path:inset(0 0 100% 0)}
@supports (animation-timeline:view()){
  .chapter+.chapter{
    animation:wipe-in linear both;
    animation-timeline:view();
    animation-range:entry 0% cover 40%;
  }
  @keyframes wipe-in{to{clip-path:inset(0 0 0% 0)}}
}
@media (prefers-reduced-motion:reduce){.chapter+.chapter{clip-path:none;animation:none}}
```

```js
// fallback pra Firefox e navegadores sem animation-timeline:view()
if(!CSS.supports('animation-timeline','view()')){
  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  document.querySelectorAll('.chapter+.chapter').forEach(function(ch){
    if(reduceMotion){
      ch.style.clipPath = 'inset(0 0 0% 0)';
      return;
    }
    ch.style.transition = 'clip-path .6s ease';
    new IntersectionObserver(function(entries){
      var e = entries[0];
      ch.style.clipPath = e.isIntersecting ? 'inset(0 0 0% 0)' : 'inset(0 0 100% 0)';
    }, {threshold:.15}).observe(ch);
  });
}
```

Armadilhas: todas as seções precisam do mesmo stacking context (`position: sticky`, `top: 0`) dentro de um contêiner comum, senão o wipe não sobrepõe corretamente. `animation-range` mal calibrado faz a próxima seção cobrir a anterior cedo demais, escondendo texto que o usuário ainda não terminou de ler. Sempre ter fallback com `IntersectionObserver` e transition CSS pro Firefox, que ainda não suporta `animation-timeline: view()`.

Fonte: Builder.io, Create Apple-style scroll animations with CSS view-timeline.
