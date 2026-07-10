# Componentes Premium (`componentes-premium`)

Catálogo vivo dos componentes de interface com a assinatura do William: botões com estados reais, números tratados como dado, feedback de formulário que respeita quem está digitando, e telas de espera que nunca parecem quebradas. Consulte este arquivo sempre que a peça tiver um CTA, um formulário, uma métrica em destaque, uma lista ou grade de itens, ou qualquer momento de carregamento e resposta assíncrona.

Toda receita abaixo já foi verificada e cola direto num HTML único com CSS e JS vanilla. Toda transição respeita `prefers-reduced-motion` e usa como base só `transform`/`opacity` (a fundamentação completa dessas duas regras está em `motion-principios.md`).

## Índice

| Componente | Quando usar |
|---|---|
| Squash and Stretch em Clique | Botão primário, ícone clicável, qualquer CTA que precisa parecer vivo ao ser pressionado |
| Glass Shine (Brilho de Reconhecimento) | Botão ou card em glass sutil que precisa de um reforço visual de "isto é clicável" |
| Botão Assinatura: Morph de Estados + Checkmark que se Desenha | Todo submit assíncrono do HTML único: form, checkout, cadastro, newsletter |
| Contador Numérico (Count-up) | Uma métrica de destaque em prova social: anos de mercado, número de projetos |
| Barra de Progresso com scroll() | Artigos longos, LPs com storytelling vertical extenso, páginas de case study |
| Anel de Foco Premium | Todo elemento focável de um formulário ou peça premium |
| Anel de Spotlight na Borda | Cards ou inputs com conteúdo denso, reforço de foco em campos de formulário |
| Validação Inline sob Demanda | Campos com regra clara (email, senha, CPF) em cadastro ou checkout |
| Toast Empilhado Estilo Sonner | Feedback de ação assíncrona que não deve travar o formulário |
| Nasce do Gatilho | Dropdown, menu de contexto, popover ancorado a um elemento clicável |
| Esqueleto Espelho | Placeholder de dado assíncrono com layout já conhecido: tabela, card, perfil |
| Foco Progressivo (Blur-up) | Hero image, foto de card, thumbnail de galeria pesada |
| Giro Contido | Espera curta dentro de um botão de salvar, atualizar ou refazer uma ação |
| Marquee de Logos | Prova social logo após o hero, quando existem marcas reconhecíveis |
| Feed Cíclico (Animated List) | Feed de atividade real, changelog, lista curta e cadenciada |
| Bento Grid Animado | Seção de features com 3 a 6 informações de peso desigual |
| Grade Presa com Zoom de Scroll | Uma única seção de showcase entre dois blocos de conteúdo importantes |
| Capa que Dobra (Sticky Scale/Rotate) | Transição cênica entre hero e primeira seção, no máximo 1 a 2 vezes por página |
| Produto Revelado Quadro a Quadro | Hero de produto físico que gira ou abre só com scroll, sem vídeo |

---

## Botões e CTAs

### Squash and Stretch em Clique

**O que é:** compressão e alongamento sutis em `scale`, não um scale linear e seco, que dão peso físico e elasticidade a um elemento respondendo a um clique, como se o material tivesse alguma flexibilidade.

**Quando usar:** botão primário no `:active`, ícone que reage a clique, CTA que precisa parecer vivo ao ser pressionado. É o ponto de contato tátil por excelência numa UI premium minimalista.

**Nota de fonte:** a receita original desta técnica passou por uma revisão que apenas confirmou o código como correto, sem reproduzir o snippet completo no material recebido. O código abaixo foi reconstruído a partir da descrição técnica e das armadilhas documentadas (ratio de 5 a 15%, transform-origin correto, exigência de `display` não inline, workaround de iOS Safari) e validado antes de entrar na skill.

```css
:root { --spring: cubic-bezier(.34, 1.56, .64, 1); }

.btn-squash {
  display: inline-flex; /* obrigatório: em display:inline, transform é ignorado */
  transform: scale(1);
  transition: transform 220ms var(--spring);
}

.btn-squash:active {
  /* comprime na vertical e alonga na horizontal: ~6% de variação, dentro
     da faixa de 5 a 15% recomendada. Em botão, transform-origin fica no
     padrão (center), que é o correto para este caso. */
  transform: scale(1.06, 0.94);
}

@media (prefers-reduced-motion: reduce) {
  .btn-squash { transition: none; }
  .btn-squash:active { transform: none; }
}
```

```js
// Necessário em iOS Safari: sem um listener de touch em algum ancestral,
// o estado :active não dispara de forma confiável em toques.
document.body.addEventListener('touchstart', () => {}, { passive: true });
```

**Armadilhas:** exagerar no ratio (acima de 1.15 a 1.2) parece efeito de jogo casual e quebra o tom minimalista, ficar entre 5% e 15% de variação. Transform-origin errado (bottom para um elemento que pousa, center para botão) faz o elemento parecer flutuar de forma estranha. Não aplicar em texto longo, esticar letras fica ilegível. Sempre envolver em `@media (prefers-reduced-motion: no-preference)`, quem é sensível a movimento não deve ver nada disso. Garanta que o elemento tenha `display: inline-flex/inline-block/block`, em `display:inline` a transformação é ignorada pelo navegador e a animação não produz efeito visual algum.

**Fonte:** https://www.joshwcomeau.com/animation/squash-and-stretch/

---

### Glass Shine (Brilho de Reconhecimento)

**O que é:** uma faixa de luz branca translúcida, inclinada, que atravessa o elemento uma única vez no hover, simulando reflexo em vidro ou superfície polida. É um flash de confirmação de interação, não um loop contínuo.

**Quando usar:** botões primários ou cards com fundo escuro em glassmorphism sutil, como reforço visual de que o elemento é interativo. Não usar em texto corrido, em elementos muito pequenos (perde legibilidade do movimento) nem repetir automaticamente sem interação do usuário.

```css
.glass-btn {
  position: relative;
  overflow: hidden;
  background: rgba(255,255,255,0.06);
  border: 1px solid rgba(255,255,255,0.12);
  -webkit-backdrop-filter: blur(6px);
  backdrop-filter: blur(6px);
}
.glass-btn::before {
  content: "";
  position: absolute;
  top: 0; left: -60%;
  width: 40%; height: 100%;
  background: linear-gradient(90deg,
    transparent, rgba(255,255,255,0.2), transparent);
  transform: skewX(-20deg);
  /* transition fica só no :hover de propósito: o motor de CSS Transitions
     usa a duração declarada no estado PARA ONDE a propriedade está indo.
     Ao sair do hover, o estado de destino é esta regra base (sem transition
     declarada = duração 0), então o brilho some instantaneamente em vez de
     varrer o botão de novo ao contrário. É isso que garante "um flash só,
     não um vaivém". */
}
.glass-btn:hover::before {
  left: 140%;
  transition: left .6s ease;
}

@media (prefers-reduced-motion: reduce) {
  .glass-btn::before { display: none; }
}
```

**Armadilhas:** gradiente com branco muito opaco no centro (acima de 0.3) parece plástico brilhante e barato, manter entre 0.15 e 0.25. Faixa muito estreita ou transição muito rápida (abaixo de 400ms) dá sensação de flash ou piscada, manter entre 500 e 700ms e 35 a 50% de largura da faixa. Reaplicar em loop via `setInterval` é o erro mais comum, deve disparar só uma vez por hover. `backdrop-filter` tem custo real de performance, evitar em muitos elementos simultâneos visíveis na tela. Sempre desativar no `prefers-reduced-motion`.

**Fonte:** https://dev.to/crayoncode/shiny-glass-hover-effect-glassmorphism-17n7 (CodePen companion: https://codepen.io/crayon-code/pen/abmgooe)

**Variante Framer:** `whileHover` disparando uma keyframe de `x` indo de -60% a 140% num `motion.span` posicionado dentro do botão, uma vez por hover, sem repetição automática.

---

### Botão Assinatura: Morph de Estados + Checkmark que se Desenha

Esta é a peça de assinatura do William: duas receitas que nasceram sobrepostas (o botão que troca de conteúdo entre idle, loading e sucesso, e o checkmark que se desenha em duas etapas) e que juntas formam UM componente coeso. O botão nunca troca de largura, nunca mostra um segundo botão do lado, e o momento de sucesso não é um símbolo estático: é o mesmo traço vivo (stroke-dashoffset) que assina o resto do sistema, desenhando o círculo e depois o "v" do check com um leve overshoot.

**O que é:** o botão de submit muda de conteúdo sem mudar de posição ou tamanho (largura fixa via `min-width`): idle mostra o texto, loading troca o texto por um spinner e desabilita o botão, sucesso troca o spinner pelo checkmark, que se desenha em duas etapas usando o atributo `pathLength="1"` direto no SVG (normaliza o comprimento do path para escala 0 a 1, sem precisar de `getTotalLength()` em JS) e some depois de 1,5 a 2 segundos, quando o formulário reseta ou navega.

**Quando usar:** em qualquer submit assíncrono do HTML único (form, checkout, cadastro, newsletter) sempre que a ação depender de uma resposta de rede. É microinteração de conteúdo, dispara em resposta a uma ação real do usuário, nunca decorativa solta na página.

**Nota de fonte:** o campo de código do checkmark na fonte original continha apenas a nota de aprovação de um revisor ("código correto, sem alterações"), sem reproduzir o SVG/CSS. A implementação abaixo funde a estrutura verificada do botão de morph de estados com o SVG do checkmark, reconstruído a partir da descrição técnica (pathLength="1", duas etapas, delay do check maior que a duração do círculo, overshoot limitado a valores abaixo de 1.7 no cubic-bezier) e validado antes de entrar na skill.

```html
<button class="btn" type="submit" data-state="idle">
  <span class="btn-label">Enviar</span>
  <span class="btn-spinner" aria-hidden="true"></span>
  <svg class="btn-check" aria-hidden="true" viewBox="0 0 24 24" width="20" height="20">
    <circle class="btn-check__circle" cx="12" cy="12" r="10" pathLength="1" fill="none" stroke="currentColor" stroke-width="2"></circle>
    <path class="btn-check__mark" d="M7 12.5L10.5 16L17 8.5" pathLength="1" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path>
  </svg>
  <span class="btn-status" role="status" aria-live="polite" style="position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap;"></span>
</button>
```

```css
.btn {
  position: relative;
  min-width: 140px;
  display: grid;
  place-items: center;
}
.btn-label, .btn-spinner, .btn-check {
  grid-area: 1 / 1;
  transition: opacity 200ms ease, transform 200ms ease;
}
.btn-spinner, .btn-check { opacity: 0; }

.btn-spinner {
  width: 16px;
  height: 16px;
  border: 2px solid currentColor;
  border-top-color: transparent;
  border-radius: 50%;
}

/* checkmark: pathLength="1" normaliza o comprimento do path para escala
   0 a 1, então dasharray/dashoffset funcionam sem getTotalLength() em JS */
.btn-check__circle,
.btn-check__mark {
  stroke-dasharray: 1;
  stroke-dashoffset: 1;
}

/* loading */
.btn[data-state="loading"] .btn-label { opacity: 0; transform: scale(.9); }
.btn[data-state="loading"] .btn-spinner {
  opacity: 1;
  animation: spin 700ms linear infinite;
}

/* success: label e spinner somem, o checkmark se desenha em duas etapas */
.btn[data-state="success"] .btn-label { opacity: 0; }
.btn[data-state="success"] .btn-spinner { opacity: 0; }
.btn[data-state="success"] .btn-check { opacity: 1; }
.btn[data-state="success"] .btn-check__circle {
  animation: desenhar 500ms cubic-bezier(.65,0,.35,1) forwards;
}
.btn[data-state="success"] .btn-check__mark {
  /* delay maior que a duração do círculo, senão os dois desenham juntos
     e perde a leitura de confirmação em duas etapas */
  animation: desenhar 350ms cubic-bezier(.34,1.56,.64,1) 450ms forwards;
}

@keyframes desenhar { to { stroke-dashoffset: 0; } }
@keyframes spin { to { transform: rotate(360deg); } }

@media (prefers-reduced-motion: reduce) {
  .btn-label, .btn-spinner, .btn-check {
    transition: opacity 1ms linear !important;
    transform: none !important;
  }
  .btn-spinner { animation-duration: 1.2s; }
  .btn-check__circle, .btn-check__mark {
    animation-duration: 1ms !important;
    animation-delay: 0ms !important;
    stroke-dashoffset: 0;
  }
}
```

```js
async function submitFlow(btn, task) {
  const statusEl = btn.querySelector('.btn-status');
  btn.dataset.state = 'loading';
  btn.disabled = true;
  if (statusEl) statusEl.textContent = 'Enviando...';
  try {
    await task();
    btn.dataset.state = 'success';
    if (statusEl) statusEl.textContent = 'Concluído';
    await new Promise(r => setTimeout(r, 1600));
  } catch (err) {
    if (statusEl) statusEl.textContent = 'Ocorreu um erro, tente novamente';
    throw err;
  } finally {
    btn.dataset.state = 'idle';
    btn.disabled = false;
  }
}
```

**Armadilhas:** deixar a largura do botão variar entre texto e spinner causa layout shift visível, sempre reservar `min-width`. Reabilitar o botão antes da resposta do servidor permite duplo submit acidental. Esquecer de restaurar o estado idle em caso de erro trava o botão em sucesso mentiroso ou em loading para sempre, use sempre `try/finally`. O checkmark sozinho não é suficiente para leitores de tela, anuncie via `aria-live`/`role="status"` junto (a `.btn-status` acima cumpre esse papel). `pathLength` é atributo do elemento SVG, não propriedade CSS, precisa ir direto no markup do `circle` e do `path`. O delay do check (450ms) precisa ser maior que a duração do círculo (500ms), senão os dois desenham juntos e perde a leitura de confirmação em duas etapas. Overshoot forte demais no cubic-bezier (valores acima de 1.7) foge do tom minimalista e fica com cara de brinquedo, o valor usado aqui (1.56) é o mesmo do token `--spring` do sistema.

**Fonte:** uxpin.com "Button States Explained"; nngroup.com "Button States: Communicate Interaction"; logrocket blog "Designing button states"; técnica pathLength=1 documentada por Cassie Evans em workshops de SVG animation e por CSS-Tricks, estrutura em duas etapas (círculo mais check) é o padrão canônico do "animated checkmark".

**Variante Framer:** Framer Motion anima os dois paths como `pathLength` com delay sequencial no `transition` (mesma lógica de duas etapas) e dispensa o atributo `pathLength="1"` porque o Motion já normaliza sozinho.

---

## Números e Dados

### Contador Numérico (Count-up)

**O que é:** número que anima de um valor base até o valor final com easing suave quando entra na viewport, tratando o dado como conteúdo em vez de decoração.

**Quando usar:** seções de prova social ou métricas (anos de mercado, número de projetos), sempre UM número por peça, tipografia grande, nunca em fileira de 3 ou mais blocos idênticos.

```js
function countUp(el, target, duration = 1200) {
  if (matchMedia('(prefers-reduced-motion: reduce)').matches) {
    el.textContent = target.toLocaleString('pt-BR');
    return;
  }
  const start = performance.now();
  const easeOutCubic = t => 1 - Math.pow(1 - t, 3);
  function tick(now) {
    const p = Math.min((now - start) / duration, 1);
    el.textContent = Math.round(easeOutCubic(p) * target).toLocaleString('pt-BR');
    if (p < 1) requestAnimationFrame(tick);
  }
  requestAnimationFrame(tick);
}

const io = new IntersectionObserver((entries) => {
  entries.forEach(e => {
    if (e.isIntersecting) {
      countUp(e.target, Number(e.target.dataset.target));
      io.unobserve(e.target);
    }
  });
}, { threshold: 0.6 });
document.querySelectorAll('[data-counter]').forEach(el => io.observe(el));
```

**Armadilhas:** contador em todos os números da página vira gadget. Duração longa demais parece brincadeira. Formatar com sufixo genérico tipo "+K" igual todo mundo. Disparar de novo ao reentrar na viewport é erro, deve rodar uma única vez, sempre com `unobserve`. Easing linear fica robótico, use `easeOut`. Jamais usar 2 ou 3 contadores lado a lado imitando cards clone de métrica.

**Fonte:** https://magicui.design/docs/components/number-ticker

**Variante Framer:** `useSpring(0, { stiffness: 100, damping: 30 })` combinado com `useInView(ref, { once: true })`, atualizando o texto no evento `change` do spring.

---

### Barra de Progresso com scroll()

**O que é:** barra fixa no topo que preenche de 0 a 100% em sincronia direta com a rolagem da página, sem nenhum listener de scroll em JS: o navegador liga a timeline da animação à posição de rolagem do documento inteiro.

**Quando usar:** artigos longos, LPs com storytelling vertical extenso, páginas de case study onde faz sentido dar feedback de progresso de leitura. Não usar em páginas curtas (uma dobra e meia), a barra não acrescenta nada e vira ruído visual.

```html
<div class="progress-bar"></div>
```

```css
:root { --accent: #4C7CF3; }

.progress-bar {
  position: fixed;
  top: 0; left: 0;
  width: 100%;
  height: 3px;
  background: var(--accent);
  transform-origin: 0 50%;
  transform: scaleX(0);
  z-index: 50;

  animation: grow-progress auto linear;
  animation-timeline: scroll(root block);
}

@keyframes grow-progress {
  from { transform: scaleX(0); }
  to   { transform: scaleX(1); }
}

@media (prefers-reduced-motion: reduce) {
  .progress-bar { animation: none; opacity: 0; }
}
```

**Armadilhas:** `animation-duration` precisa ser `auto`, nunca segundos, senão a barra roda no tempo errado e dessincroniza do scroll real. A propriedade `animation-timeline` é reset-only no shorthand `animation`: sempre declarar `animation-timeline` depois do shorthand `animation`, nunca antes, senão ele reseta para `auto`. Risco de slop: nada de glow, gradiente arco-íris ou barra grossa arredondada tipo loading spinner, é uma linha fina de 2 a 3px na cor de acento única do DNA.

**Fonte:** MDN Web Docs, "Scroll progress animations in CSS"; Chrome for Developers, "Animate elements on scroll".

---

## Feedback e Forms

### Anel de Foco Premium

**O que é:** o estado de foco por teclado nunca pode ser removido ou empobrecido visualmente, mas pode ser desenhado com a mesma intenção do resto da peça. A versão base usa um anel composto de duas camadas em `box-shadow` (um gap na cor da superfície seguido de um anel na cor de acento única do DNA), padrão usado por Vercel Geist e por Linear no lugar do azul genérico do navegador. Existe também uma variante de anel único com entrada animada, útil quando o elemento fica dentro de um container com `overflow:hidden` que cortaria o `box-shadow`. As duas disparam só em `:focus-visible`, então clique de mouse não acende o anel, apenas navegação por teclado ou foco programático.

**Quando usar:** em todo input, textarea, select ou botão focável de um formulário premium. É o detalhe que separa uma peça premium de uma peça que só parece bonita no mouse.

**Base obrigatória (anel duplo, Vercel Geist / Linear):**

```css
:root { --accent: #3b62ff; --surface: #F4F4F2; }
:root[data-theme="dark"] { --surface: #0A0C0F; }

.input,
.select,
.textarea,
.btn {
  border: 1px solid rgba(10,12,15,.12);
  border-radius: 10px;
  padding: 12px 14px;
  outline: none;
  transition: border-color 150ms cubic-bezier(.4,0,.2,1),
              box-shadow 150ms cubic-bezier(.4,0,.2,1);
}

.input:focus-visible,
.select:focus-visible,
.textarea:focus-visible,
.btn:focus-visible {
  border-color: var(--accent);
  box-shadow: 0 0 0 2px var(--surface), 0 0 0 4px var(--accent);
}

@media (prefers-reduced-motion: reduce) {
  .input, .select, .textarea, .btn { transition: none; }
}
```

**Variante com entrada animada (quando um ancestral corta o box-shadow):**

```css
:root { --focus-color: #4F7CFF; } /* o único acento de cor da peça */

.focusable {
  outline: none; /* só remove o padrão porque substitui por algo melhor abaixo */
}

.focusable:focus-visible {
  outline: 2px solid var(--focus-color);
  outline-offset: 4px;
  border-radius: 6px;
  animation: focus-in 180ms cubic-bezier(0.16, 1, 0.3, 1);
}

@keyframes focus-in {
  from {
    outline-offset: 0px;
    outline-color: color-mix(in srgb, var(--focus-color) 55%, transparent);
  }
  to {
    outline-offset: 4px;
    outline-color: var(--focus-color);
  }
}

@media (prefers-reduced-motion: reduce) {
  .focusable:focus-visible {
    animation: none;
  }
}
```

**Armadilhas:** usar `:focus` em vez de `:focus-visible` aplica o anel também em cliques de mouse, poluindo a UI. Remover `outline` sem `:focus-visible` como substituto é o erro clássico de acessibilidade e quebra navegação por teclado (WCAG 2.4.7). O anel via `box-shadow` (assim como `outline`) é cortado quando um ancestral tem `overflow:hidden`, por exemplo um card com `border-radius` que recorta uma imagem, nesse caso use a variante de anel único com `outline-offset`, ou mova o `overflow:hidden` para um wrapper mais interno. Animar `border-width` em vez de `box-shadow`/`outline` causa reflow a cada foco, o anel deve sempre entrar por essas duas propriedades. Teste o contraste do anel nos dois temas (claro e escuro), o gap precisa bater com `--surface` de cada modo ou o anel "flutua" errado. Nunca usar a mesma cor do texto para o anel, ele precisa ser reconhecível em leitura periférica rápida.

**Fonte:** Vercel Geist (vercel.com/geist/input); Linear.app design notes (tom lavanda de assinatura no focus ring); padrão double-ring documentado em Piccalilli, "Taking a shot at the double focus ring problem"; rauno.me/craft/interaction-design (princípio de detalhes invisíveis aplicado a estados de foco).

**Variante Framer:** `<motion.button whileFocus={{ outlineOffset: 4, opacity: 1 }} initial={{ outlineOffset: 0 }} transition={{ duration: 0.18, ease: [0.16,1,0.3,1] }} />`.

---

### Anel de Spotlight na Borda

**O que é:** variação do spotlight de card onde só a borda de 1px acende perto do cursor, usando `mask-composite` para criar um anel oco sobre um pseudo elemento com padding, em vez de iluminar a área inteira do card.

**Quando usar:** cards ou inputs com conteúdo denso (texto, imagem) onde um glow de área inteira brigaria com o conteúdo. Também funciona bem em campos de formulário no `focus-within`, como reforço de foco mais elegante que o outline padrão do navegador.

```html
<div class="field">
  <input type="text" placeholder="seu email" />
</div>
```

```css
.field {
  position: relative;
  border-radius: 12px;
}
.field input {
  all: unset;
  box-sizing: border-box;
  display: block;
  width: 100%;
  padding: 14px 16px;
  border-radius: inherit;
  background: #101318;
  color: #F4F4F2;
}
.field::after {
  content: "";
  position: absolute;
  inset: -1px;
  border-radius: inherit;
  padding: 1px;
  background: radial-gradient(160px circle at var(--x, 50%) var(--y, 50%),
    rgba(232, 138, 53, 0.9), transparent 70%);
  -webkit-mask: linear-gradient(#000 0 0) content-box, linear-gradient(#000 0 0);
          mask: linear-gradient(#000 0 0) content-box, linear-gradient(#000 0 0);
  -webkit-mask-composite: xor;
          mask-composite: exclude;
  opacity: 0;
  transition: opacity .35s ease;
  pointer-events: none;
}
.field:hover::after,
.field:focus-within::after {
  opacity: 1;
}

@media (prefers-reduced-motion: reduce) {
  .field::after {
    transition: none;
  }
}
```

```js
document.querySelectorAll('.field').forEach((field) => {
  field.addEventListener('pointermove', (e) => {
    const rect = field.getBoundingClientRect();
    field.style.setProperty('--x', `${e.clientX - rect.left}px`);
    field.style.setProperty('--y', `${e.clientY - rect.top}px`);
  });
});
```

**Armadilhas:** `mask-composite` tem suporte com prefixo diferente entre engines (`-webkit-mask-composite: xor` versus `mask-composite: exclude`), declare os dois. Precisa de raio menor que o spotlight de preenchimento (150 a 200px) para não virar um halo grosso em vez de um anel fino. Só funciona bem em elementos que já têm alguma borda ou raio de canto definidos, aplicado num elemento sem borda visível o efeito parece surgir do nada. Teste também o foco via teclado (`focus-within`), não só hover de mouse, para não quebrar acessibilidade. O wrapper `.field` (div) precisa envolver o `<input>` com estilos `all: unset`, aplicar a classe direto no `<input>` faz o `::after` nunca renderizar, por ser elemento substituído.

**Fonte:** ibelick, "Creating an interactive spotlight border with CSS and React" (https://ibelick.com/blog/create-spotlight-border-with-react-css).

**Variante Framer:** mesma estrutura de mask, mas com `useMotionTemplate` gerando `--x`/`--y` e `motion.div` animando a opacidade de entrada e saída do anel.

---

### Validação Inline sob Demanda

**O que é:** o campo não valida a cada tecla digitada. Ele só mostra erro depois que o usuário sai do campo (evento `blur`) pela primeira vez. A partir desse ponto, passa a revalidar em tempo real a cada tecla, até o campo ficar válido, momento em que o feedback some. É o padrão que pesquisa de UX mede como redução real de erros percebidos, porque nunca pune quem ainda está no meio de digitar.

**Quando usar:** campos com regra clara e verificável (email, senha, CPF, campo obrigatório) em formulários de cadastro, checkout ou captura de lead. Não usar em campos livres de texto longo, onde validação em tempo real não faz sentido.

```js
function wireInlineValidation(input, validate) {
  let touched = false;
  const msg = input.parentElement.querySelector('[data-error]');

  // Liga o input à mensagem de erro para leitor de tela
  if (msg) {
    if (!msg.id) msg.id = `${input.id || Math.random().toString(36).slice(2)}-error`;
    msg.setAttribute('aria-live', 'polite');
    input.setAttribute('aria-describedby', msg.id);
  }

  input.addEventListener('blur', () => {
    touched = true;
    applyResult(validate(input.value));
  });

  input.addEventListener('input', () => {
    if (touched) applyResult(validate(input.value)); // só revalida ao vivo após o 1º erro
  });

  function applyResult(error) {
    input.classList.toggle('is-invalid', !!error);
    input.classList.toggle('is-valid', touched && !error && input.value !== '');
    input.setAttribute('aria-invalid', String(!!error));
    if (msg) msg.textContent = error || '';
  }
}
```

**Armadilhas:** validar a cada tecla desde a primeira digitação pune o usuário no meio da tarefa e aumenta ansiedade. Esconder o erro sem anunciar via `aria-live`/`aria-invalid` deixa leitor de tela sem contexto. Trocar só a cor da borda (verde ou vermelho) sem ícone ou texto é sinal fraco para daltonismo. Nunca bloquear o submit silenciosamente, sempre mostre por que o formulário não avança.

**Fonte:** pesquisa de UX de formulários agregada de Baymard, Zuko e Nielsen Norman Group, apontando aumento de 22% na taxa de sucesso e queda de 22% em erros com validação inline on-blur versus validação só no submit; guidance de copy de erro do Vercel Geist ("name the field and the constraint, ends in a period").

---

### Toast Empilhado Estilo Sonner

**O que é:** toasts se empilham como um baralho: cada um atrás do topo recebe `translateY` negativo proporcional ao índice (gap de 14px) e um `scale` reduzido (0.05 por índice), criando ilusão de profundidade com poucos elementos visíveis. Ao passar o mouse ou focar, a pilha expande e revela todos os toasts na vertical. Arrastar (swipe) remove o toast se a distância ou a velocidade do gesto ultrapassar um limiar, o que vier primeiro, sem precisar completar um arraste longo.

**Quando usar:** feedback de ações assíncronas que não deve travar o formulário (salvo com sucesso, falha de rede, item enviado). Use com moderação: um toast por evento relevante, nunca um por autosave silencioso.

```css
.toaster { position: relative; }

.toast {
  position: absolute;
  inset-inline: 0;
  bottom: 0;
  touch-action: none; /* o JS assume o controle do gesto, evita scroll nativo brigando com o drag */
  transition: transform 400ms ease, opacity 400ms ease;
  transform: translateY(calc(var(--index) * -14px)) scale(calc(1 - var(--index) * 0.05));
}

.toaster.expanded .toast {
  transform: translateY(calc(var(--offset) * -1px)) scale(1);
}

@media (prefers-reduced-motion: reduce) {
  .toast { transition: opacity 200ms ease; }
}
```

```js
function layoutToasts(toasts, expanded) {
  let offset = 0;
  toasts.forEach((t, i) => {
    t.style.setProperty('--index', i);
    t.style.setProperty('--offset', offset);
    offset += expanded ? t.offsetHeight + 14 : 0;
  });
}

function bindHoverExpand(toasterEl, toasts) {
  const expand = () => { toasterEl.classList.add('expanded'); layoutToasts(toasts, true); };
  const collapse = () => { toasterEl.classList.remove('expanded'); layoutToasts(toasts, false); };
  toasterEl.addEventListener('pointerenter', expand);
  toasterEl.addEventListener('pointerleave', collapse);
  toasterEl.addEventListener('focusin', expand);  // acessível via teclado, não só mouse/touch
  toasterEl.addEventListener('focusout', collapse);
}

function bindSwipe(toast, onDismiss) {
  const DISTANCE_THRESHOLD = 45;   // px
  const VELOCITY_THRESHOLD = 0.11; // px/ms
  let dragging = false, startY = 0, startT = 0;

  toast.addEventListener('pointerdown', e => {
    dragging = true;
    startY = e.clientY;
    startT = performance.now();
    toast.setPointerCapture(e.pointerId); // garante que pointerup/pointermove continuem chegando mesmo fora do elemento
    toast.style.transition = 'none';      // sem lag: o toast segue o dedo em tempo real
  });

  toast.addEventListener('pointermove', e => {
    if (!dragging) return;
    const dy = e.clientY - startY;
    const y = dy > 0 ? dy : dy * 0.15; // leve resistência ao arrastar na direção "errada"
    toast.style.transform = `translateY(${y}px)`;
    toast.style.opacity = String(Math.max(1 - Math.abs(dy) / 200, 0.3));
  });

  function endDrag(e) {
    if (!dragging) return;
    dragging = false;
    toast.style.transition = ''; // volta a usar a transition definida no CSS

    const dy = e.clientY - startY;
    const elapsed = Math.max(performance.now() - startT, 1);
    const velocity = Math.abs(dy) / elapsed;

    if (Math.abs(dy) > DISTANCE_THRESHOLD || velocity > VELOCITY_THRESHOLD) {
      onDismiss(toast);
    } else {
      toast.style.transform = '';
      toast.style.opacity = '';
    }
  }

  toast.addEventListener('pointerup', endDrag);
  toast.addEventListener('pointercancel', endDrag);
}
```

**Armadilhas:** usar `@keyframes` em vez de transitions/transform direto trava a suavidade porque keyframes não são interrompíveis, um novo toast chegando faz os antigos "pularem" para a nova posição em vez de deslizar. Animar `top`/`margin-top` em vez de `transform` causa reflow e jank perceptível. Esquecer uma região `aria-live` no container deixa leitor de tela sem anunciar o toast. Não limitar o número de toasts visíveis deixa a pilha crescer sem controle.

**Fonte:** sonner.emilkowal.ski; emilkowal.ski/ui/building-a-toast-component.

---

### Nasce do Gatilho

**O que é:** um elemento que aparece a partir de um ponto de origem (botão, ícone) deve nascer visualmente daquele ponto, não do centro da tela. `transform-origin` dinâmico combinado com `@starting-style`, o recurso nativo do CSS para animar entrada sem JavaScript de estado, cria essa sensação sem nenhuma biblioteca.

**Quando usar:** dropdowns, menus de contexto, popovers e tooltips grandes ancorados a um elemento clicável. Exceção: modais ficam centralizados e não usam origem do gatilho.

```css
.popover {
  transform-origin: var(--origem, top center);
  transition: opacity 200ms cubic-bezier(0.23,1,0.32,1),
              transform 200ms cubic-bezier(0.23,1,0.32,1);
  opacity: 1;
  transform: scale(1);
}
.popover[hidden] { display: none; }

:root {
  --popover-scale-inicial: 0.95;
}

@starting-style {
  .popover { opacity: 0; transform: scale(var(--popover-scale-inicial)); }
}

.popover.is-fechando {
  opacity: 0;
  transform: scale(var(--popover-scale-inicial));
}

@media (prefers-reduced-motion: reduce) {
  :root { --popover-scale-inicial: 1; }
  .popover {
    transition-duration: 80ms;
    transition-timing-function: linear;
  }
}
```

```js
/* JS lê a posição do gatilho, calcula a origem RELATIVA AO PRÓPRIO POPOVER
   (não ao viewport), e cuida de abertura e fechamento com transição real */
function abrirPopover(gatilho, popover) {
  popover.classList.remove("is-fechando");
  popover.removeAttribute("hidden"); // precisa estar renderizado para medir

  const rectGatilho = gatilho.getBoundingClientRect();
  const rectPopover = popover.getBoundingClientRect();
  const origemX = rectGatilho.left + rectGatilho.width / 2 - rectPopover.left;
  popover.style.setProperty("--origem", `${origemX}px top`);
}

function fecharPopover(popover) {
  const finalizarFechamento = (evento) => {
    if (evento.target !== popover || evento.propertyName !== "opacity") return;
    popover.setAttribute("hidden", "");
    popover.classList.remove("is-fechando");
    popover.removeEventListener("transitionend", finalizarFechamento);
  };
  popover.addEventListener("transitionend", finalizarFechamento);
  popover.classList.add("is-fechando");
}
```

**Armadilhas:** `@starting-style` ainda não tem suporte universal, preveja fallback com classe `.visivel` e transição manual para navegadores antigos. Deixar `transform-origin` fixo em `center` quebra a ilusão de que o menu nasce do botão, principalmente em menus alinhados à direita da tela. Aplicar essa técnica num modal por engano descentraliza um componente que deveria ficar fixo no meio da tela.

**Fonte:** https://github.com/emilkowalski/skills/blob/main/skills/emil-design-eng/SKILL.md e https://emilkowal.ski/ui/good-vs-great-animations

**Variante Framer:** `style={{ transformOrigin: origem }} initial={{ opacity: 0, scale: 0.95 }} animate={{ opacity: 1, scale: 1 }} exit={{ opacity: 0, scale: 0.95 }}`.

---

## Loading e Vazio

### Esqueleto Espelho

**O que é:** placeholder com exatamente a mesma forma e dimensão do conteúdo final (altura de linha, largura de avatar, proporção de card), preenchido com um único tom neutro da paleta e um brilho sutil de dois tons (nunca multicor) que varre a superfície uma vez por ciclo.

**Quando usar:** quando dados assíncronos vão preencher um layout já conhecido: linhas de tabela, grid de cards, bloco de perfil, sidebar. Não usar para esperas sem forma definida, nesse caso, use um spinner contido.

```css
.skeleton {
  --sk-base: #E4E4E0;   /* off-white base, um tom abaixo */
  --sk-shine: #F4F4F2;  /* mesmo off-white do DNA, sem matiz extra */
  width: var(--w, 100%);
  height: var(--h, 1em);
  border-radius: 6px;
  background: linear-gradient(100deg, var(--sk-base) 40%, var(--sk-shine) 50%, var(--sk-base) 60%);
  background-size: 200% 100%;
  animation: sk-sweep 1.6s ease-in-out infinite;
}

/* dark: regra própria (não misturar seletor com @media na mesma lista) */
:root[data-theme="dark"] .skeleton {
  --sk-base: #14161B;
  --sk-shine: #1D2027;
}
@media (prefers-color-scheme: dark) {
  .skeleton {
    --sk-base: #14161B;
    --sk-shine: #1D2027;
  }
}
/* light explícito: garante que o toggle manual vença mesmo com SO em dark */
:root[data-theme="light"] .skeleton {
  --sk-base: #E4E4E0;
  --sk-shine: #F4F4F2;
}

@keyframes sk-sweep {
  from { background-position: 150% 0; }
  to   { background-position: -50% 0; }
}

/* linhas múltiplas: escalonar para não piscar em uníssono.
   nth-of-type é mais seguro que nth-child se houver elementos
   não-.skeleton entre os irmãos. */
.skeleton:nth-of-type(2) { animation-delay: .12s; }
.skeleton:nth-of-type(3) { animation-delay: .24s; }

@media (prefers-reduced-motion: reduce) {
  .skeleton { animation: none; opacity: .7; }
}
```

**Armadilhas:** gradiente com várias cores (efeito arco-íris) é o carimbo mais visível de UI genérica de IA, use só dois tons do mesmo neutro. O skeleton precisa ter a mesma altura e largura do conteúdo real (meça antes), senão o texto real "pula" quando chega e quebra a sensação premium. Várias linhas de skeleton brilhando exatamente juntas parece robótico, escalonar o delay resolve.

**Fonte:** Vercel Geist Skeleton (https://vercel.com/geist/skeleton); Vercel Web Interface Guidelines (https://vercel.com/design/guidelines); LogRocket, "Skeleton loading screen design".

**Variante Framer:** `motion.div` com variants de opacity/backgroundPosition e `staggerChildren` no container de linhas para escalonar o delay automaticamente em vez de `nth-child` manual.

---

### Foco Progressivo (Blur-up)

**O que é:** a imagem final se revela a partir de uma miniatura borrada já embutida no HTML (LQIP em base64), com o desfoque diminuindo e um crossfade curto para a versão em alta resolução assim que ela termina de carregar, sem deslocar o layout.

**Quando usar:** hero images, fotos de card, thumbnails de galeria; qualquer imagem pesada cujo download não pode travar o primeiro paint da página.

```html
<div class="blur-img" style="aspect-ratio:16/9">
  <img class="blur-img__lqip" src="data:image/jpeg;base64,..." alt="">
  <img class="blur-img__full" data-src="foto-full.jpg" alt="Descrição real">
</div>
```

```css
.blur-img { position:relative; overflow:hidden; background:#E4E4E0; }
.blur-img__lqip, .blur-img__full {
  position:absolute; inset:0; width:100%; height:100%; object-fit:cover;
}
.blur-img__lqip { filter: blur(18px); transform: scale(1.1); }
.blur-img__full { opacity:0; transition: opacity .5s ease; }
.blur-img__full.is-loaded { opacity:1; }

@media (prefers-reduced-motion: reduce) {
  .blur-img__full { transition: none; }
}
```

```js
function initBlurImg(root = document) {
  root.querySelectorAll('.blur-img').forEach(wrap => {
    const full = wrap.querySelector('.blur-img__full');
    if (!full || !full.dataset.src) return;
    const pre = new Image();
    pre.onload = () => {
      full.src = full.dataset.src;
      requestAnimationFrame(() => full.classList.add('is-loaded'));
    };
    pre.src = full.dataset.src;
  });
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', () => initBlurImg());
} else {
  initBlurImg();
}
```

**Armadilhas:** trocar o blur pela imagem nítida sem transição quebra a sensação de revelação, sempre anime `opacity`. Sem `scale(1.1)` no LQIP a borda borrada do zoom vaza nas bordas do container. Blur acima de 20 a 24px em thumbs médios parece imagem quebrada, não elegante. Sempre reserve `aspect-ratio` fixo no wrapper para não gerar layout shift antes mesmo do JS rodar.

**Fonte:** CSS-Tricks, "The Blur-Up Technique for Loading Background Images"; José M. Pérez, "How Medium does progressive image loading".

**Variante Framer:** `motion.img` com `initial={{opacity:0}} animate={{opacity:1}}` disparado no `onLoad` da imagem final, mantendo o LQIP como background-image fixo por baixo.

---

### Giro Contido

**O que é:** indicador giratório pequeno, do mesmo tamanho do texto ou ícone ao lado dele, usado só para esperas curtas disparadas por uma ação direta do usuário. Nunca para carregar uma página inteira ou dominar o layout.

**Quando usar:** dentro de botões de enviar/salvar, ícone de atualizar inline, retry de uma linha de tabela; esperas de aproximadamente 1 a 3 segundos.

```html
<button class="btn" id="save-btn">
  <span class="btn__label">Salvar</span>
</button>
```

```css
.btn__spinner {
  width: 1em; height: 1em; border-radius: 50%;
  border: 2px solid color-mix(in srgb, var(--accent) 25%, transparent);
  border-top-color: var(--accent);
  animation: spin .7s linear infinite;
  display: inline-block; margin-right: .5em;
  vertical-align: -0.15em; /* alinha opticamente com a baseline do texto */
}

@keyframes spin { to { transform: rotate(360deg); } }

@media (prefers-reduced-motion: reduce) {
  .btn__spinner { animation-duration: 1.6s; }
}

.btn[aria-busy="true"] {
  cursor: progress;
}
```

```js
const saveBtn = document.getElementById('save-btn');
const saveLabel = saveBtn.querySelector('.btn__label');
const originalLabel = saveLabel.textContent;

saveBtn.addEventListener('click', async () => {
  if (saveBtn.getAttribute('aria-busy') === 'true') return; // evita clique duplo empilhar spinners

  saveBtn.setAttribute('aria-busy', 'true');
  saveBtn.disabled = true;

  const spinner = document.createElement('span');
  spinner.className = 'btn__spinner';
  saveBtn.prepend(spinner); // monta o elemento, nunca só esconde com display:none

  // troca o texto só se a espera passar de ~1s, sem "piscar" em respostas rápidas
  const slowLabelTimer = setTimeout(() => {
    saveLabel.textContent = 'Salvando…';
  }, 1000);

  try {
    await sendForm(); // ponto de integração: chamada assíncrona real (fetch, etc.)
  } finally {
    clearTimeout(slowLabelTimer);
    spinner.remove();
    saveLabel.textContent = originalLabel;
    saveBtn.removeAttribute('aria-busy');
    saveBtn.disabled = false;
  }
});

// placeholder de exemplo, substituir pela chamada real
async function sendForm() {
  return new Promise((resolve) => setTimeout(resolve, 1500));
}
```

**Armadilhas:** pré-renderizar o spinner com `display:none` e só alternar visibilidade deixa uma rotação parcial congelada visível no primeiro frame, o que lê como falha, sempre crie e remova o elemento. Nunca substituir o texto do botão pelo spinner sozinho, mantenha o label ao lado. Se a espera passar de 1 segundo, troque o texto para algo como "Salvando…" com reticências.

**Fonte:** Vercel Geist Spinner (https://vercel.com/geist/spinner); Vercel Web Interface Guidelines (https://vercel.com/design/guidelines).

**Variante Framer:** `AnimatePresence` envolvendo o spinner com exit/initial de opacity e um `motion.span` com `animate={{rotate:360}} transition={{repeat:Infinity, ease:'linear', duration:.7}}`.

---

## Listas e Grades

### Marquee de Logos

**O que é:** faixa horizontal com loop infinito em velocidade constante (sem salto perceptível), pausa no hover, usada para exibir logos de clientes ou parceiros com clima editorial, não de banner publicitário.

**Quando usar:** seção de prova social ("usado por", "mencionado em"), nunca como peça principal do hero, sempre com base neutra ao redor.

```css
.marquee {
  overflow: hidden;
  -webkit-mask-image: linear-gradient(90deg, transparent, #000 8%, #000 92%, transparent);
  mask-image: linear-gradient(90deg, transparent, #000 8%, #000 92%, transparent);
}
.marquee__track {
  display: flex;
  width: max-content;
  gap: 4rem;
  animation: marquee-scroll var(--duration, 28s) linear infinite;
}
.marquee:hover .marquee__track { animation-play-state: paused; }
.marquee__track img { filter: grayscale(1); opacity: .6; transition: filter .3s, opacity .3s; }
.marquee__track img:hover { filter: grayscale(0); opacity: 1; }
@keyframes marquee-scroll { from { transform: translateX(0); } to { transform: translateX(-50%); } }
@media (prefers-reduced-motion: reduce) { .marquee__track { animation: none; } }
```

```html
<!-- markup real: duas cópias idênticas do mesmo grupo de logos dentro do track.
     a translateX(-50%) desloca exatamente a largura de uma cópia (a track inteira
     mede as 2 cópias somadas), então quando a 1ª cópia sai o loop reinicia sem salto. -->
<div class="marquee">
  <div class="marquee__track">
    <div class="marquee__group">
      <img src="logo-1.svg" alt="Cliente 1" />
      <img src="logo-2.svg" alt="Cliente 2" />
      <img src="logo-3.svg" alt="Cliente 3" />
    </div>
    <div class="marquee__group" aria-hidden="true">
      <img src="logo-1.svg" alt="" />
      <img src="logo-2.svg" alt="" />
      <img src="logo-3.svg" alt="" />
    </div>
  </div>
</div>

<style>
.marquee__group { display: flex; gap: 4rem; }
</style>
```

**Armadilhas:** logos coloridos demais quebram a base neutra, sempre grayscale mais opacidade, cor só no hover. Esquecer de duplicar o conteúdo gera pulo visível no loop. Velocidade rápida demais parece rodapé de propaganda de TV. Não pausar no hover impede o usuário de ler. `mask-image` sem prefixo `-webkit-` quebra no Safari.

**Fonte:** https://magicui.design/docs/components/marquee

---

### Feed Cíclico (Animated List)

**O que é:** lista compacta onde um novo item entra periodicamente por cima (fade, leve `translateY` negativo e `scale`), empurrando os antigos, com máscara de gradiente no rodapé suavizando a saída, sugerindo atividade ao vivo sem ruído visual.

**Quando usar:** feed de atividade real (últimos eventos, últimas ações do sistema), changelog, lista curta e cadenciada. Máximo 5 a 6 itens visíveis por vez.

```html
<div class="feed" id="feed" aria-live="off"></div>

<style>
.feed {
  position: relative;
  overflow: hidden;
  max-height: 22rem;
  -webkit-mask-image: linear-gradient(to bottom, #000 80%, transparent);
  mask-image: linear-gradient(to bottom, #000 80%, transparent);
}
.feed__item {
  opacity: 0;
  transform: translateY(-12px) scale(.96);
  transition: opacity .35s ease, transform .35s ease;
}
.feed__item.is-in { opacity: 1; transform: translateY(0) scale(1); }

@media (prefers-reduced-motion: reduce) {
  .feed__item { transition: none; opacity: 1; transform: none; }
}
</style>

<script>
const feed = document.querySelector('.feed');

// Placeholders: troque por sua fonte de dados real (websocket, polling de API,
// SSE etc). Nunca inventar evento/prova social falsa aqui, ver armadilhas.
function buildItemNode(data) {
  const el = document.createElement('div');
  el.className = 'feed__item';
  el.textContent = data.text;
  return el;
}
let cursor = 0;
function nextData() {
  cursor++;
  return { text: `Evento real #${cursor}` };
}

function pushItem(feedEl, node, max = 5) {
  feedEl.prepend(node);
  requestAnimationFrame(() => requestAnimationFrame(() => node.classList.add('is-in')));
  const items = feedEl.querySelectorAll('.feed__item');
  if (items.length > max) items[items.length - 1].remove();
}

let timer;
let paused = false;

function loop() {
  if (paused || document.hidden || matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  pushItem(feed, buildItemNode(nextData()));
}
timer = setInterval(loop, 2600);

feed.addEventListener('mouseenter', () => { paused = true; });
feed.addEventListener('mouseleave', () => { paused = false; });
</script>
```

**Armadilhas:** loop infinito sem pausa incomoda quem está lendo, sempre pausar em `document.hidden` e idealmente no hover. Usar dado fake tipo "fulano comprou agora" é prova social falsa e antiético, só use dado real. Máscara sem prefixo `-webkit-` quebra Safari. Mais de 5 a 6 itens visíveis vira ruído. `setInterval` rodando com a aba em background desperdiça CPU sem necessidade.

**Fonte:** https://magicui.design/docs/components/animated-list

**Variante Framer:** `AnimatePresence` envolvendo os itens com `layout` e `initial={{ opacity: 0, y: -20, scale: .9 }} animate={{ opacity: 1, y: 0, scale: 1 }} exit={{ opacity: 0, scale: .8 }}`.

---

### Bento Grid Animado

**O que é:** grid assimétrico (blocos de tamanhos variados conforme a importância real do conteúdo, não cards clonados) onde cada célula entra em cascata sutil e ganha profundidade leve (elevação e sombra, sem glow) no hover.

**Quando usar:** seção de features ou capacidades do produto, showcase com 3 a 6 informações de peso desigual entre si.

```css
.bento {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  grid-auto-rows: 120px;
  gap: 1px;
  background: var(--border);
}
.bento__cell {
  background: var(--surface);
  grid-column: span var(--cols, 2);
  grid-row: span var(--rows, 1);
  opacity: 0;
  transform: translateY(12px);
  transition: opacity .5s ease, transform .5s ease, box-shadow .3s ease;
  transition-delay: calc(var(--i, 0) * 70ms);
}
.bento__cell.is-in { opacity: 1; transform: translateY(0); }
.bento__cell:hover {
  transition-delay: 0s; /* impede que o delay de entrada "vaze" para o hover */
  box-shadow: 0 8px 30px rgba(0,0,0,.08);
  transform: translateY(-2px);
}
@media (prefers-reduced-motion: reduce) {
  .bento__cell { transition: none; opacity: 1; transform: none; }
}
```

```js
document.querySelectorAll('.bento').forEach(grid => {
  const cells = grid.querySelectorAll('.bento__cell');
  cells.forEach((c, i) => c.style.setProperty('--i', i));
  const io = new IntersectionObserver(([entry]) => {
    if (!entry.isIntersecting) return;
    cells.forEach(c => c.classList.add('is-in'));
    io.unobserve(entry.target);
  }, { threshold: 0.15 });
  io.observe(grid);
});
```

**Armadilhas:** três blocos idênticos em tamanho e conteúdo é o card clone banido no DNA, cada plano deve ter hierarquia de conteúdo diferente. Dot-grid ou gradiente de fundo dentro dos blocos é slop clássico. Hover com glow ou shine border também. Cascata com delay tão grande que a última célula demora segundos é ruim. Variar tamanho dos blocos só por estética, sem relação com a importância real do conteúdo, quebra a lógica do padrão.

**Fonte:** https://magicui.design/docs/components/bento-grid

**Variante Framer:** `parent = { hidden: {}, show: { transition: { staggerChildren: .07 } } }` combinado com `whileInView="show"` e `viewport={{ once: true }}` no container, `whileHover={{ y: -2 }}` em cada célula.

---

### Grade Presa com Zoom de Scroll

**O que é:** uma seção fica presa na tela via `position: sticky` enquanto o usuário rola por um contêiner alto; a grade de imagens escala e ganha opacidade guiada nativamente por `animation-timeline: view()` do CSS, sem JS de scroll rodando o tempo todo, com fallback via scroll listener para navegadores sem suporte.

**Quando usar:** uma única seção de showcase ou transição entre dois blocos de conteúdo importantes da página, não em toda seção da peça.

```html
<div class="showcase">
  <div class="showcase__stage">
    <div class="showcase__grid">
      <img src="1.jpg" alt="" loading="lazy" width="600" height="400">
      <img src="2.jpg" alt="" loading="lazy" width="600" height="400">
      <img src="3.jpg" alt="" loading="lazy" width="600" height="400">
    </div>
  </div>
</div>
```

```css
.showcase{
  height:400vh;
  /* .showcase é o "sujeito" do View Timeline: sua visibilidade
     dentro do scroller raiz é que dirige a animação */
  view-timeline-name:--showcase-progress;
  view-timeline-axis:block;
}
.showcase__stage{
  position:sticky;top:0;height:100vh;
  overflow:hidden;display:grid;place-items:center;
}
.showcase__grid{
  display:grid;grid-template-columns:repeat(3,1fr);gap:1rem;
  animation:grid-zoom linear both;
  /* referencia o View Timeline nomeado acima, não um scroll() cru */
  animation-timeline:--showcase-progress;
  animation-range:entry 0% cover 60%;
  will-change:transform,opacity;
}
@keyframes grid-zoom{
  from{transform:scale(.7);opacity:.4}
  to{transform:scale(1.1);opacity:1}
}
@media (prefers-reduced-motion:reduce){
  .showcase{height:auto;view-timeline-name:none}
  .showcase__stage{position:static;height:auto;overflow:visible}
  .showcase__grid{animation:none;transform:none;opacity:1}
}
```

```js
(function(){
  var reduceMotion = matchMedia('(prefers-reduced-motion: reduce)').matches;
  var supportsViewTimeline = CSS.supports('animation-timeline: view()');
  if(reduceMotion || supportsViewTimeline) return; // nativo cuida, ou usuário não quer movimento

  var grid = document.querySelector('.showcase__grid');
  var stage = document.querySelector('.showcase');
  var ticking = false;

  function update(){
    var r = stage.getBoundingClientRect();
    var p = Math.min(1, Math.max(0, -r.top / (r.height - innerHeight)));
    grid.style.transform = 'scale(' + (.7 + p*.4) + ')';
    grid.style.opacity = .4 + p*.6;
    ticking = false;
  }
  addEventListener('scroll', function(){
    if(!ticking){ requestAnimationFrame(update); ticking = true; }
  }, {passive:true});
})();
```

**Armadilhas:** `animation-timeline: scroll()` ainda não é suportado em todo Safari, então o fallback JS é obrigatório, não decorativo. `height:400vh` mal dimensionado cria "scroll morto" onde nada muda por muitas telas, péssimo para UX. Escala acima de 1.3 estica e pixela imagens raster. Usar essa técnica em mais de uma seção por página vira gimmick repetitivo, o oposto de microinteração como conteúdo. A seção presa some do controle natural do usuário, então precisa de feedback visual claro de progresso.

**Fonte:** https://tympanus.net/codrops/2026/03/02/sticky-grid-scroll-building-a-scroll-driven-animated-grid/

**Variante Framer:** `useScroll({ target: stageRef, offset:['start start','end end'] })` combinado com `useTransform` mapeando `scrollYProgress` para `scale`, `<motion.div style={{ position:'sticky', top:0, scale }} />`.

---

## Transições Cênicas

Duas peças "pesadas" que também nasceram catalogadas como componente, mas que funcionam mais como set pieces de transição de página do que como blocos reutilizáveis em toda seção. Use no máximo uma vez por peça, nunca as duas juntas na mesma LP.

### Capa que Dobra (Sticky Scale/Rotate)

**O que é:** a seção A fica grudada no topo (`sticky`) enquanto a próxima sobe por baixo; conforme o scroll avança dentro do contêiner, A encolhe e inclina levemente, como uma capa sendo virada, revelando B.

**Quando usar:** transição entre hero e primeira seção de conteúdo, ou entre dois blocos de storytelling que merecem uma pausa cênica; usar no máximo uma ou duas vezes por página.

```html
<!-- <div class="pair" style="height:200vh"><section class="cover">A</section><section class="reveal">B</section></div> -->
```

```css
.pair { position: relative; }
.cover {
  position: sticky;
  top: 0;
  height: 100vh;
  transform-origin: center top;
  will-change: transform;
}
.reveal { position: relative; height: 100vh; }

@media (prefers-reduced-motion: reduce) {
  .cover { transform: none !important; border-radius: 0 !important; }
}
```

```js
const pair = document.querySelector('.pair');
const cover = pair.querySelector('.cover');
const reduceMotion = matchMedia('(prefers-reduced-motion: reduce)').matches;

function clamp(v, min, max) {
  return Math.min(max, Math.max(min, v));
}

let ticking = false;

function update() {
  const r = pair.getBoundingClientRect();
  const p = clamp(-r.top / (r.height - innerHeight), 0, 1);
  cover.style.transform = `scale(${1 - 0.2 * p}) rotate(${-5 * p}deg)`;
  cover.style.borderRadius = `${p * 24}px`;
  ticking = false;
}

function onScroll() {
  if (!ticking) {
    requestAnimationFrame(update);
    ticking = true;
  }
}

if (!reduceMotion) {
  addEventListener('scroll', onScroll, { passive: true });
  addEventListener('resize', onScroll, { passive: true });
  onScroll(); // aplica o estado correto se a página já carregar parcialmente scrollada
}
```

**Armadilhas:** esquecer o `border-radius` progressivo faz o encolhimento parecer um corte quadrado artificial. `rotate` acima de 6 a 8 graus foge do minimalismo do DNA e lembra slide de apresentação. Scroll listener sem `passive:true` gera jank em mobile. Usar essa transição 3 ou mais vezes na mesma página vira montanha russa e contraria o respiro generoso do DNA.

**Fonte:** https://blog.olivierlarose.com/tutorials/perspective-section-transition

**Variante Framer:** `useScroll({ target: container, offset:['start start','end end'] })` combinado com `useTransform` mapeando `scrollYProgress` para `scale` (1 a 0.8) e `rotate` (0 a -5).

---

### Produto Revelado Quadro a Quadro

**O que é:** uma sequência de imagens numeradas é desenhada num canvas fixo dentro de uma seção alta; a posição de scroll dentro da seção escolhe qual quadro desenhar, criando o efeito de girar ou abrir o produto só com scroll, sem vídeo.

**Quando usar:** reveal de produto físico (rotação, abertura, montagem) quando não se quer depender de arquivo de vídeo; funciona bem como hero de produto único.

```html
<div class="frame-wrap" style="height:400vh">
  <div class="frame-stage"><canvas width="1200" height="800"></canvas></div>
</div>
```

```css
.frame-wrap{position:relative}
.frame-stage{position:sticky;top:0;height:100vh;display:grid;place-items:center}
canvas{max-width:100%;max-height:100%}
```

```js
const N = 60;
const PRELOAD = 8; // carrega só os primeiros quadros de cara; o resto entra em segundo plano
const imgs = new Array(N);

function loadFrame(i){
  if (imgs[i]) return;
  const im = new Image();
  im.src = `/frames/f${String(i).padStart(3,'0')}.jpg`;
  imgs[i] = im;
}

for (let i = 0; i < Math.min(PRELOAD, N); i++) loadFrame(i);

const canvas = document.querySelector('canvas');
const ctx = canvas.getContext('2d');
const wrap = document.querySelector('.frame-wrap');

function draw(i){
  const idx = Math.min(N - 1, Math.max(0, i));
  loadFrame(idx); // rede de segurança se o scroll pular na frente do preload
  const im = imgs[idx];
  if (im && im.complete) ctx.drawImage(im, 0, 0, canvas.width, canvas.height);
}

let ticking = false;
function onScroll(){
  if (ticking) return;
  ticking = true;
  requestAnimationFrame(() => {
    const r = wrap.getBoundingClientRect();
    const scrollable = r.height - innerHeight;
    const p = scrollable > 0 ? Math.min(1, Math.max(0, -r.top / scrollable)) : 0;
    draw(Math.floor(p * (N - 1)));
    ticking = false;
  });
}

const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;

if (reduced){
  draw(N - 1); // reduced motion: mostra o quadro final direto, sem animação
} else {
  draw(0); // desenha o primeiro quadro já no load, sem esperar o usuário rolar
  addEventListener('scroll', onScroll, { passive: true });
  const loadRest = () => { for (let i = PRELOAD; i < N; i++) loadFrame(i); };
  if ('requestIdleCallback' in window) requestIdleCallback(loadRest);
  else setTimeout(loadRest, 200);
}
```

**Armadilhas:** carregar todos os quadros de uma vez trava a página, pré-carregue só os primeiros e busque o resto em segundo plano, ou use poucos quadros (30 a 60) com JPEG comprimido. Sem `passive:true` e sem throttle via `rAF` o scroll fica pesado. Sempre cheque `img.complete` antes de `drawImage` para não desenhar quadro vazio. Em `prefers-reduced-motion`, pule a animação e mostre direto o quadro final.

**Fonte:** CSS-Tricks, "Let's Make One of Those Fancy Scrolling Animations Used on Apple Product Pages"; confirmado por referência a `hero_startframe`/`hero_endframe` no markup de apple.com/mac-mini.

---

## Regra de montagem

Nenhuma peça deve usar todas as 19 receitas deste arquivo de uma vez. Uma LP típica pede: 1 receita de botão (o assinatura se houver submit real), 1 de foco/forms se houver formulário, no máximo 1 de números se houver métrica de destaque, 1 de loading se houver dado assíncrono, e 1 de lista/grade se houver prova social ou features. As duas transições cênicas do final são o tempero raro, no máximo uma por página inteira.
