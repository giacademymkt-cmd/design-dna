# Especialista em Ecommerce (`ecommerce-especialista`)

O resto do design-dna ensina como uma peça deve **parecer**: paleta, tipografia, layout, motion. Este arquivo ensina como uma loja de verdade **funciona**, porque um mockup pode acertar todo acento de cor e toda sombra difusa e ainda assim parecer "arte" em vez de ecommerce, se faltar o que faz alguém confiar e comprar: seletor de variante sempre visível, selo de confiança no lugar certo, prazo de entrega honesto, checkout sem fricção. Leia isto **antes** de desenhar qualquer página de produto (PDP), carrinho, checkout ou categoria (PLP), e combine com o estilo visual escolhido em `SKILL.md` (`apple-premium`, `editorial-minimal-mockup` etc.): o estilo dá a pele, este arquivo dá o esqueleto que converte.

O calibre de referência aqui é pesquisa comportamental real de compra online, Baymard Institute (mais de 14 anos de teste de usabilidade, 30.000+ elementos de checkout avaliados em 327 lojas, 700+ problemas catalogados em páginas de listagem) e Nielsen Norman Group, não opinião de design. Onde a fonte é prática de mercado consolidada em vez de estudo formal (como o padrão de WhatsApp como canal de venda no ecommerce brasileiro pequeno), isso é declarado explicitamente na receita, sem forjar autoridade que a fonte não tem.

**Contexto de calibragem usado nos exemplos:** Caetana Estilo de Campo, ecommerce WooCommerce de pilchas gaúchas femininas (bombachas, vestidos), feitas sob encomenda (até 30 dias úteis, sem estoque pronto), variantes reais de cor e tamanho (P a EXG), frete grátis acima de R$299,99, devolução em 30 dias, pagamento via PagSeguro e PIX, suporte primário por WhatsApp, catálogo pequeno (poucas dezenas de peças, 2 categorias), zero avaliações formais ainda. Troque os números e nomes pelo projeto real, mas a estrutura vale para qualquer ecommerce pequeno brasileiro no mesmo perfil.

## Índice

| Padrão | Quando usar |
|---|---|
| Anatomia de PDP que Converte | Toda página de produto com preço e variante |
| Comunicação de Prazo Sob Encomenda | Produto feito por encomenda, sem estoque pronto |
| Checkout de Baixo Abandono | Fluxo de carrinho e finalização de compra |
| PLP Curada por Mais Vendidos | Categoria/listagem com catálogo pequeno (poucas dezenas de itens) |
| WhatsApp como Canal Paralelo de Venda | Ecommerce brasileiro pequeno com suporte via WhatsApp |
| Prova Social Sem Reviews | Loja nova, zero avaliações formais ainda |
| Sticky Add-to-Cart Mobile | Toda PDP acessada em tela pequena |

---

## Página de Produto (PDP)

### Anatomia de PDP que Converte

**De onde veio:** Baymard Institute, pesquisa de Product Page UX (testes de usabilidade em larga escala sobre como usuários avaliam, comparam e decidem comprar em páginas de produto).

**O que é:** a PDP se organiza em duas colunas no desktop, galeria à esquerda (50 a 58% da largura) e "buy-box" à direita (42 a 50%), com a buy-box acompanhando o scroll da galeria (`position: sticky`). Dentro da buy-box, a ordem importa e é a parte que mais projeto de IA erra: nome do produto, preço, seletor de variante (cor primeiro, depois tamanho, sempre com o valor selecionado visível no `<legend>`, nunca escondido dentro de um dropdown fechado), indicador de disponibilidade, o CTA principal, e **imediatamente abaixo do CTA** a faixa de selos de confiança (frete, troca, forma de pagamento). Esse último ponto é o erro mais comum: times de design tratam selo de confiança como rodapé decorativo e o empurram para o final da página, mas a pesquisa mostra que a dúvida ("e se não couber? e se eu quiser devolver?") acontece no exato segundo antes do clique em comprar, não depois.

**Proporções e medidas observadas:** galeria com thumbnails verticais ou em carrossel horizontal abaixo da imagem principal (nunca menos de 3 fotos, ideal 4 a 6, incluindo pelo menos uma foto de contexto de uso, não só still em fundo branco); preço em tipografia grande o bastante para ser o segundo elemento mais destacado da buy-box depois do nome do produto; seletor de variante com swatches de no mínimo 32px de toque (acessibilidade de clique) mostrando a cor real, não um nome de cor sem preview; faixa de confiança limitada a 3 itens (frete, troca, pagamento), nunca mais que isso na mesma linha.

**Esqueleto:**

```html
<div class="pdp">
  <div class="pdp__gallery">
    <img class="pdp__gallery-main" src="bombacha-terracota-01.jpg"
         alt="Bombacha gaúcha feminina terracota, vista frontal">
    <div class="pdp__thumbs" role="tablist" aria-label="Fotos do produto">
      <button class="pdp__thumb is-active" role="tab" aria-selected="true">
        <img src="bombacha-terracota-01-thumb.jpg" alt="">
      </button>
      <button class="pdp__thumb" role="tab" aria-selected="false">
        <img src="bombacha-terracota-02-thumb.jpg" alt="">
      </button>
      <button class="pdp__thumb" role="tab" aria-selected="false">
        <img src="bombacha-terracota-uso.jpg" alt="">
      </button>
    </div>
  </div>

  <div class="pdp__buybox">
    <p class="pdp__breadcrumb">Bombachas</p>
    <h1 class="pdp__title">Bombacha Terracota Estilo de Campo</h1>
    <p class="pdp__price">R$ 349,90</p>

    <fieldset class="pdp__variant">
      <legend>Cor: <strong class="pdp__variant-value">Terracota</strong></legend>
      <div class="pdp__swatches">
        <button class="pdp__swatch is-selected" style="--swatch:#B5502E" aria-label="Terracota" aria-pressed="true"></button>
        <button class="pdp__swatch" style="--swatch:#2E3B4E" aria-label="Azul marinho" aria-pressed="false"></button>
        <button class="pdp__swatch" style="--swatch:#3B3B3B" aria-label="Preto" aria-pressed="false"></button>
      </div>
    </fieldset>

    <fieldset class="pdp__variant">
      <legend>Tamanho: <strong class="pdp__variant-value">M</strong></legend>
      <div class="pdp__sizes">
        <button class="pdp__size">P</button>
        <button class="pdp__size is-selected" aria-pressed="true">M</button>
        <button class="pdp__size">G</button>
        <button class="pdp__size">GG</button>
        <button class="pdp__size">EXG</button>
      </div>
      <a class="pdp__size-guide" href="#guia-de-medidas">Ver guia de medidas</a>
    </fieldset>

    <p class="pdp__availability" data-state="sob-encomenda">
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true">
        <circle cx="12" cy="12" r="9"/><path d="M12 8v5l3 2"/>
      </svg>
      Feita sob encomenda: chega até 05 de agosto
    </p>

    <button class="btn btn--primary pdp__cta" type="button">Adicionar ao carrinho</button>

    <ul class="pdp__trust">
      <li>Frete grátis acima de R$299,99</li>
      <li>Troca grátis em até 30 dias</li>
      <li>Pagamento seguro via PagSeguro e PIX</li>
    </ul>

    <a class="pdp__whatsapp-link" href="https://wa.me/5500000000000">
      Dúvida sobre o tamanho? Fale no WhatsApp
    </a>
  </div>
</div>
```

```css
.pdp{
  display:grid;
  grid-template-columns:1.15fr 1fr;
  gap:56px;
  max-width:1120px;
  margin-inline:auto;
  padding:48px 24px;
  align-items:start;
}
.pdp__gallery-main{ width:100%; aspect-ratio:4/5; object-fit:cover; border-radius:16px; }
.pdp__thumbs{ display:flex; gap:10px; margin-top:12px; }
.pdp__thumb{ width:64px; height:80px; border-radius:8px; overflow:hidden; border:1px solid var(--border); opacity:.65; }
.pdp__thumb img{ width:100%; height:100%; object-fit:cover; }
.pdp__thumb.is-active{ opacity:1; border-color:var(--accent); }

.pdp__buybox{ position:sticky; top:24px; }
.pdp__breadcrumb{ font-size:.8125rem; color:var(--muted); margin-bottom:8px; }
.pdp__title{ font-size:1.75rem; line-height:1.2; margin:0 0 12px; }
.pdp__price{ font-size:1.5rem; font-weight:600; margin:0 0 24px; }

.pdp__variant{ border:none; padding:0; margin:0 0 24px; }
.pdp__variant legend{ font-size:.875rem; color:var(--muted); margin-bottom:10px; }
.pdp__variant legend strong{ color:var(--fg); }

.pdp__swatches{ display:flex; gap:10px; }
.pdp__swatch{
  width:36px; height:36px; border-radius:50%;
  background:var(--swatch); border:2px solid transparent;
  box-shadow:0 0 0 1px var(--border);
  cursor:pointer;
}
.pdp__swatch.is-selected{ border-color:#fff; box-shadow:0 0 0 2px var(--accent); }

.pdp__sizes{ display:flex; gap:8px; flex-wrap:wrap; }
.pdp__size{
  min-width:44px; height:44px; padding:0 12px;
  border:1px solid var(--border); border-radius:10px;
  background:transparent; font-size:.9rem; cursor:pointer;
}
.pdp__size.is-selected{ border-color:var(--accent); background:color-mix(in oklab, var(--accent) 10%, transparent); }
.pdp__size-guide{ display:inline-block; margin-top:10px; font-size:.8125rem; text-decoration:underline; color:var(--muted); }

.pdp__availability{
  display:flex; align-items:center; gap:8px;
  font-size:.875rem; color:var(--muted); margin:4px 0 20px;
}

.pdp__cta{ width:100%; padding:16px; font-size:1rem; }

/* faixa de confiança: logo abaixo do CTA, nunca no rodapé */
.pdp__trust{
  list-style:none; margin:16px 0 0; padding:0;
  display:flex; flex-direction:column; gap:8px;
  font-size:.8125rem; color:var(--muted);
}
.pdp__trust li{ display:flex; align-items:center; gap:8px; }
.pdp__trust li::before{
  content:""; width:14px; height:14px; flex-shrink:0;
  background:var(--accent); mask:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath d='M20 6L9 17l-5-5' fill='none' stroke='%23000' stroke-width='3'/%3E%3C/svg%3E") center/contain no-repeat;
}

/* WhatsApp: presente, mas visualmente subordinado ao CTA principal */
.pdp__whatsapp-link{
  display:block; margin-top:20px; text-align:center;
  font-size:.8125rem; color:var(--muted); text-decoration:underline;
}

@media (max-width:860px){
  .pdp{ grid-template-columns:1fr; gap:24px; }
  .pdp__buybox{ position:static; }
}
```

**Armadilhas:** empurrar frete/troca/pagamento para o rodapé é o erro estrutural mais comum, a pesquisa mostra que 71% dos compradores abandonam quando a política de devolução não está claramente visível na própria página do produto, não porque a política é ruim, mas porque ela é invisível no momento certo. Selo de confiança genérico demais (ícone de cadeado clichê, badge de "site 100% seguro" sem contexto) parece falso e reduz credibilidade em vez de aumentar. Exagerar no número de selos também prejudica: páginas com 1 a 3 tipos de sinal de confiança convertem 23% melhor que páginas sem nenhum, mas páginas com 7 ou mais tipos convertem 8% pior, o excesso lê como propaganda insistente. Esconder o valor da variante selecionada dentro de um dropdown fechado obriga o usuário a abrir para lembrar o que escolheu, sempre mostrar no `<legend>`. Seletor de cor por nome sem swatch visual força o usuário a adivinhar o tom.

**Fonte:** baymard.com/blog/current-state-ecommerce-product-page-ux; baymard.com/blog/footer-needs-return-shipping-links (71% abandonam sem política de devolução visível); userintuition.ai, "Trust UX: Badges, Proof, and the Research Behind Them" (curva de 1-3 sinais versus 7+ sinais).

---

### Comunicação de Prazo Sob Encomenda ("Feito à Mão")

**De onde veio:** Baymard Institute, pesquisa sobre data de entrega estimada (EDD) versus velocidade de frete genérica; prática de fulfillment para produtos sob encomenda.

**O que é:** produto sem estoque pronto e com prazo de produção real (a Caetana leva até 30 dias úteis) não deve tentar esconder ou suavizar esse prazo, isso é o oposto do que a pesquisa recomenda. O padrão certo é comunicar o prazo como parte da narrativa de artesania, não como desculpa por atraso: linguagem tipo "sua peça começa a ser feita quando você compra" em vez de "prazo de produção: até 30 dias úteis" seco; uma barra de progresso **simbólica** (não um rastreamento literal em tempo real, é um mapa mental das etapas: Corte, Costura, Acabamento, Envio) que aparece já na PDP antes da compra, preparando a expectativa; e o dado mais importante de todos, uma **data específica calculada**, não uma faixa vaga. A pesquisa do Baymard mostra que 75% dos compradores completam a compra com mais disposição quando veem uma data de entrega estimada (ex: "Chega até 05 de agosto") em vez de uma faixa de dias ("3 a 5 dias úteis"): a data concreta reduz a ansiedade de espera porque vira uma promessa mensurável, não uma estimativa genérica.

**Proporções e medidas observadas:** a barra de etapas fica visível na PDP, não só no email de confirmação; a data estimada aparece em pelo menos dois pontos, na PDP (antes de decidir comprar) e de novo no carrinho/checkout (reforçando a decisão); o cálculo soma o prazo de produção real aos dias úteis de frete, nunca subestime o prazo para parecer mais rápido, isso quebra a confiança para sempre quando o pedido atrasar.

**Esqueleto:**

```html
<div class="made-to-order">
  <p class="made-to-order__label">
    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true">
      <path d="M12 20c4-2 7-5 7-9a7 7 0 1 0-14 0c0 4 3 7 7 9Z"/><circle cx="12" cy="11" r="2.4"/>
    </svg>
    Feita sob encomenda, especialmente para você
  </p>
  <p class="made-to-order__desc">Sua bombacha começa a ser feita assim que o pedido é confirmado.</p>

  <ol class="made-to-order__steps">
    <li class="is-active">Corte</li>
    <li>Costura</li>
    <li>Acabamento</li>
    <li>Envio</li>
  </ol>

  <p class="made-to-order__eta">
    Previsão de entrega: <strong data-eta>até 05 de agosto</strong>
  </p>
</div>
```

```css
.made-to-order{
  border:1px solid var(--border); border-radius:14px;
  padding:20px; margin:20px 0;
}
.made-to-order__label{
  display:flex; align-items:center; gap:8px;
  font-weight:600; font-size:.95rem; margin:0 0 6px;
}
.made-to-order__desc{ font-size:.8125rem; color:var(--muted); margin:0 0 16px; }

.made-to-order__steps{
  display:flex; list-style:none; margin:0 0 16px; padding:0; gap:4px;
}
.made-to-order__steps li{
  flex:1; text-align:center; font-size:.75rem; color:var(--muted);
  padding-top:14px; position:relative;
}
.made-to-order__steps li::before{
  content:""; position:absolute; top:0; left:0; right:0; height:3px;
  background:var(--border); border-radius:2px;
}
.made-to-order__steps li.is-active::before{ background:var(--accent); }
.made-to-order__steps li.is-active{ color:var(--fg); font-weight:600; }

.made-to-order__eta{ font-size:.875rem; margin:0; }
.made-to-order__eta strong{ color:var(--accent); }
```

```js
// calcula uma data estimada real a partir do prazo de produção + frete,
// nunca mostrar uma faixa vaga tipo "até 30 dias úteis" quando dá pra calcular a data exata
function calcularDataEntrega(dataCompra, diasUteisProducao, diasUteisFrete) {
  const totalDiasUteis = diasUteisProducao + diasUteisFrete;
  const data = new Date(dataCompra);
  let adicionados = 0;
  while (adicionados < totalDiasUteis) {
    data.setDate(data.getDate() + 1);
    const diaSemana = data.getDay(); // 0 = domingo, 6 = sábado
    if (diaSemana !== 0 && diaSemana !== 6) adicionados++;
  }
  return data.toLocaleDateString('pt-BR', { day: '2-digit', month: 'long' });
}

document.querySelectorAll('[data-eta]').forEach((el) => {
  el.textContent = `até ${calcularDataEntrega(new Date(), 20, 3)}`; // 20 dias úteis de produção + 3 de frete, ajustar por peça/CEP
});
```

**Armadilhas:** esconder o prazo de produção até o carrinho ou checkout, deixando o usuário descobrir só depois de decidir comprar, é o erro que mais gera arrependimento e pedido de cancelamento, a informação precisa estar na PDP antes da decisão. Usar linguagem de desculpa ("infelizmente o prazo é de até 30 dias") em vez de linguagem de processo artesanal transforma um diferencial (feito à mão, sob medida) em fraqueza percebida. Mostrar faixa de dias em vez de data específica é uma oportunidade perdida, a pesquisa mostra ganho real de conversão com data calculada. Prometer uma data otimista demais para parecer mais rápido é o erro mais caro de todos: a data virou uma promessa na cabeça do comprador, quebrar essa promessa destrói a confiança de forma desproporcional ao atraso real.

**Fonte:** baymard.com/blog/shipping-speed-vs-delivery-date (75% dos compradores completam a compra com mais disposição vendo EDD); wesupplylabs.com e thegood.medium.com sobre estimated delivery dates para itens sob encomenda.

---

## Carrinho e Checkout

### Checkout de Baixo Abandono

**De onde veio:** Baymard Institute, pesquisa de Cart & Checkout Usability (mais de 110 diretrizes, benchmark de 327 lojas de topo de faturamento nos EUA e Europa, 30.000+ elementos de checkout avaliados manualmente).

**O que é:** a taxa média de abandono de carrinho medida pelo Baymard fica em torno de 70%, e boa parte é evitável com estrutura, não com desconto. Os pilares do checkout de baixo abandono: **checkout como convidado é a opção mais proeminente** (botão maior, cor primária, posição mais alta), "criar conta" vira opção secundária ou link discreto, nunca o padrão pré-selecionado, hoje metade das lojas ainda erra isso e obriga ou empurra o usuário para criar conta antes de comprar; **campos mínimos**, sem duplicar email ou senha para confirmação, com preenchimento automático de endereço a partir do CEP; **indicador de progresso** (ex: Carrinho > Dados > Pagamento > Confirmação) para o usuário sempre saber quantos passos faltam, reduzindo a ansiedade de "quanto tempo isso vai levar"; **reforço de confiança exatamente no momento do pagamento**, ícones de segurança e das formas de pagamento aceitas (PagSeguro, PIX, cartão) posicionados perto do campo de pagamento, não no rodapé, porque é ali que a hesitação é maior; e **nenhum custo surpresa**, o valor do frete precisa aparecer antes da tela final, nunca só na confirmação.

**Proporções e medidas observadas:** indicador de progresso com no máximo 3 a 4 etapas nomeadas (mais que isso cansa visualmente); botão de "continuar como convidado" com prioridade visual clara sobre "entrar/criar conta" (peso de cor e posição, não só tamanho de fonte); resumo do pedido fixo ou sempre visível durante o preenchimento dos dados, nunca escondido atrás de um "ver resumo".

**Esqueleto:**

```html
<div class="checkout">
  <ol class="checkout__steps" aria-label="Etapas da compra">
    <li class="is-done">Carrinho</li>
    <li class="is-active">Dados</li>
    <li>Pagamento</li>
    <li>Confirmação</li>
  </ol>

  <div class="checkout__body">
    <section class="checkout__form">
      <h2>Como você quer continuar?</h2>
      <div class="checkout__guest-choice">
        <button class="btn btn--primary checkout__guest-btn" type="button">
          Continuar como convidado
        </button>
        <a class="checkout__login-link" href="#login">Já tenho conta, entrar</a>
      </div>

      <!-- campos mínimos: nome, email, CEP (endereço auto-preenchido), telefone -->
      <form class="checkout__fields">
        <label>Nome completo <input type="text" name="nome" required></label>
        <label>Email <input type="email" name="email" required></label>
        <label>CEP <input type="text" name="cep" inputmode="numeric" required></label>
        <label>Endereço <input type="text" name="endereco" readonly placeholder="Preenchido automaticamente"></label>
        <label>Número <input type="text" name="numero" required></label>
        <label>Telefone (WhatsApp) <input type="tel" name="telefone" required></label>
      </form>
    </section>

    <aside class="checkout__summary">
      <h2>Resumo do pedido</h2>
      <!-- itens do carrinho aqui -->
      <p class="checkout__line"><span>Subtotal</span><span>R$ 349,90</span></p>
      <p class="checkout__line"><span>Frete</span><span>Grátis</span></p>
      <p class="checkout__line checkout__line--total"><span>Total</span><span>R$ 349,90</span></p>

      <ul class="checkout__payment-trust">
        <li>Pagamento processado via PagSeguro</li>
        <li>PIX com confirmação instantânea</li>
        <li>Seus dados não ficam salvos na loja</li>
      </ul>
    </aside>
  </div>
</div>
```

```css
.checkout__steps{
  display:flex; list-style:none; gap:8px; margin:0 0 32px; padding:0;
  max-width:1120px; margin-inline:auto;
}
.checkout__steps li{
  flex:1; text-align:center; font-size:.8125rem; color:var(--muted);
  padding-bottom:10px; border-bottom:3px solid var(--border);
}
.checkout__steps li.is-done{ color:var(--fg); border-color:var(--accent); }
.checkout__steps li.is-active{ color:var(--fg); font-weight:600; border-color:var(--accent); }

.checkout__body{
  display:grid; grid-template-columns:1.4fr 1fr; gap:48px;
  max-width:1120px; margin-inline:auto; padding:0 24px 64px;
}

.checkout__guest-choice{ display:flex; flex-direction:column; gap:12px; margin-bottom:28px; }
.checkout__guest-btn{ width:100%; padding:16px; }
.checkout__login-link{ text-align:center; font-size:.8125rem; color:var(--muted); text-decoration:underline; }

.checkout__fields{ display:grid; gap:16px; }
.checkout__fields label{ display:flex; flex-direction:column; gap:6px; font-size:.8125rem; color:var(--muted); }
.checkout__fields input{
  padding:12px 14px; border:1px solid var(--border); border-radius:10px; font-size:.9375rem;
}

.checkout__summary{
  border:1px solid var(--border); border-radius:14px; padding:24px;
  align-self:start; position:sticky; top:24px;
}
.checkout__line{ display:flex; justify-content:space-between; font-size:.875rem; margin:0 0 8px; }
.checkout__line--total{ font-weight:700; font-size:1rem; border-top:1px solid var(--border); padding-top:12px; margin-top:12px; }

/* reforço de confiança no momento do pagamento, não no rodapé da página */
.checkout__payment-trust{
  list-style:none; margin:20px 0 0; padding:16px 0 0;
  border-top:1px solid var(--border);
  display:flex; flex-direction:column; gap:8px;
  font-size:.75rem; color:var(--muted);
}

@media (max-width:860px){
  .checkout__body{ grid-template-columns:1fr; }
  .checkout__summary{ position:static; order:-1; }
}
```

**Armadilhas:** forçar criação de conta antes de finalizar a compra é uma das causas mais citadas de abandono de checkout, sempre deixe "continuar como convidado" mais visível e maior que "criar conta". Esconder o valor do frete até a última tela quebra a confiança construída até ali, mesmo quando o frete é grátis, mostre isso cedo. Pedir campos redundantes (confirmar email, confirmar senha, CPF em formato livre sem máscara) aumenta erro de digitação e frustração. Sem indicador de progresso, o usuário não sabe se está no passo 2 de 4 ou perto do fim, e a incerteza por si só aumenta abandono. Tirar os selos de segurança e ícones de forma de pagamento justamente da tela de pagamento (empurrando pro rodapé do site) é desperdiçar o reforço de confiança no momento exato em que ele mais importa, selos de confiança perto do pagamento aumentam a conclusão em cerca de 12 a 17%.

**Fonte:** baymard.com/research/checkout-usability (70%+ de abandono médio, 110+ diretrizes, benchmark de 327 lojas); pesquisa Baymard sobre "checkout as guest" como opção mais proeminente; userintuition.ai sobre selos de confiança perto do pagamento (+12 a 17% de conclusão).

---

## Categoria e Listagem (PLP)

### PLP Curada por Mais Vendidos

**De onde veio:** Baymard Institute, pesquisa de Product Lists & Filtering (83 diretrizes, mais de 700 problemas de usabilidade catalogados em 19 lojas testadas).

**O que é:** filtro complexo (cor, tamanho, preço, ocasião, tecido, todos ao mesmo tempo) só compensa o custo de interface quando o catálogo é grande o bastante para gerar resultados vazios sem ele. Com poucas dezenas de itens em 2 categorias, como a Caetana, um filtro completo vira ruído: cada faceta adicional é mais uma chance de o usuário zerar o resultado e sentir que a loja "não tem nada". A pesquisa do Baymard mostra que **ordenação (sort)** costuma ser subaproveitada mesmo sendo mais simples de implementar e mais útil que filtro em catálogos pequenos: os 4 critérios de ordenação essenciais são "mais vendidos", "novidades", "menor preço" e "maior preço". Para um catálogo pequeno, a curadoria manual do lojista já resolve o que o filtro tentaria automatizar: "mais vendidos" como ordenação padrão da página, e um selo real (não decorativo) nos itens que de fato vendem mais, calculado a partir de dados reais de venda, nunca aplicado a esmo pra parecer popular.

**Proporções e medidas observadas:** grid de 2 a 4 colunas dependendo da tela, sem sidebar de filtro se o catálogo tem menos de ~50 itens (2 a 3 abas de categoria substituem a sidebar); seletor de ordenação único, visível no topo da grade, com "Mais vendidos" pré-selecionado; selo de mais vendido aplicado a no máximo 10 a 15% dos itens da categoria (se aplicado a metade do catálogo, o selo perde qualquer significado).

**Esqueleto:**

```html
<div class="plp">
  <header class="plp__header">
    <nav class="plp__tabs" aria-label="Categorias">
      <a class="plp__tab is-active" href="#bombachas">Bombachas</a>
      <a class="plp__tab" href="#vestidos">Vestidos</a>
    </nav>
    <label class="plp__sort">
      Ordenar por
      <select>
        <option selected>Mais vendidos</option>
        <option>Novidades</option>
        <option>Menor preço</option>
        <option>Maior preço</option>
      </select>
    </label>
  </header>

  <div class="plp__grid">
    <article class="plp__card">
      <div class="plp__card-media">
        <img src="bombacha-terracota.jpg" alt="Bombacha terracota Estilo de Campo">
        <span class="plp__badge">Mais vendido</span>
      </div>
      <h3 class="plp__card-title">Bombacha Terracota</h3>
      <p class="plp__card-price">R$ 349,90</p>
    </article>

    <article class="plp__card">
      <div class="plp__card-media">
        <img src="bombacha-azul.jpg" alt="Bombacha azul marinho Estilo de Campo">
      </div>
      <h3 class="plp__card-title">Bombacha Azul Marinho</h3>
      <p class="plp__card-price">R$ 349,90</p>
    </article>
    <!-- ...repetir para o restante do catálogo... -->
  </div>
</div>
```

```css
.plp{ max-width:1120px; margin-inline:auto; padding:32px 24px 64px; }
.plp__header{
  display:flex; justify-content:space-between; align-items:center;
  margin-bottom:24px; flex-wrap:wrap; gap:16px;
}
.plp__tabs{ display:flex; gap:24px; }
.plp__tab{ font-size:.9375rem; color:var(--muted); padding-bottom:8px; border-bottom:2px solid transparent; }
.plp__tab.is-active{ color:var(--fg); border-color:var(--accent); font-weight:600; }

.plp__sort{ font-size:.8125rem; color:var(--muted); display:flex; align-items:center; gap:8px; }
.plp__sort select{ border:1px solid var(--border); border-radius:8px; padding:8px 10px; }

.plp__grid{
  display:grid;
  grid-template-columns:repeat(auto-fill, minmax(240px, 1fr));
  gap:24px;
}
.plp__card-media{ position:relative; border-radius:14px; overflow:hidden; aspect-ratio:4/5; }
.plp__card-media img{ width:100%; height:100%; object-fit:cover; }

/* selo de mais vendido: real, não decorativo, só aplicado via marcação manual/dado de venda */
.plp__badge{
  position:absolute; top:12px; left:12px;
  background:var(--accent); color:#fff;
  font-size:.6875rem; font-weight:600;
  padding:5px 10px; border-radius:999px;
}

.plp__card-title{ font-size:.9375rem; margin:12px 0 4px; }
.plp__card-price{ font-size:.9375rem; font-weight:600; margin:0; }
```

**Armadilhas:** aplicar o selo "mais vendido" em quase todo item da vitrine (ou em todos) é o equivalente comercial do badge decorativo genérico banido no restante do design-dna, ele precisa ser verdade e raro para funcionar. Construir uma sidebar de filtro completa (cor, tamanho, preço, tecido) para um catálogo de 20 a 40 peças é engenharia de interface sem retorno de navegação real, e ainda cria risco de resultado vazio ("nenhum produto encontrado") que não existiria sem o filtro. Deixar a grade sem nenhuma ordenação padrão (a ordem crua de cadastro no banco) joga a curadoria fora, "mais vendidos" como padrão é o que aproveita o trabalho de curadoria que o lojista pequeno já faz manualmente.

**Fonte:** baymard.com/research/ecommerce-product-lists; baymard.com/blog/ecommerce-product-lists-report-and-benchmark (83 diretrizes, 700+ problemas em 19 lojas testadas, 4 critérios essenciais de ordenação).

---

## Canais Paralelos e Prova Social

### WhatsApp como Canal Paralelo de Venda

**De onde veio:** prática de mercado consolidada em ecommerce brasileiro pequeno (WooCommerce com plugin de WhatsApp, Nuvemshop, Yampi), não um estudo formal e específico do Nielsen Norman Group sobre este canal; o princípio estrutural por trás, porém, vem do modelo hub-and-spoke de atendimento do NN/g: o canal de suporte precisa estar acessível de qualquer ponto da jornada sem competir com a tarefa principal em andamento.

**O que é:** em catálogo pequeno sob encomenda, é comum e eficaz ter o WhatsApp como canal paralelo ao carrinho tradicional, seja para tirar dúvida de tamanho antes de decidir, seja para fechar a venda diretamente com um vendedor quando o cliente prefere esse caminho. A regra de ouro de UI é: **o WhatsApp nunca compete visualmente com o CTA principal de compra**. Isso significa peso visual sempre subordinado, seja como link de texto discreto logo abaixo da faixa de confiança na PDP ("Dúvida sobre o tamanho? Fale no WhatsApp"), seja como botão flutuante posicionado de forma que nunca sobreponha o `sticky add-to-cart` no mobile (ver receita própria mais abaixo).

**Proporções e medidas observadas:** botão flutuante com 48 a 56px de diâmetro, ancorado no canto inferior direito, com margem de segurança acima da barra fixa de compra em mobile (nunca sobrepor); link inline em tamanho de texto secundário (.75 a .8125rem), cor neutra/muted, nunca a cor de acento reservada para o CTA de compra.

**Esqueleto:**

```html
<!-- variante flutuante: fica fora do fluxo de compra, some quando a barra sticky de compra aparece no mobile -->
<a class="whatsapp-fab" href="https://wa.me/5500000000000?text=Oi!%20Tenho%20uma%20d%C3%BAvida%20sobre%20um%20produto"
   aria-label="Falar no WhatsApp" target="_blank" rel="noopener">
  <svg width="26" height="26" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
    <path d="M12 2a10 10 0 0 0-8.6 15L2 22l5.2-1.4A10 10 0 1 0 12 2Z"/>
  </svg>
</a>
```

```css
.whatsapp-fab{
  position:fixed;
  right:20px;
  bottom:20px; /* na presença do sticky add-to-cart mobile, sobe para bottom: calc(72px + 20px), ver receita de sticky */
  width:52px; height:52px;
  display:grid; place-items:center;
  background:#25D366; color:#fff;
  border-radius:50%;
  box-shadow:0 8px 20px -6px rgba(0,0,0,.35);
  z-index:40; /* abaixo do z-index da barra sticky de compra, nunca acima */
  transition:transform .2s ease;
}
.whatsapp-fab:hover{ transform:scale(1.06); }

@media (prefers-reduced-motion: reduce){
  .whatsapp-fab{ transition:none; }
}
```

```html
<!-- variante inline: dentro da própria buy-box, sempre depois da faixa de confiança, nunca antes do CTA de compra -->
<a class="pdp__whatsapp-link" href="https://wa.me/5500000000000">
  Dúvida sobre o tamanho? Fale no WhatsApp
</a>
```

**Armadilhas:** colocar o botão flutuante de WhatsApp na mesma posição vertical do sticky add-to-cart mobile faz os dois se sobreporem ou o usuário clicar no errado por engano, sempre reserve espaço vertical entre os dois elementos fixos. Deixar o botão de WhatsApp do mesmo tamanho, cor sólida e destaque do CTA de "comprar" faz o cliente hesitar sobre qual é a ação principal da página, o WhatsApp é sempre a alternativa, nunca o par do CTA. Oferecer só o caminho de WhatsApp, sem nenhum caminho de compra direta no site, joga fora a automação que o próprio carrinho oferece e sobrecarrega o atendimento manual desnecessariamente.

**Fonte:** padrão de mercado de plugins de WhatsApp para WooCommerce/Nuvemshop/Yampi em ecommerce brasileiro pequeno (prática consolidada, não estudo formal); nngroup.com/articles/customer-service-model (modelo hub-and-spoke de atendimento, base estrutural do princípio de não competir com a tarefa principal).

---

### Prova Social Sem Reviews ("Clientes Reais")

**De onde veio:** pesquisa agregada sobre conteúdo gerado por usuário (UGC) como sinal de confiança (Yotpo, WiserNotify), combinada com o princípio de restrição de sinais de confiança do Baymard (1 a 3 tipos convertem melhor que 0 ou que 7+).

**O que é:** quando a loja ainda não tem avaliações formais (nenhuma nota, nenhum review de plataforma), a saída **não é fingir** com um widget de estrelas zerado carregado com 5 estrelas por padrão, isso é o dark pattern mais citado de ecommerce novo, e sim construir uma seção de "Clientes Reais" com o mesmo peso visual e o mesmo espaço na página que uma seção de reviews teria: nome real, contexto real (cidade, ocasião de uso), foto real quando houver consentimento, tratados como conteúdo central da página, não como rodapé pequeno. A pesquisa de UGC mostra que boa parte dos compradores (mais da metade, em diferentes levantamentos) confia mais em foto real de cliente do que em foto profissional de still de produto, então essa seção não é um substituto fraco de reviews, é um tipo diferente de prova social com efeito real.

**Proporções e medidas observadas:** seção com peso de página inteira (não uma faixa pequena no rodapé), mínimo de 3 a 4 clientes reais por seção para não parecer isolado; foto quadrada ou retrato, citação curta (1 a 2 frases reais, nunca reescrita para soar como propaganda), nome e cidade/contexto, nunca nota numérica ou estrelas se essas notas não existirem de verdade.

**Esqueleto:**

```html
<section class="real-customers">
  <h2 class="real-customers__title">Quem já vestiu Caetana</h2>
  <div class="real-customers__grid">
    <figure class="real-customers__card">
      <img src="marina-cliente.jpg" alt="Marina usando a bombacha terracota">
      <blockquote>"Usei na Semana Farroupilha e recebi elogio o dia inteiro."</blockquote>
      <figcaption>Marina, Porto Alegre</figcaption>
    </figure>
    <figure class="real-customers__card">
      <img src="joana-cliente.jpg" alt="Joana usando o vestido gaúcho">
      <blockquote>"O tecido é mais fresco do que eu esperava para o calor de dezembro."</blockquote>
      <figcaption>Joana, Bagé</figcaption>
    </figure>
    <!-- adicionar conforme depoimentos reais forem chegando, nunca inventar -->
  </div>
</section>
```

```css
.real-customers{ max-width:1120px; margin-inline:auto; padding:64px 24px; }
.real-customers__title{ font-size:1.5rem; text-align:center; margin:0 0 32px; }
.real-customers__grid{
  display:grid;
  grid-template-columns:repeat(auto-fit, minmax(220px, 1fr));
  gap:24px;
}
.real-customers__card{ margin:0; text-align:center; }
.real-customers__card img{
  width:100%; aspect-ratio:1; object-fit:cover; border-radius:14px; margin-bottom:16px;
}
.real-customers__card blockquote{
  margin:0 0 10px; font-size:.9375rem; line-height:1.5;
}
.real-customers__card figcaption{ font-size:.8125rem; color:var(--muted); }
```

**Armadilhas:** widget de avaliação com estrelas zeradas ou pré-preenchidas com nota alta antes de existir qualquer review real é enganoso e, dependendo da jurisdição, sujeito a questionamento por prática enganosa, nunca simule uma nota que não existe. Inventar depoimento ou usar foto de banco de imagens fazendo passar por cliente real é antiético e quebra a confiança de forma irreversível se descoberto, use só depoimento e foto reais com consentimento. Colocar a seção pequena, no rodapé, com peso visual de nota de rodapé, desperdiça o efeito, dê a ela o mesmo protagonismo de página que uma seção de reviews consolidada teria.

**Fonte:** yotpo.com, "11 Social Proof Marketing Examples" (conteúdo gerado por usuário como sinal mais persuasivo que foto profissional); wisernotify.com, "33 Shocking Social Proof Statistics"; userintuition.ai sobre a curva de 1-3 sinais de confiança sendo o ponto ótimo.

---

## Mobile Commerce

### Sticky Add-to-Cart Mobile

**De onde veio:** Baymard Institute, pesquisa de usabilidade mobile em páginas de produto; testes A/B documentados por consultorias de otimização de conversão (thegood.com, growthrock.co).

**O que é:** em tela pequena, assim que o usuário rola a página para baixo (o que acontece na grande maioria das sessões mobile, a maior parte dos usuários rola além da posição original do botão de comprar), o seletor de variante e o CTA de compra somem da tela. Sem um mecanismo fixo, o usuário precisa rolar de volta para cima para comprar, uma ação contraintuitiva que a pesquisa aponta como fricção evitável e cara: testes mostram ganho de conversão mobile na faixa de 5 a 12% simplesmente por manter uma barra fixa no rodapé da tela com miniatura do produto, preço e o CTA sempre acessível.

**Proporções e medidas observadas:** barra fixa de aproximadamente 64 a 76px de altura; aparece só depois que o CTA original sai da viewport (não desde o carregamento da página, isso duplicaria o CTA sem necessidade); contém miniatura pequena do produto (40 a 48px), preço, atalho para trocar variante (abre o mesmo seletor da PDP, não duplica a interface) e o botão de comprar; nunca ocupa a mesma faixa vertical do botão flutuante de WhatsApp (ver receita anterior), os dois elementos fixos precisam de espaço reservado próprio.

**Esqueleto:**

```html
<!-- botão original na buy-box, ele é o "sujeito" observado pelo IntersectionObserver -->
<button class="btn btn--primary pdp__cta" id="original-cta" type="button">Adicionar ao carrinho</button>

<!-- barra fixa: some por padrão, aparece só quando o CTA original sai da tela -->
<div class="sticky-atc" id="sticky-atc" hidden>
  <img class="sticky-atc__thumb" src="bombacha-terracota-thumb.jpg" alt="">
  <div class="sticky-atc__info">
    <p class="sticky-atc__name">Bombacha Terracota</p>
    <p class="sticky-atc__price">R$ 349,90 · Tam. M</p>
  </div>
  <button class="btn btn--primary sticky-atc__cta" type="button">Comprar</button>
</div>
```

```css
.sticky-atc{
  position:fixed; left:0; right:0; bottom:0;
  display:flex; align-items:center; gap:12px;
  padding:10px 16px;
  background:var(--surface, #fff);
  border-top:1px solid var(--border);
  box-shadow:0 -8px 24px -12px rgba(0,0,0,.15);
  z-index:50; /* acima do botão flutuante de WhatsApp */
  transform:translateY(100%);
  transition:transform .25s ease;
}
.sticky-atc:not([hidden]){ transform:translateY(0); }

.sticky-atc__thumb{ width:44px; height:44px; border-radius:8px; object-fit:cover; }
.sticky-atc__info{ flex:1; min-width:0; }
.sticky-atc__name{ font-size:.8125rem; margin:0; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }
.sticky-atc__price{ font-size:.75rem; color:var(--muted); margin:0; }
.sticky-atc__cta{ padding:10px 20px; font-size:.875rem; white-space:nowrap; }

@media (min-width:860px){
  .sticky-atc{ display:none; } /* padrão é mobile-only: no desktop a buy-box já é sticky por conta própria */
}
@media (prefers-reduced-motion: reduce){
  .sticky-atc{ transition:none; }
}
```

```js
const originalCta = document.getElementById('original-cta');
const stickyAtc = document.getElementById('sticky-atc');

const io = new IntersectionObserver(([entry]) => {
  // a barra aparece exatamente quando o CTA original sai da viewport, nunca antes
  stickyAtc.hidden = entry.isIntersecting;
}, { threshold: 0 });

io.observe(originalCta);
```

**Armadilhas:** mostrar a barra fixa desde o carregamento da página, antes mesmo do CTA original sair da tela, duplica a ação de compra sem necessidade e polui a tela pequena, a barra só deve aparecer quando o original desaparecer da viewport. Deixar a barra sticky sobrepor o botão flutuante de WhatsApp (ou vice-versa) é o erro de composição mais comum quando as duas receitas são usadas juntas, sempre reserve espaço vertical exclusivo para cada elemento fixo e dê `z-index` maior à barra de compra, que é a ação primária. Colocar o CTA da barra fixa desabilitado sem nenhuma variante selecionada, sem explicar o motivo, deixa o usuário sem entender por que não consegue comprar, prefira abrir o seletor de variante ao tocar em "Comprar" se ainda faltar escolha.

**Fonte:** pesquisa de usabilidade mobile do Baymard Institute sobre páginas de produto (maioria das sessões mobile rola além da posição original do CTA); thegood.com, "How To Improve User Experience With A Sticky Add To Cart Button"; growthrock.co, "Sticky Add to Cart Button Example: Actual AB Test Results" (ganho de 5 a 12% em conversão mobile).

---

## Regra de montagem

Nenhuma peça de ecommerce usa todas as receitas deste arquivo de uma vez isoladas do resto do design-dna, elas se somam à direção visual escolhida (`apple-premium`, `editorial-minimal-mockup` etc.), nunca a substituem. A ordem de prioridade quando as duas coisas parecem conflitar é sempre a mesma: **mecânica de conversão vence estética**. Se o estilo escolhido pedir respiro generoso e um único CTA por dobra, mas a pesquisa deste arquivo pede selo de confiança visível logo abaixo do botão, o selo entra, só que desenhado com a mesma disciplina de cor única e tipografia limpa do resto do sistema, nunca como badge colorido genérico. Da mesma forma, catálogo pequeno nunca ganha filtro grande só porque "loja de verdade tem filtro", e produto sob encomenda nunca esconde o prazo real só porque "30 dias parece muito", a honestidade estrutural é o que faz a peça parecer loja de verdade em vez de arte bonita sem chão.
