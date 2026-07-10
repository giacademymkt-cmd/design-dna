# Padrões de Seção Premium (`secoes-premium`)

Registro de como os sites mais bem desenhados do mundo (Linear, Stripe, Vercel, Raycast, Apple) estruturam os blocos que toda página de produto precisa: abertura, prova social, oferta, fechamento e transição de conteúdo. Leia isto antes de desenhar qualquer seção de uma LP ou página de produto, quando a dúvida for mais estrutural que estética: quanto de largura o visual do hero ocupa, quantas colunas o footer aguenta, como destacar um plano sem parecer propaganda. Cada padrão já vem com o esqueleto de código pronto para colar e adaptar.

### Hero Editorial com Aceno de Produto

**De onde veio:** Linear, Stripe, Raycast.

**O que é:** Headline grande (uma frase só, sem hype) alinhada ao centro ou à esquerda, subtítulo curto com largura restrita, dois CTAs (um sólido primário, um fantasma/outline secundário) e, abaixo ou ao lado, um visual real do produto (screenshot de UI, nunca ilustração 3D ou orb) como prova principal. Quando existe um texto acima do headline (o kicker, tipo "New Coding Sessions" no Linear), ele é pequeno, funcional e neutro, nunca um badge colorido tipo pílula.

**Proporções e medidas observadas:** subtítulo com 38 a 45 caracteres por linha; visual do produto ocupando 40 a 60% da composição; borda de 1px no visual com sombra suave (nunca sombra 3D dramática ou rotação em perspectiva); uma frase só de headline, nunca duas empilhadas tentando dizer tudo.

**Esqueleto:**

```html
<section class="hero">
  <p class="hero__kicker">Novo: Coding Sessions</p>
  <h1 class="hero__title">O sistema para times e agentes construírem produto</h1>
  <p class="hero__subtitle">Feito para planejar e construir, desenhado para a era da IA.</p>
  <div class="hero__ctas">
    <a class="btn btn--primary" href="#start">Começar agora</a>
    <a class="btn btn--ghost" href="#demo">Ver demonstração</a>
  </div>
  <div class="hero__visual" data-reveal>
    <img src="app-screenshot.png" alt="" />
  </div>
</section>
```

```css
.hero{ max-width:1120px; margin-inline:auto; padding:160px 24px 96px; text-align:center; }
.hero__kicker{ font-size:.8125rem; color:var(--muted); margin-bottom:20px; } /* nunca dar background/border-radius/cor de destaque aqui: isso vira pill e é slop */
.hero__title{ font-size:clamp(2.5rem, 4vw + 1rem, 4.25rem); line-height:1.05; letter-spacing:-.02em; max-width:20ch; margin-inline:auto; }
.hero__subtitle{ margin:24px auto 0; max-width:42ch; color:var(--muted); font-size:1.125rem; }
.hero__ctas{ display:flex; gap:12px; justify-content:center; margin-top:36px; }
.hero__visual{
  margin-top:80px;
  border:1px solid var(--border);
  border-radius:16px;
  box-shadow:0 24px 60px -20px rgba(0,0,0,.35);
  overflow:hidden;
  opacity:0;
  transform:translateY(24px);
  transition:opacity .8s ease, transform .8s ease;
}
.hero__visual.is-visible{ opacity:1; transform:none; }

@media (prefers-reduced-motion: reduce){
  .hero__visual{ opacity:1; transform:none; transition:none; }
}
```

```js
(function () {
  var visual = document.querySelector('.hero__visual');
  if (!visual) return;

  var prefersReduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (prefersReduced) {
    visual.classList.add('is-visible');
    return;
  }

  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (entry.isIntersecting) {
        entry.target.classList.add('is-visible');
        io.unobserve(entry.target);
      }
    });
  }, { threshold: 0.2 });

  io.observe(visual);
})();
```

**Armadilhas:** badge grande e colorido acima do título (tipo pílula gradiente) é slop puro, na referência real o kicker é texto pequeno neutro. Screenshot com sombra 3D exagerada ou rotação em perspectiva também é slop, a sombra deve ser suave e reta. Não empilhar duas frases de headline tentando dizer tudo de uma vez, uma frase só.

**Fonte:** linear.app, stripe.com, raycast.com

---

### Faixa de Logos em Movimento Contínuo (Prova Social)

**De onde veio:** Stripe (marquee de logos), Raycast (grid de avatares como variante por pessoas).

**O que é:** Stripe usa um marquee infinito com logos coloridos reconhecíveis, sem headline gritante acima, no máximo um microtexto neutro tipo "Usado por milhares de empresas". Raycast prefere um grid estático de avatares de pessoas reais com citação curta em vez de logos. Em ambos os casos o elemento fica logo abaixo do hero, antes de qualquer explicação de feature, como prova de credibilidade instantânea e silenciosa.

**Proporções e medidas observadas:** 12 a 15 logos por ciclo; ciclo lento de 30 a 40 segundos (nunca rápido, isso quebra a sensação premium); lista duplicada exatamente igual para o loop fechar sem costura; máscara de gradiente nas bordas (transparente até 8% e de 92% até o fim) para o logo não nascer/morrer bruscamente.

**Esqueleto:**

```html
<div class="logowall" aria-label="Empresas que confiam">
  <div class="logowall__track">
    <img src="l1.svg" alt="Empresa 1"><img src="l2.svg" alt="Empresa 2">
    <!-- ...mais logos... -->
  </div>
  <div class="logowall__track" aria-hidden="true">
    <!-- duplicar exatamente a mesma lista, garante loop sem costura -->
  </div>
</div>
```

```css
.logowall{
  overflow:hidden;
  display:flex;
  mask-image:linear-gradient(90deg,transparent,#000 8%,#000 92%,transparent);
  -webkit-mask-image:linear-gradient(90deg,transparent,#000 8%,#000 92%,transparent);
}
.logowall__track{ display:flex; gap:64px; align-items:center; flex-shrink:0; animation:scroll 36s linear infinite; }
.logowall__track img{ height:28px; width:auto; filter:grayscale(1); opacity:.55; transition:opacity .3s, filter .3s; }
.logowall__track img:hover{ opacity:1; filter:none; }
.logowall:hover .logowall__track{ animation-play-state:paused; }
@keyframes scroll{ to{ transform:translateX(-100%); } }

@media (prefers-reduced-motion: reduce){
  .logowall{ mask-image:none; -webkit-mask-image:none; }
  .logowall__track{ animation:none; flex-wrap:wrap; flex-shrink:1; }
  .logowall__track[aria-hidden="true"]{ display:none; } /* esconde o clone: sem isso a lista aparece duplicada na tela */
}
```

**Armadilhas:** velocidade rápida demais quebra a sensação premium, o ciclo real da referência é lento (30 a 40s). Esquecer de duplicar a lista deixa um salto visível no loop. Não pausar no hover nem respeitar prefers-reduced-motion é falha grave de acessibilidade para algo puramente decorativo.

**Fonte:** stripe.com (marquee de logos), raycast.com (grid de avatares como variante de prova social por pessoas)

---

### Cartão Central Elevado (Pricing sem Badge Gritante)

**De onde veio:** Linear, Raycast.

**O que é:** 3 a 5 planos lado a lado (Linear tem 4, Raycast tem 5). O plano recomendado, que nem sempre é o do meio geométrico (no Linear é o Business, penúltimo), recebe destaque sutil: elevação vertical, borda na cor de acento em vez de cinza, sombra mais funda com o próprio tom do acento, e botão preenchido sólido enquanto os demais usam outline. A diferença entre os cards é de peso visual, não de tamanho de fonte ou de conteúdo, e cada plano precisa de hierarquia própria de conteúdo, não só o número do preço mudando.

**Proporções e medidas observadas:** translateY negativo de 8 a 16px no card em destaque; borda de 1 a 2px na cor de acento; scale nunca acima de 1.05 (quebra o alinhamento da grade e vira brinquedo); rótulo do destaque é uma linha de texto discreta na cor de acento, nunca uma fita diagonal "Mais Popular" berrante.

**Esqueleto:**

```html
<div class="pricing">
  <article class="plan"><h3>Free</h3>...<a class="btn" href="#">Começar</a></article>
  <article class="plan plan--featured">
    <p class="plan__label">Recomendado</p>
    <h3>Pro</h3>...<a class="btn" href="#">Começar</a>
  </article>
  <article class="plan"><h3>Enterprise</h3>...<a class="btn" href="#">Falar com vendas</a></article>
</div>
```

```css
/* assume tokens definidos no :root do documento final, por exemplo:
   --border:#E4E4E0; --accent:#2D5BFF; --fg:#0A0C0F; */

.pricing{
  display:grid;
  grid-template-columns:repeat(3,1fr);
  gap:24px;
  align-items:start;
  max-width:960px;
  margin-inline:auto;
}

.plan{
  border:1px solid var(--border);
  border-radius:14px;
  padding:32px;
  transition:transform .3s ease, box-shadow .3s ease;
}

.plan--featured{
  border-color:var(--accent);
  transform:translateY(-12px);
  box-shadow:0 20px 40px -16px color-mix(in oklab, var(--accent) 40%, transparent);
}

.plan--featured:hover{
  transform:translateY(-16px);
  box-shadow:0 28px 48px -16px color-mix(in oklab, var(--accent) 45%, transparent);
}

.plan__label{ font-size:.75rem; color:var(--accent); font-weight:600; margin-bottom:8px; }

.plan:not(.plan--featured) .btn{ background:transparent; border:1px solid var(--border); color:var(--fg); }
.plan--featured .btn{ background:var(--accent); color:#fff; border:none; }

/* responsivo: empilha e troca a elevação flutuante por só cor/borda de acento */
@media (max-width:720px){
  .pricing{ grid-template-columns:1fr; max-width:420px; }
  .plan--featured{ transform:none; order:-1; }
  .plan--featured:hover{ transform:none; }
}

@media (prefers-reduced-motion: reduce){
  .plan, .plan--featured, .plan--featured:hover{ transition:none; }
}
```

Nota: se o número de planos variar (Raycast usa 5), troque manualmente o `repeat(3,1fr)` pelo número real de cards, o valor não é dinâmico em CSS puro.

**Armadilhas:** três cards idênticos mudando só o número é o anti-padrão explícito do briefing, cada plano precisa de hierarquia de conteúdo diferente, não só de preço. Badge tipo fita diagonal "Mais Popular" em cor berrante é slop, a referência real usa uma linha de texto discreta na cor de acento. Escalar o card em destaque demais (scale acima de 1.05) quebra o alinhamento da grade e parece brinquedo.

**Fonte:** linear.app/pricing, raycast.com/pricing

---

### Footer em Grade Densa e Silenciosa

**De onde veio:** Linear, Vercel, Stripe, Raycast.

**O que é:** Footer com muitas colunas (4 a 8, Vercel chega a 7-8 com mais de 70 links, Stripe tem 7 colunas com mais de 60 links), cada uma com um título pequeno em caixa alta e letter-spacing, e links em cor de texto secundária de baixo contraste que ganham contraste total só no hover. Nenhum elemento decorativo, nenhuma imagem, nenhum CTA grande, apenas uma borda superior de 1px separando do conteúdo. É a antítese do footer minimalista de uma coluna: aqui a densidade é o próprio sinal de que o produto é maduro e tem profundidade.

**Proporções e medidas observadas:** 4 a 8 colunas com `grid-template-columns:repeat(auto-fit, minmax(140px, 1fr))`; título de coluna em `.75rem`, caixa alta, letter-spacing `.08em`; links em `.875rem`, opacidade `.85` em repouso subindo para opacidade total no hover ou focus; borda superior única de 1px, sem sombra nem gradiente.

**Esqueleto:**

```html
<footer class="footer">
  <div class="footer__grid">
    <nav class="footer__col" aria-label="Produto">
      <p class="footer__heading">Produto</p>
      <ul>
        <li><a href="#">Recursos</a></li>
        <li><a href="#">Preços</a></li>
        <li><a href="#">Changelog</a></li>
      </ul>
    </nav>
    <nav class="footer__col" aria-label="Empresa">
      <p class="footer__heading">Empresa</p>
      <ul>
        <li><a href="#">Sobre</a></li>
        <li><a href="#">Carreiras</a></li>
        <li><a href="#">Blog</a></li>
      </ul>
    </nav>
    <!-- repetir para Docs, Legal, Comunidade, Redes... -->
  </div>
</footer>
```

```css
.footer{ border-top:1px solid var(--border); padding:64px 24px 40px; }
.footer__grid{
  display:grid;
  grid-template-columns:repeat(auto-fit, minmax(140px, 1fr));
  gap:32px; max-width:1120px; margin-inline:auto;
}
.footer__col ul{ list-style:none; margin:0; padding:0; }
.footer__heading{ font-size:.75rem; text-transform:uppercase; letter-spacing:.08em; color:var(--muted); margin:0 0 16px; }
.footer__col a{
  display:block;
  font-size:.875rem;
  color:var(--muted);
  opacity:.85;
  text-decoration:none;
  padding:6px 0;
  transition:opacity .2s, color .2s;
}
.footer__col a:hover,
.footer__col a:focus-visible{ opacity:1; color:var(--fg); }

@media (prefers-reduced-motion: reduce){
  .footer__col a{ transition:none; }
}
```

**Armadilhas:** baixar demais o contraste dos links (abaixo de 4.5:1 no texto principal) fere acessibilidade mesmo sendo estilo dimmed, teste com o hover para garantir contraste total ali. Transformar o footer em segunda home page com CTA grande e imagem de produto quebra a função de fechamento silencioso da página.

**Fonte:** linear.app, vercel.com, stripe.com, raycast.com

---

### Capítulo Fixo com Texto Trocado (Scroll Storytelling)

**De onde veio:** Apple (páginas de iPhone e Mac).

**O que é:** Uma seção alta contém um bloco `sticky` que fica preso na tela enquanto o usuário rola; dentro dele, blocos de texto trocam de estado (fade in/out) conforme a posição de scroll avança dentro daquele intervalo. É o padrão clássico das páginas de produto Apple, onde a imagem fica parada e o texto ao redor muda em capítulos, contando uma história em etapas sobre um único produto sem trocar de tela.

**Proporções e medidas observadas:** seção com 300 a 400vh de altura (menos que isso troca os passos rápido demais para leitura); estágio sticky de 100vh; 3 a 5 etapas de texto por seção; visual limitado a `max-height:50vh` para não empurrar ou cortar o texto seguinte.

**Esqueleto:**

```html
<section class="pin-wrap" style="height:400vh">
  <div class="pin-stage">
    <img class="pin-visual" src="produto.jpg" alt="Produto em destaque">
    <div class="pin-steps">
      <p class="pin-step is-active">Redesenhado por dentro.</p>
      <p class="pin-step">Mais rápido em cada tarefa.</p>
      <p class="pin-step">Feito pra durar.</p>
    </div>
  </div>
</section>
```

```css
.pin-wrap{position:relative}
.pin-stage{
  position:sticky;top:0;height:100vh;
  display:flex;flex-direction:column;align-items:center;justify-content:center;
  gap:2rem;overflow:hidden;
}
.pin-visual{
  max-height:50vh;max-width:80vw;width:auto;height:auto;object-fit:contain;
}
.pin-steps{
  position:relative;
  width:min(90vw,32rem);
  height:3rem; /* área reservada fixa: evita o container colapsar a 0 e o texto sumir */
  text-align:center;
}
.pin-step{
  position:absolute;
  inset:0;
  margin:0;
  display:flex;align-items:center;justify-content:center;
  opacity:0;
  transform:translateY(12px);
  transition:opacity .5s ease,transform .5s ease;
  font-size:1.25rem;
}
.pin-step.is-active{opacity:1;transform:translateY(0)}
@media (prefers-reduced-motion:reduce){
  .pin-step{transition:none}
}
```

```js
const steps = [...document.querySelectorAll('.pin-step')];
const wrap = document.querySelector('.pin-wrap');
let ticking = false;

function onScroll(){
  const r = wrap.getBoundingClientRect();
  const range = r.height - innerHeight;
  const p = range > 0 ? Math.min(1, Math.max(0, -r.top / range)) : 0;
  const i = Math.min(steps.length - 1, Math.floor(p * steps.length));
  steps.forEach((s, idx) => s.classList.toggle('is-active', idx === i));
  ticking = false;
}

function requestTick(){
  if (!ticking){
    ticking = true;
    requestAnimationFrame(onScroll);
  }
}

addEventListener('scroll', requestTick, { passive: true });
addEventListener('resize', requestTick);
onScroll(); // sincroniza o estado logo no load, cobre reload com scroll restaurado no meio da seção
```

**Armadilhas:** altura da seção precisa ser generosa (300 a 400vh) ou os passos trocam rápido demais para leitura. Calcular o índice sem clamp pode estourar o array no último pixel de scroll, sempre usar `Math.min(steps.length-1, ...)`. Sem `passive:true` no listener de scroll, o rolamento trava em mobile. `position:sticky` para de funcionar se qualquer elemento ancestral tiver overflow diferente de visible, transform ou contain, não encaixe essa seção dentro de wrappers com essas propriedades.

**Fonte:** padrão confirmado em apple.com/mac-mini (wrappers altos com scroll estendido e troca de conteúdo por etapas) e descrito em artigos que documentam a estrutura de páginas de produto Apple.

---

### Vazio Discreto (Empty State)

**De onde veio:** Vercel Geist, padrão de estado vazio da comunidade (Linear incluso).

**O que é:** Estado vazio com um ícone de linha fina monocromático (`currentColor` em opacidade baixa, nunca ilustração colorida de estoque), título curto em sentence case e uma descrição de uma linha que soma informação nova, com no máximo um botão de ação. Serve para primeira execução sem dados, busca ou filtro sem resultado, inbox zerada, lista esvaziada depois de uma exclusão.

**Proporções e medidas observadas:** ícone de 40x40px, `stroke-width:1.4`, opacidade `.55`; padding vertical generoso (`4rem 1.5rem`); título em `1.05rem` peso 600; descrição em `.9rem`; um único CTA em texto (nunca botão sólido competindo com o CTA principal da página).

**Esqueleto:**

```html
<div class="empty-state" role="status" aria-live="polite">
  <svg class="empty-state__icon" width="40" height="40" viewBox="0 0 24 24"
       fill="none" stroke="currentColor" stroke-width="1.4" aria-hidden="true">
    <path d="M4 7h16M4 12h10M4 17h7"/>
  </svg>
  <h3 class="empty-state__title">Nenhum resultado encontrado</h3>
  <p class="empty-state__desc">Tente outro termo ou remova os filtros ativos.</p>
  <button class="empty-state__cta" type="button">Limpar filtros</button>
</div>
```

```css
.empty-state {
  display: flex; flex-direction: column; align-items: center; text-align: center;
  gap: .5rem; padding: 4rem 1.5rem;
  color: var(--fg-muted, rgba(10,12,15,.55));
}
.empty-state__icon { opacity: .55; margin-bottom: .5rem; }
.empty-state__title {
  margin: 0; font-size: 1.05rem; font-weight: 600;
  color: var(--fg, #0A0C0F);
}
.empty-state__desc { margin: 0; font-size: .9rem; }
.empty-state__cta {
  margin-top: 1rem; padding: 0; background: none; border: none;
  color: var(--accent, #3B82F6); font-weight: 600; cursor: pointer;
  transition: opacity .15s ease;
}
.empty-state__cta:hover { opacity: .7; }
.empty-state__cta:focus-visible { outline: 2px solid var(--accent, #3B82F6); outline-offset: 3px; }

/* opt-in: só usar quando o estado vazio SUBSTITUI uma lista populada em runtime
   (busca ou filtro), não em renderização estática inicial (ex: inbox zerada no load) */
.empty-state--enter { opacity: 0; transform: translateY(8px); transition: opacity .4s ease, transform .4s ease; }
.empty-state--enter.is-visible { opacity: 1; transform: translateY(0); }
@media (prefers-reduced-motion: reduce) {
  .empty-state--enter { transition: none; opacity: 1; transform: none; }
}
```

```js
// chamar só no momento em que o estado vazio troca dinamicamente uma lista populada
// (ex: callback de busca/filtro que zerou os resultados)
function showEmptyState(el) {
  el.classList.add('empty-state--enter');
  requestAnimationFrame(() => el.classList.add('is-visible'));
}
```

**Armadilhas:** ilustração colorida e fofa de estoque (foguete, caixa vazia, astronauta) é o clichê mais reconhecível de UI genérica, o ícone deve usar `currentColor` com opacidade reduzida, sem ganhar cor própria além do acento único da peça. Empilhar 2 ou 3 CTAs no vazio é sinal de indecisão de produto, ficar em um só. Nunca usar esse espaço para avisos críticos persistentes, eles desaparecem assim que o conteúdo carrega.

**Fonte:** Vercel Geist Empty State (vercel.com/geist/empty-state), Vercel Web Interface Guidelines (vercel.com/design/guidelines), SaaSUI, padrão de empty state do Linear (saasui.design/pattern/empty-state/linear)

---

## Regra de montagem

Uma página não usa todos os padrões de uma vez: escolha hero, uma prova social, uma oferta e um footer, e só entre um capítulo de scroll se a página realmente tiver uma história de produto para contar em etapas, não decoração. O que faz a combinação não virar template é a variação de peso entre as seções: se o hero já é denso e visual, deixe a prova social discreta e rápida; se o pricing é o clímax da página, o footer volta a ser silencioso. Nunca repita a mesma técnica de reveal (fade, sticky, marquee) em duas seções seguidas, isso é o que denuncia o piloto automático. E todo padrão aqui carrega sua própria regra de `prefers-reduced-motion`: reaproveite o esqueleto, mas nunca corte esse bloco ao adaptar.
