# Texto e Cursor Premium (`motion-texto-cursor`)

Leia este arquivo quando for animar a entrada de uma headline, destacar uma palavra chave dentro de um título, ou desenhar o hover de um card, botão ou link. Ele reúne o repertório vanilla (HTML/CSS/JS puro, sem lib) para texto em movimento e para a resposta de cursor da peça, sempre com fallback de `prefers-reduced-motion` e variante em Framer Motion quando o projeto já é React.

## Índice

| Receita | Quando usar |
|---|---|
| Cortina de Texto (Mask Entry) | Headline de hero e títulos de seção que precisam entrar com peso |
| Leitura Guiada por Scroll | Parágrafo de manifesto ou sobre, iluminado palavra a palavra pelo scroll |
| Texto que Acende ao Rolar | Bloco de texto longo tipo página de especificação, estilo Apple |
| Revelação de Texto por Palavra | Headline ou manifesto que precisa nascer palavra a palavra conforme rola |
| Jitter Sutil em Stagger de Texto | Título ou lista curta que precisa fugir do stagger perfeito de template |
| Texto Decodificado (Scramble Reveal) | Palavra chave de destaque ou métrica isolada, nunca bloco corrido |
| Microcopy de Erro que Ensina + Tremor Contido | Validação de campo de formulário |
| Boop (resposta tátil no hover) | Ícones, botões secundários, itens de navegação |
| Botão que Respira | Qualquer CTA, botão primário/secundário ou ícone clicável |
| Spotlight que Segue o Cursor | Cards de feature, pricing, botão grande de destaque |
| Wipe de Revelação (Clip-Path no Hover) | Item de lista de projeto, link "ver mais", card único de destaque |
| Magnetismo Sutil (pull contido) | CTA principal, ícones de navegação ou redes sociais |
| Morph de Ícone no Hover | Botão de ação com estado alternável (favoritar, expandir, menu) |

## Efeitos de texto

### Cortina de Texto (Mask Entry)

Cada linha do título fica dentro de um contêiner com `overflow: hidden`, o texto nasce deslocado para baixo e desliza até a posição natural com atraso escalonado por linha, criando uma revelação tipo cortina em vez de um fade genérico. Duas receitas equivalentes da mesma família (Cortina de Linha e Máscara de Linha) foram fundidas nesta ficha: a versão abaixo usa progressive enhancement, o texto só fica escondido se o JS confirmou que vai animar, e escopa o índice do stagger por bloco, então funciona mesmo com vários títulos animados na mesma página.

Quando usar: headline de hero, títulos de seção ao entrarem na viewport, subtítulos curtos. Evite em parágrafos longos, o efeito é para tipografia protagonista, não para corpo de texto.

```html
<!-- coloque este script o mais cedo possível no <head>, antes do <body>,
     para evitar flash de conteúdo já visível sendo escondido depois -->
<script>document.documentElement.classList.add('js-anim');</script>

<h1 class="reveal">
  <span class="line-mask"><span class="line-inner">Primeira linha do título</span></span>
  <span class="line-mask"><span class="line-inner">Segunda linha do título</span></span>
</h1>
```

```css
.line-mask { display: block; overflow: hidden; }
.line-inner {
  display: block;
  transition: transform .9s cubic-bezier(.19,1,.22,1);
  transition-delay: calc(var(--i, 0) * 80ms);
}
/* o estado "escondido" só existe se o JS confirmou que vai animar */
.js-anim .line-inner { transform: translateY(110%); }
.js-anim .reveal.is-visible .line-inner { transform: translateY(0); }

@media (prefers-reduced-motion: reduce) {
  .js-anim .line-inner { transition: none; transform: none; }
}
```

```js
// índice escopado por bloco .reveal, não global: corrige o stagger
// quando a técnica é usada em mais de um lugar da página (hero + seções)
document.querySelectorAll('.reveal').forEach(reveal => {
  reveal.querySelectorAll('.line-mask').forEach((el, i) => {
    el.style.setProperty('--i', i);
  });
});

const io = new IntersectionObserver((entries) => {
  entries.forEach(e => {
    if (e.isIntersecting) {
      e.target.classList.add('is-visible');
      io.unobserve(e.target);
    }
  });
}, { threshold: .4 });

document.querySelectorAll('.reveal').forEach(el => io.observe(el));
```

Armadilhas: esquecer `overflow: hidden` no `.line-mask` faz a linha vazar antes de entrar. Delay maior que 100ms por linha em headline de 4 ou mais linhas fica lento e teatral, sinal de slop. `overflow: hidden` mal calculado corta descendentes de letras acentuadas (ç, ã) se o `line-height` for justo, dê folga vertical. Nunca esconda o texto por padrão sem o fallback: a técnica acima só aplica `translateY` quando a classe `js-anim` existe no `<html>`, então sem JS o título continua legível. Para headline responsiva cujo número de linhas muda entre mobile e desktop, não dá para confiar em quebra manual, trave a largura ou o tamanho da fonte para garantir a contagem de linhas, ou trate o título inteiro como um único `.line-mask` sem stagger por linha.

Fonte: https://blog.olivierlarose.com/tutorials/text-mask-animation e https://tympanus.net/codrops/2025/05/14/from-splittext-to-morphsvg-5-creative-demos-using-free-gsap-plugins/

Variante Framer: `const { ref, inView } = useInView({ threshold: .4 }); <motion.span variants={{hidden:{y:'110%'},show:{y:0}}} initial="hidden" animate={inView?'show':'hidden'} transition={{delay:i*.08, ease:[.19,1,.22,1]}} />`

### Leitura Guiada por Scroll

Um parágrafo é dividido em palavras e cada palavra recebe uma fatia própria do progresso de scroll do bloco, ganhando opacidade conforme o usuário rola. O texto se ilumina no ritmo do scroll, não do tempo.

Quando usar: bloco de manifesto ou sobre, parágrafo de destaque entre seções, texto editorial curto. Evite em blocos com mais de 40 palavras.

```js
function clamp(v, min, max) {
  return Math.max(min, Math.min(max, v));
}

function wrapWords(el) {
  el.innerHTML = el.textContent.trim().split(/\s+/)
    .map(w => `<span class="w">${w}</span>`).join(' ');
}

function initLeituraGuiada(el) {
  const prefersReduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const cssDrivesIt = window.CSS && CSS.supports && CSS.supports('animation-timeline: view()');

  wrapWords(el);

  // reduced motion ou CSS scroll-timeline nativo: nenhum JS de scroll é necessário
  if (prefersReduced || cssDrivesIt) return;

  const words = el.querySelectorAll('.w');
  let ticking = false;

  function update() {
    const r = el.getBoundingClientRect();
    const total = r.height + innerHeight * 0.6;
    const progress = clamp((innerHeight * 0.8 - r.top) / total, 0, 1);
    words.forEach((w, i) => {
      const start = i / words.length;
      const end = start + 1 / words.length;
      const p = clamp((progress - start) / (end - start), 0, 1);
      w.style.opacity = 0.25 + p * 0.75;
    });
    ticking = false;
  }

  function onScroll() {
    if (!ticking) {
      requestAnimationFrame(update);
      ticking = true;
    }
  }

  // só escuta scroll enquanto o bloco está perto da viewport (evita custo global)
  const io = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        window.addEventListener('scroll', onScroll, { passive: true });
        update();
      } else {
        window.removeEventListener('scroll', onScroll);
      }
    });
  }, { rootMargin: '60% 0px 60% 0px' });

  io.observe(el);
}

document.querySelectorAll('.leitura-guiada').forEach(initLeituraGuiada);
```

```css
.leitura-guiada .w { opacity: .25; }

@supports (animation-timeline: view()) {
  .leitura-guiada .w {
    animation: reveal linear both;
    animation-timeline: view();
    animation-range: entry 10% cover 50%;
  }
  @keyframes reveal { from { opacity: .25 } to { opacity: 1 } }
}

@media (prefers-reduced-motion: reduce) {
  .leitura-guiada .w {
    opacity: 1 !important;
    animation: none !important;
  }
}
```

Armadilhas: recalcular `getBoundingClientRect` a cada frame sem cache prejudica performance em textos longos. Deixar o piso de opacidade em 0 torna o texto ilegível e falha em contraste, mantenha o piso em .25 como no código acima. Aplicar em blocos com mais de 40 palavras vira caça ao tesouro e frustra quem só quer ler.

Fonte: https://blog.olivierlarose.com/tutorials/text-gradient-opacity-on-scroll

### Texto que Acende ao Rolar

Cada linha de um parágrafo nasce apagada e acende para opacidade total conforme cruza uma faixa de gatilho na tela durante o scroll, criando leitura progressiva. É o efeito das páginas de chip e performance da Apple, onde o texto parece se iluminar frase por frase. Diferente da Leitura Guiada por Scroll, que trabalha por palavra com gradiente contínuo cobrindo todo o percurso do bloco, aqui a unidade é a linha inteira e o aceso é mais binário, ligado a uma faixa de entrada e cobertura definida em `animation-range`.

Quando usar: blocos de texto longos ou declarações de propósito que precisam ser lidos com ritmo controlado pelo scroll, não tudo de uma vez. Bom para seção de princípios ou de especificações técnicas.

```html
<style>
.ignite .line {
  opacity: .25;
  transition: opacity .3s linear;
}
@supports (animation-timeline: view()) {
  .ignite .line {
    animation: acende linear both;
    animation-timeline: view();
    animation-range: entry 10% cover 40%;
  }
  @keyframes acende {
    to { opacity: 1; }
  }
}
@media (prefers-reduced-motion: reduce) {
  .ignite .line {
    opacity: 1 !important;
    animation: none !important;
    transition: none !important;
  }
}
</style>

<script>
// fallback para navegadores sem suporte a animation-timeline: view()
// (ex: Firefox em versões sem a feature). Não roda se reduced-motion
// estiver ativo, já que o CSS acima já força opacity: 1 nesse caso.
if (
  !CSS.supports('animation-timeline', 'view()') &&
  !window.matchMedia('(prefers-reduced-motion: reduce)').matches
) {
  const linhas = document.querySelectorAll('.ignite .line');
  const io = new IntersectionObserver(entries => {
    entries.forEach(e => {
      e.target.style.opacity = e.isIntersecting ? '1' : '.25';
    });
  }, { rootMargin: '-40% 0px -40% 0px' });
  linhas.forEach(l => io.observe(l));
}
</script>
```

Armadilhas: sem o bloco de `prefers-reduced-motion`, o texto fica preso em opacidade baixa para quem desativa animação, quebrando legibilidade, sempre force `opacity: 1`. `animation-timeline: view()` ainda não roda em todo o Firefox, cheque com `@supports`. Faixa de `animation-range` mal calibrada faz o texto acender cedo ou tarde demais, ajuste testando ao vivo.

Fonte: https://www.builder.io/blog/view-timeline (Builder.io, "Create Apple-style scroll animations with CSS view-timeline")

### Revelação de Texto por Palavra

Título ou parágrafo que revela palavra a palavra conforme o próprio scroll avança, não só ao entrar na tela, dando à tipografia o papel de protagonista sem depender de imagem. Cada palavra usa uma fatia do mesmo `view-timeline` compartilhado pelo contêiner, definida por um índice (`--i`) e o total de palavras (`--n`) setados via JS, o que produz o efeito cascata só com CSS. Duas receitas equivalentes da mesma família (Cascata de Palavras por Linha ao Rolar e Revelação de Texto por Palavra) foram fundidas nesta ficha, ficando com a versão que tem fallback JS completo para navegadores sem suporte a `animation-timeline`.

Quando usar: headline de hero, manifesto ou seção de posicionamento, blocos de texto longos que precisam de ritmo de leitura controlado. Usar com moderação, no máximo 1 a 2 vezes por página.

```html
<!-- envolva o título ou parágrafo alvo com class="reveal-line" -->
<h1 class="reveal-line">Palavra a palavra a cascata acontece aqui</h1>
```

```css
.reveal-line {
  view-timeline-name: --line-reveal;
  view-timeline-axis: block;
}

.reveal-word {
  opacity: .15;
  animation: word-in linear both;
  animation-timeline: --line-reveal;
  /* cada palavra usa uma fatia diferente do mesmo timeline do container,
     definida por --i (índice) e --n (total), setados via JS no style inline */
  animation-range: calc(var(--i, 0) / var(--n, 1) * 60%)
                    calc(var(--i, 0) / var(--n, 1) * 60% + 40%);
}
@keyframes word-in { to { opacity: 1; } }

/* fallback: nenhuma animation aqui, só transição controlada por classe */
.reveal-word.js-fallback {
  animation: none;
  transition: opacity .5s ease;
}
.reveal-word.js-fallback.is-visible {
  opacity: 1;
}

@media (prefers-reduced-motion: reduce) {
  .reveal-word { animation: none; transition: none; opacity: 1; }
}
```

```js
document.querySelectorAll('.reveal-line').forEach((el) => {
  const original = el.textContent.trim();
  const words = original.split(/\s+/);

  el.setAttribute('aria-label', original);
  el.innerHTML = words
    .map((w, i) => `<span class="reveal-word" style="--i:${i};--n:${words.length}" aria-hidden="true">${w}</span>`)
    .join(' ');

  const spans = [...el.querySelectorAll('.reveal-word')];
  const supportsScrollTimeline = CSS.supports('animation-timeline: view()');
  const reduceMotion = matchMedia('(prefers-reduced-motion: reduce)').matches;

  if (supportsScrollTimeline || reduceMotion) return;

  spans.forEach((s) => s.classList.add('js-fallback'));
  const io = new IntersectionObserver(([entry]) => {
    if (!entry.isIntersecting) return;
    spans.forEach((w, i) => setTimeout(() => w.classList.add('is-visible'), i * 35));
    io.unobserve(el);
  }, { threshold: 0.4 });
  io.observe(el);
});
```

Armadilhas: quebrar o texto em spans sem cuidado de acessibilidade faz leitor de tela ler palavra por palavra fora de contexto, sempre coloque o texto completo num `aria-label` no elemento pai e `aria-hidden="true"` nos spans internos, como no JS acima. Aplicar `animation-timeline: view()` direto em cada span, sem um timeline nomeado compartilhado no contêiner, faz as palavras da mesma linha revelarem todas juntas em vez de uma a uma, é por isso que o `view-timeline-name` vive no `.reveal-line`, não no `.reveal-word`. Stagger rápido demais, menos de 20ms, fica ilegível e estroboscópico. Em headlines com muitas palavras, o `animation-range` pode ultrapassar 100%, limite a técnica a títulos curtos ou reduza a fatia por palavra proporcionalmente à contagem de spans. Nunca use cor neon ou gradiente nas palavras junto do reveal, e não aplique em todo parágrafo do site, perde a exclusividade e vira tique visual.

Fonte: https://magicui.design/docs/components/text-reveal e https://magicui.design/docs/components/text-animate

Variante Framer: `const { scrollYProgress } = useScroll({ target: ref, offset: ['start 0.9','start 0.25'] }); {words.map((w,i) => <motion.span style={{ opacity: useTransform(scrollYProgress, [i/words.length,(i+1)/words.length], [0.15,1]) }}>{w}</motion.span>)}`

### Jitter Sutil em Stagger de Texto

Injetar pequenas variações aleatórias de delay e deslocamento em cada item de uma sequência animada, para fugir do stagger perfeitamente sincronizado que parece gerado por template.

Quando usar: reveal de linhas ou palavras de um título protagonista entrando na tela, lista curta de itens. Qualquer lugar onde elementos entrariam em fila perfeita demais e sinalizariam origem genérica.

**Dose:** no máximo 1 por página, em palavra ou rótulo, nunca em bloco de texto.

```js
function staggerReveal(items, { baseDelay = 60, jitter = 30 } = {}) {
  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  items.forEach((el, i) => {
    if (reduceMotion) return; // a regra @media abaixo cuida do estado final
    const delay = Math.max(i * baseDelay + (Math.random() * jitter - jitter / 2), 0);
    const drift = 8 + Math.random() * 6; // 8 a 14px, nunca idêntico
    el.style.setProperty('--delay', `${delay}ms`);
    el.style.setProperty('--drift', `${drift}px`);
  });
}

// .reveal-group envolve o conjunto (título ou lista); dispara tudo junto quando entra na tela
const wrapper = document.querySelector('.reveal-group');
const items = wrapper.querySelectorAll('.reveal-word');
staggerReveal(items);

const io = new IntersectionObserver((entries, obs) => {
  if (entries[0].isIntersecting) {
    wrapper.classList.add('is-visible');
    obs.disconnect();
  }
}, { threshold: 0.3 });
io.observe(wrapper);
```

```css
.reveal-word {
  opacity: 0;
  transform: translateY(var(--drift, 10px));
  animation: word-in 500ms var(--spring, ease-out) var(--delay, 0ms) forwards;
  animation-play-state: paused; /* fica parado até o wrapper entrar na viewport */
}
.reveal-group.is-visible .reveal-word {
  animation-play-state: running;
}
@keyframes word-in {
  to { opacity: 1; transform: translateY(0); }
}
@media (prefers-reduced-motion: reduce) {
  .reveal-word {
    animation: none !important;
    opacity: 1 !important;
    transform: none !important;
  }
}
```

Armadilhas: aleatoriedade demais destrói a leitura de hierarquia, mantenha a variação numa faixa pequena, delay base mais ou menos 30 a 40ms, nunca centenas. `Math.random()` sem seed gera resultado diferente a cada reload, aceitável para decoração mas evite se precisar de reprodução exata em teste visual. Nunca aplique jitter em CTA ou elemento de ação, ali o usuário espera resposta previsível e imediata. O objetivo é orgânico, não caótico, se exagerar vira bagunça em vez de sutileza.

Fonte: https://www.joshwcomeau.com/blog/whimsical-animations/

### Texto Decodificado (Scramble Reveal)

No hover, ou no disparo por `IntersectionObserver` quando o elemento entra na viewport, o texto se decompõe em caracteres aleatórios e vai sendo decodificado letra por letra, da esquerda para a direita, até revelar o texto final. É a técnica clássica popularizada pelo Hyperplexed no efeito "Hacked Text".

Quando usar: em uma palavra chave dentro de um headline, um rótulo de navegação, ou um número ou métrica de destaque. Nunca em blocos de texto corrido nem no headline inteiro, o efeito precisa ficar pontual para não virar estética hacker genérica.

**Dose:** no máximo 1 por página, em palavra ou rótulo, nunca em bloco de texto.

```html
<!-- <span class="scramble" data-value="Impacto real" data-trigger="hover">Impacto real</span>
     <span class="scramble" data-value="128 empresas" data-trigger="view">128 empresas</span>
     coloque o script no fim do body, ou dentro de DOMContentLoaded -->
```

```css
.scramble { display: inline-block; }
```

```js
const CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
const reduceMotionQuery = matchMedia('(prefers-reduced-motion: reduce)');

function makeScramble(el) {
  const final = el.dataset.value;
  let frame = null;
  let iter = 0;

  return function play() {
    // lê .matches no momento do disparo, não uma vez só no load do script
    if (reduceMotionQuery.matches) {
      el.textContent = final;
      return;
    }
    clearInterval(frame);
    iter = 0;
    // trava a largura atual para evitar CLS enquanto os caracteres trocam de tamanho
    el.style.minWidth = el.getBoundingClientRect().width + 'px';

    frame = setInterval(() => {
      el.textContent = final.split('').map((ch, i) => {
        if (ch === ' ') return ' ';
        if (i < iter) return final[i];
        return CHARS[Math.floor(Math.random() * CHARS.length)];
      }).join('');
      if (iter >= final.length) {
        clearInterval(frame);
        el.style.minWidth = ''; // libera a largura depois de revelado
      }
      iter += 1 / 3;
    }, 35);
  };
}

// gatilho 1: hover (palavra dentro de headline, rótulo de nav)
document.querySelectorAll('.scramble[data-trigger="hover"]').forEach(el => {
  el.addEventListener('mouseenter', makeScramble(el));
});

// gatilho 2: entrada em viewport (número ou métrica de destaque)
document.querySelectorAll('.scramble[data-trigger="view"]').forEach(el => {
  const play = makeScramble(el);
  const observer = new IntersectionObserver((entries, obs) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        play();
        obs.unobserve(entry.target); // dispara só uma vez, nunca em loop
      }
    });
  }, { threshold: 0.6 });
  observer.observe(el);
});
```

Armadilhas: charset com símbolos tipo `!@#$%&*` remete a estética cyberpunk barata, use só letras maiúsculas ou um charset neutro. Rodar em loop automático ou aplicar em bloco grande de texto vira gimmick, dispare só uma vez por hover ou entrada em viewport. Sem largura mínima reservada o texto pode oscilar de largura durante a decodificação, o `minWidth` travado no código acima resolve isso. Sempre cheque `prefers-reduced-motion` e, se ativo, aplique o texto final direto sem animar.

Fonte: CodePen Hyperplexed, "Hacked Text Effect" (https://codepen.io/Hyperplexed/pen/rNrJgrd)

Variante Framer: em React, o mesmo loop de `setInterval` funciona dentro de um `useEffect` atualizando um `useState` com o texto atual, ou use `motion.span` por caractere com `AnimatePresence` para uma versão mais spring.

### Microcopy de Erro que Ensina + Tremor Contido

A mensagem de erro nomeia o campo e a regra específica que falhou (por exemplo "a senha precisa de pelo menos 8 caracteres") em vez de um genérico "campo inválido". O texto é o canal principal do feedback, um tremor horizontal curto (400ms, poucos pixels, oscilações decrescentes) reforça o momento em que o erro aparece, mas nunca é contínuo nem é a única pista.

Quando usar: no exato instante em que um campo falha validação, no blur ou no submit. Use o tremor só na transição de válido para inválido, nunca repita a cada nova tentativa de digitação enquanto o campo já está marcado como erro.

```css
.input.is-invalid { border-color: var(--accent-error, #C0392B); }

@keyframes field-shake {
  10%, 90% { transform: translateX(-1px); }
  20%, 80% { transform: translateX(2px); }
  30%, 50%, 70% { transform: translateX(-4px); }
  40%, 60% { transform: translateX(4px); }
}

.input.is-shaking { animation: field-shake 400ms cubic-bezier(.36,.07,.19,.97); }

@media (prefers-reduced-motion: reduce) {
  .input.is-shaking { animation: none; }
}
```

```js
const ERROR_COPY = {
  email: 'Digite um email válido, tipo nome@empresa.com',
  password: 'A senha precisa de pelo menos 8 caracteres',
};

function setFieldError(input, msgEl, fieldName) {
  const wasInvalid = input.classList.contains('is-invalid');

  msgEl.textContent = ERROR_COPY[fieldName] ?? 'Confira este campo antes de continuar';
  msgEl.setAttribute('role', 'alert');
  input.classList.add('is-invalid');
  input.setAttribute('aria-invalid', 'true');

  // dispara o tremor só na transição válido -> inválido, nunca em repetição
  // enquanto o campo já estiver marcado como erro
  if (!wasInvalid) {
    input.classList.remove('is-shaking');
    void input.offsetWidth; // força reflow para permitir reiniciar a animação depois
    input.classList.add('is-shaking');
  }
}

function clearFieldError(input, msgEl) {
  input.classList.remove('is-invalid', 'is-shaking');
  input.removeAttribute('aria-invalid');
  msgEl.textContent = '';
}

document.querySelectorAll('.input').forEach((input) => {
  input.addEventListener('animationend', () => input.classList.remove('is-shaking'));
});

// exemplo de uso: validar no blur, nunca a cada tecla digitada
document.querySelectorAll('.input[data-field]').forEach((input) => {
  const msgEl = document.querySelector(`[data-error-for="${input.dataset.field}"]`);
  input.addEventListener('blur', () => {
    const isValid = input.checkValidity(); // ou sua regra custom
    if (!isValid) {
      setFieldError(input, msgEl, input.dataset.field);
    } else {
      clearFieldError(input, msgEl);
    }
  });
});
```

Armadilhas: shake repetido a cada tentativa de submit com o mesmo erro fica irritante rápido, dispare só na transição de estado, o `wasInvalid` no código acima cuida disso. Shake como único sinal falha para quem usa `prefers-reduced-motion` ou tem baixa visão, o texto sempre precisa carregar a informação sozinho, por isso `role="alert"` e `aria-invalid` no input. Mensagem genérica tipo "erro" ou "inválido" não ensina nada e força o usuário a adivinhar a regra de novo. Use um tom terroso e dessaturado na cor de erro, nunca vermelho puro de formulário genérico, para não competir com o único acento de cor da peça.

Fonte: animationpatterns.art, "CSS Error Shake Feedback with Reduced Motion"

## Cursor e hover

### Boop (resposta tátil no hover)

Microtransformação (scale, rotate, translate) que dispara no `mouseenter` e se desfaz sozinha depois de um tempo fixo, independente do cursor continuar em cima. É como uma máquina que se desliga sozinha: um pico de movimento controlado, não um hover state permanente.

Quando usar: ícones, botões secundários, itens de navegação, qualquer elemento pequeno que deve reagir ao toque do cursor com personalidade sem virar decoração contínua. Bom lugar para concentrar o único acento de cor da peça.

```js
function attachBoop(el, { scale = 1.1, rotate = 8, timing = 180 } = {}) {
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (reduce) return;

  const computed = getComputedStyle(el).transform;
  const base = computed && computed !== 'none' ? computed : '';

  el.style.transition = `transform ${timing}ms var(--spring, ease-out)`;
  let timeoutId;

  el.addEventListener('pointerenter', () => {
    clearTimeout(timeoutId);
    el.style.transform = `${base} scale(${scale}) rotate(${rotate}deg)`.trim();
    timeoutId = setTimeout(() => {
      el.style.transform = base;
    }, timing);
  });
}

document.querySelectorAll('[data-boop]').forEach(el => attachBoop(el));
```

Armadilhas: nunca dispare no `:focus`, é um efeito puramente decorativo e atrapalha quem navega por teclado, o outline de foco já dá o feedback necessário, use apenas `pointerenter` ou `mouseenter`. Sempre cheque `prefers-reduced-motion` e saia cedo da função se o usuário preferir menos movimento. Exagerar em rotação ou escala vira estética de jogo casual, fique em rotação de 5 a 15 graus e escala de 1.05 a 1.15. Se o elemento já usa `transform` para posicionamento ou ainda carrega um transform residual de outra animação, capture o transform base via `getComputedStyle` antes de aplicar o boop, como no código acima, e restaure esse base, não uma string vazia, ao final, senão o boop reseta ou desloca o elemento. Aplicar boop em todos os elementos da página cansa rápido, reserve para 1 ou 2 pontos de interação por seção.

Fonte: https://www.joshwcomeau.com/react/boop/

Variante Framer: `whileHover={{ scale: 1.1, rotate: 8 }} transition={{ type: "spring", stiffness: 300, damping: 10 }}`

### Botão que Respira

Feedback tátil mínimo mas essencial: o botão encolhe levemente ao ser pressionado, imitando um botão físico. É a microinteração mais barata e mais eficaz para uma interface parecer premium, mesmo sem nenhum outro efeito visual.

Quando usar: em qualquer CTA, botão primário ou secundário, ou ícone clicável da peça.

```css
.botao {
  transition: transform 140ms cubic-bezier(0.23,1,0.32,1),
              background-color 150ms ease;
  will-change: transform;
}
.botao:active {
  transform: scale(0.97);
}
@media (hover: hover) and (pointer: fine) {
  .botao:hover { background-color: var(--acento-hover, currentColor); }
}
@media (prefers-reduced-motion: reduce) {
  .botao { transition: background-color 150ms ease; }
  .botao:active { transform: none; }
}
```

Armadilhas: aplicar scale menor que 0.9 faz o botão parecer quebrado, mantenha entre 0.95 e 0.98. Colocar hover de scale sem o media query `hover: hover` deixa o estado grudado em toque no mobile, ficando ligado após o tap. Animar `box-shadow` grande junto do transform pode sair do compositor e engasgar em aparelhos fracos, prefira só transform e cor.

Fonte: https://emilkowal.ski/ui/7-practical-animation-tips

### Spotlight que Segue o Cursor

Um brilho radial sutil (`radial-gradient` de raio pequeno e opacidade baixa) que segue a posição do cursor dentro de um card ou botão, atualizado por CSS custom properties via JS, revelando a superfície como se fosse iluminada por uma fonte de luz pontual. É a aplicação tátil da lei de Fitts como feedback visual contínuo, e o efeito de hover mais reconhecível do site do Linear. Duas receitas equivalentes da mesma família (Spotlight que Segue o Cursor e Spotlight de Preenchimento em Card) foram fundidas nesta ficha, ficando com a versão que usa `requestAnimationFrame` para não travar em telas grandes e checa `(hover: hover) and (pointer: fine)` antes de anexar qualquer listener.

Quando usar: cards de feature, pricing ou painéis de configuração, botões primários grandes e superfícies de destaque, onde o hover precisa comunicar que aquilo é interativo sem badge, sem ícone extra, só luz. Pode ser aplicado a vários cards da mesma grade desde que a intensidade seja baixa, o problema do anti-slop não é o efeito em si, é usar composição e cor idênticas demais entre cards clones.

```css
.spotlight-card {
  position: relative;
  overflow: hidden;
  --x: 50%;
  --y: 50%;
  --spotlight-color: 255, 255, 255; /* troque para 10, 12, 15 em fundo off-white */
}
.spotlight-card::after {
  content: "";
  position: absolute;
  inset: 0;
  background: radial-gradient(240px circle at var(--x) var(--y),
    rgba(var(--spotlight-color), 0.08), transparent 70%);
  opacity: 0;
  transition: opacity 200ms ease;
  pointer-events: none;
}
.spotlight-card:hover::after {
  opacity: 1;
}

@media (prefers-reduced-motion: reduce) {
  .spotlight-card::after {
    display: none;
  }
}
```

```js
const prefersReducedMotion = matchMedia('(prefers-reduced-motion: reduce)').matches;
const hasFinePointer = matchMedia('(hover: hover) and (pointer: fine)').matches;

if (hasFinePointer && !prefersReducedMotion) {
  document.querySelectorAll('.spotlight-card').forEach((card) => {
    let raf = null;
    let lastEvent = null;

    card.addEventListener('pointermove', (e) => {
      lastEvent = e;
      if (raf) return;
      raf = requestAnimationFrame(() => {
        const r = card.getBoundingClientRect();
        card.style.setProperty('--x', `${lastEvent.clientX - r.left}px`);
        card.style.setProperty('--y', `${lastEvent.clientY - r.top}px`);
        raf = null;
      });
    });
  });
}
```

Armadilhas: atualizar a posição direto no evento sem `requestAnimationFrame` engasga em telas grandes, já resolvido acima com o throttle por `raf`. Raio grande, acima de 400px, ou opacidade alta, acima de 0.2, transforma o glow contido em "orb de gradiente", exatamente o que o DNA reprova, mantenha raio entre 250 e 350px e opacidade entre 0.10 e 0.18. Use apenas um acento de cor no `radial-gradient`, nunca multicor. Sempre `pointer-events: none` no pseudo elemento para não interceptar cliques. Sempre esconda o pseudo-elemento inteiro, não só a transição, em `prefers-reduced-motion: reduce`. Nunca anexe o listener em touch, cheque `(hover: hover) and (pointer: fine)` antes, como no código acima.

Fonte: https://rauno.me/craft/interaction-design e https://frontendmasters.com/blog/glowing-hover-effect/ (padrão do card linear.app, recriação em CodePen https://codepen.io/akella/pen/XWYrRmb)

Variante Framer: `const x = useMotionValue(0.5); const y = useMotionValue(0.5); <motion.div onMouseMove={(e) => { const r = e.currentTarget.getBoundingClientRect(); x.set(e.clientX - r.left); y.set(e.clientY - r.top); }} style={{ background: useMotionTemplate\`radial-gradient(240px at ${x}px ${y}px, rgba(255,255,255,.08), transparent 70%)\` }} />`

### Wipe de Revelação (Clip-Path no Hover)

Um card ou link revela uma camada (imagem, cor de destaque) deslizando de dentro para fora via `clip-path: inset()` animado por transição CSS pura, disparado no hover e no foco de teclado, como uma cortina que abre sem recortar o DOM.

Quando usar: item de lista de projetos, link "ver mais" ou card único de destaque onde a transição texto para imagem precisa carregar intenção, sem repetir o mesmo efeito em três cards clones ao mesmo tempo.

```html
<a class="reveal-card" href="#" style="display:block;position:relative">
  <span class="reveal-card__label">Ver projeto</span>
  <span class="reveal-card__layer" style="background:#0A0C0F"></span>
</a>
```

```css
.reveal-card { position: relative; overflow: hidden; }
.reveal-card__layer {
  position: absolute; inset: 0;
  clip-path: inset(0 100% 0 0);
  transition: clip-path .6s cubic-bezier(.65,0,.35,1);
}
.reveal-card:hover .reveal-card__layer,
.reveal-card:focus-visible .reveal-card__layer {
  clip-path: inset(0 0 0 0);
}
@media (prefers-reduced-motion: reduce) {
  .reveal-card__layer {
    transition: opacity .2s linear;
    clip-path: none;
    opacity: 0;
  }
  .reveal-card:hover .reveal-card__layer,
  .reveal-card:focus-visible .reveal-card__layer {
    opacity: 1;
  }
}
```

Armadilhas: combinar `clip-path` com `filter` ou `backdrop-filter` no mesmo elemento gera bugs de composição em Safari. Usar só `:hover` exclui teclado e touch, sempre pareie com `:focus-visible`, como no código acima. Wipe abrindo em menos de 300ms parece glitch em vez de intencional. Aplicar esse wipe simultaneamente em vários cards da mesma grade transforma a técnica no clichê dos três cards clones que o DNA proíbe, reserve para um elemento de destaque por vez.

Fonte: https://tympanus.net/codrops/2026/05/06/from-shader-uniforms-to-clip-path-wipes-how-gsap-drives-my-portfolio/

Variante Framer: `<motion.div className="layer" initial={{ clipPath:'inset(0 100% 0 0)' }} whileHover={{ clipPath:'inset(0 0% 0 0)' }} transition={{ duration:.6, ease:[.65,0,.35,1] }} />`

### Magnetismo Sutil (pull contido)

Um botão ou ícone se desloca poucos pixels em direção ao cursor quando ele entra na área do elemento, calculado como uma fração, nunca 1 para 1, da distância entre o cursor e o centro do elemento, e volta suavemente ao centro no `mouseleave`.

Quando usar: CTA principal, ícones de navegação ou redes sociais no rodapé. Usar em no máximo 1 ou 2 elementos de destaque por tela, se todo botão da página for magnético a microinteração deixa de ser conteúdo e vira ruído.

```js
const STRENGTH = 0.35; // fração do deslocamento, manter entre 0.2 e 0.4 para ficar contido
const canHover = matchMedia('(hover: hover) and (pointer: fine)').matches;
const reduceMotion = matchMedia('(prefers-reduced-motion: reduce)').matches;

if (canHover && !reduceMotion) {
  document.querySelectorAll('.magnetic').forEach(el => {
    el.addEventListener('mousemove', e => {
      const r = el.getBoundingClientRect();
      const dx = (e.clientX - r.left - r.width / 2) * STRENGTH;
      const dy = (e.clientY - r.top - r.height / 2) * STRENGTH;
      el.style.transform = `translate(${dx}px, ${dy}px)`;
    });
    el.addEventListener('mouseleave', () => {
      el.style.transform = 'translate(0, 0)';
    });
  });
}
```

```css
.magnetic {
  display: inline-block; /* obrigatório se a classe for aplicada num <a> ou <span> */
  transition: transform .25s cubic-bezier(.2,.8,.2,1);
  will-change: transform;
}
```

Armadilhas: multiplicador próximo de 1, deslocamento igual à distância real do cursor, faz o elemento grudar de forma exagerada, mantenha `STRENGTH` entre 0.2 e 0.4. Resete a posição no `mouseleave` sempre com transição suave, nunca instantâneo, senão quebra a ilusão. Não aplique em elementos grandes, cards ou seções inteiras, a técnica é feita para alvos pequenos como botões e ícones. O guard `canHover` acima evita anexar os listeners em touch, o que deixaria o elemento deslocado após um tap sem `mouseleave` correspondente. Um efeito ainda mais refinado move o texto interno numa fração menor que o contêiner, dois níveis de deslocamento, mas isso é opcional, o de um nível já cumpre o padrão Linear/Apple.

Fonte: https://en.inithtml.com/resources/magnetic-hover-effect-creating-cursor-attracted-buttons-with-vanilla-javascript/

Variante Framer: `useMotionValue` combinado com `useSpring` (stiffness alta, damping médio) atualizado no `onPointerMove` do elemento, resetando para 0,0 no `onPointerLeave`.

### Morph de Ícone no Hover

Troca de um path por outro no hover ou num toggle de estado (seta reta vira seta curva, mais vira x, play vira pause) sem lib de morph. O truque é ter dois desenhos com exatamente o mesmo número de comandos e pontos na mesma ordem, e animar o atributo `d` via `transition` em CSS, com fallback JS de interpolação numérica para navegadores que ainda não animam `d`.

Quando usar: botão de ação com estado alternável (favoritar, expandir e colapsar, menu hambúrguer), microinteração de cursor-hover que reforça a affordance sem empilhar dois ícones sobrepostos com opacity crossfade.

```html
<button class="morph-icon" type="button" aria-label="Alternar menu">
  <svg viewBox="0 0 24 24" width="24" height="24" aria-hidden="true">
    <path class="morph-icon__path" fill="none" stroke="var(--accent)" stroke-width="2"
          stroke-linecap="round"
          d="M12 5L12 19M5 12L19 12"/>
  </svg>
</button>
```

```css
.morph-icon {
  background: none;
  border: none;
  padding: 8px;
  cursor: pointer;
  line-height: 0;
}
.morph-icon__path {
  transition: d .3s cubic-bezier(.65,0,.35,1);
  d: path("M12 5L12 19M5 12L19 12"); /* "+" fechado: 2 subpaths, M+L */
}
.morph-icon:hover .morph-icon__path,
.morph-icon:focus-visible .morph-icon__path {
  d: path("M5 5L19 19M19 5L5 19"); /* mesmo tipo e mesma ordem de comandos, agora interpola de verdade */
}
@media (prefers-reduced-motion: reduce) {
  .morph-icon__path { transition: none; }
}
```

```js
(function () {
  var supportsCSSd = window.CSS && CSS.supports && CSS.supports('d', 'path("M0 0L1 1")');
  if (supportsCSSd) return; // navegador já anima "d" via CSS, JS não precisa entrar

  var reduceMotion = matchMedia('(prefers-reduced-motion: reduce)').matches;
  var DENTRO = "M12 5L12 19M5 12L19 12"; // "+"
  var FORA   = "M5 5L19 19M19 5L5 19";   // "x"

  function morph(el, dInicial, dFinal, duracaoMs) {
    duracaoMs = duracaoMs || 300;
    if (reduceMotion) { el.setAttribute('d', dFinal); return; }
    var nums = function (s) { return s.match(/-?[\d.]+/g).map(Number); };
    var a = nums(dInicial), b = nums(dFinal);
    var t0 = performance.now();
    requestAnimationFrame(function tick(t) {
      var p = Math.min(1, (t - t0) / duracaoMs);
      var atual = a.map(function (v, i) { return v + (b[i] - v) * p; });
      var i = 0;
      el.setAttribute('d', dInicial.replace(/-?[\d.]+/g, function () { return atual[i++]; }));
      if (p < 1) requestAnimationFrame(tick);
    });
  }

  document.querySelectorAll('.morph-icon').forEach(function (btn) {
    var path = btn.querySelector('.morph-icon__path');
    btn.addEventListener('mouseenter', function () { morph(path, DENTRO, FORA); });
    btn.addEventListener('mouseleave', function () { morph(path, FORA, DENTRO); });
    btn.addEventListener('focus', function () { morph(path, DENTRO, FORA); });
    btn.addEventListener('blur', function () { morph(path, FORA, DENTRO); });
  });
})();
```

Armadilhas: o par de paths precisa ter exatamente o mesmo número de comandos e na mesma ordem (M, L, C e assim por diante), senão o navegador não interpola e o ícone salta em vez de morphar suavemente. O jeito mais seguro de garantir isso na mão é escrever os dois estados só com M e L absolutos, evitando misturar atalhos como h, v ou l entre os dois desenhos, as letras de comando precisam ser idênticas em tipo e caixa (M é diferente de m, L é diferente de l). Suporte a `d` animável via CSS ainda é limitado a navegadores baseados em Chromium, sempre mantenha o fallback JS de interpolação numérica ou um crossfade simples de opacity entre dois ícones fixos, já incluído acima. Morph acima de 300ms em elemento pequeno de 24px fica lento e chama atenção demais para um detalhe que deveria ser sutil.

Fonte: CSS-Tricks, "Animate SVG Path Changes in CSS" e "How SVG Shape Morphing Works"

Variante Framer: Framer Motion não faz morph nativo entre paths de formatos diferentes, exige a mesma condição de mesmo número de pontos manualmente, ou combine com uma lib de interpolação como flubber quando os formatos têm contagens diferentes.
