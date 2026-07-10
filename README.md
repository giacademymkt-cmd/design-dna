<div align="center">

![design-dna](assets/banner.png)

**Skill do [Claude Code](https://claude.com/claude-code)** com o DNA de design pessoal do William: 7 registros visuais, 18 livros de receita, regras de qualidade e anti-slop, prontos pra qualquer agente desenhar peças premium sem precisar de direção manual.

</div>

## O que é isto

Não é um gerador genérico de LP. É um sistema de gosto, destilado da leitura de referências que o William curou (rondesignlab, iconlypro, code.xr e outras fontes de UI premium). Qualquer peça nova, seja landing page, dashboard, componente, post de social ou criativo de anúncio, deve sair como se tivesse vindo da mesma prancheta.

`SKILL.md` é o ponto de entrada e já traz tudo mastigado pra qualquer agente: direção geral, tabela de escolha de estilo, ritual de alinhamento antes de desenhar, modo Glow Up (pra melhorar site existente), regras globais, mapa da biblioteca de receitas e checklist final antes de entregar. Um agente que carregue essa skill não precisa de contexto adicional pra saber o que fazer.

## Instalar no Claude Code

Clone o repositório dentro da pasta de skills:

```bash
git clone https://github.com/giacademymkt-cmd/design-dna.git ~/.claude/skills/design-dna
```

Ou, se preferir manter o repositório em outro lugar e só linkar:

```bash
git clone https://github.com/giacademymkt-cmd/design-dna.git ~/algum-lugar/design-dna
ln -s ~/algum-lugar/design-dna ~/.claude/skills/design-dna
```

Depois de instalado, a skill é acionada automaticamente sempre que o pedido envolver criar, desenhar, redesenhar ou melhorar (`glow up`) uma peça visual.

---

## Os 7 registros visuais

Cada peça usa **um estilo por vez**, escolhido pela tabela de decisão do `SKILL.md`. As imagens abaixo são demos reais renderizadas a partir das regras de cada estilo (paleta, tipografia, componente assinatura), não mockups genéricos.

<table>
<tr><td width="50%">

![Soft Neumorphism Light](assets/style-light.png)

</td><td width="50%">

![Dark UI Lab](assets/style-dark.png)

</td></tr>
<tr><td>

### 1 · `soft-neumorphism-light`
Mockup de app mobile e SaaS claro: base off-white `#ECECEE`, cards brancos flutuando com sombra dupla difusa, acento único por peça (azul, verde, coral ou violeta), tudo dentro de um "palco" tracejado.

**Quando usar:** telas de app mobile (settings, navegação, perfil), bibliotecas de ícones/componentes, produto SaaS em light mode tátil.

</td><td>

### 2 · `dark-ui-lab`
Estética de dev-tool sobre fundo quase-preto `#0A0C0F`/`#111111`, superfícies elevadas `#161A1F`, glass translúcido, ícones 3D de vidro fosco e acentos vibrantes pontuais (teal `#2BD9B4`, azul, magenta). Microinteração como assinatura: o Botão Assinatura (idle → progresso → checkmark).

**Quando usar:** demo de dev-tool, showcase de componentes, dashboard premium noturno, comparativo bom vs ruim.

</td></tr>
</table>

<table>
<tr><td width="50%">

![Apple Premium](assets/style-apple.png)

</td><td width="50%">

![Editorial Minimal + Mockup Cinematográfico](assets/style-editorial.png)

</td></tr>
<tr><td>

### 3 · `apple-premium`
Refinamento extremo inspirado na linguagem de design da Apple. Contenção total: tipografia gigante e precisa (`-apple-system`), respiro generoso, alternância `#FFFFFF`/`#F5F5F7`, um único acento `#0071E3`, CTA pill, zero decoração que não carregue informação.

**Quando usar:** página de produto high-end, LP institucional, "estilo apple", o grau mais alto de sofisticação.

</td><td>

### 4 · `editorial-minimal-mockup`
Assinatura do rondesignlab: case de produto editorial premium. Grid suíço arejado, cards bento super-arredondados, gradiente aurora/mesh quente dentro de superfícies claras, acento neon/lime `#D9F500` usado sempre como sinal de dado, nunca decoração.

**Quando usar:** case study de produto/portfólio, LP de SaaS B2B, healthtech/fintech, showcase de UI com aura cinematográfica.

</td></tr>
</table>

<table>
<tr><td width="50%">

![Dev Tutorial: Demo + Código](assets/style-devtutorial.png)

</td><td width="50%">

![Showcase de Fluxo de App](assets/style-appflow.png)

</td></tr>
<tr><td>

### 5 · `dev-tutorial-code-showcase`
Formato dominante do code.xr: componente de UI real animado flutuando em cima sobre fundo claro, janela de editor de código estilo macOS embaixo com syntax highlight multicolor. Ensina o resultado e o "como" na mesma tela.

**Quando usar:** conteúdo educativo de dev/design pra Reels e carrosséis, documentação de design system, prova de microinteração com código real.

</td><td>

### 6 · `app-flow-showcase`
Formato de portfólio de UI/UX mobile: 2 a 3 mockups de celular lado a lado contando uma jornada completa (onboarding, home, detalhe/checkout) numa imagem só. Dois polos: light clean com acento azul único, ou dark quase-preto com acento saturado.

**Quando usar:** apresentar um app mobile mostrando o fluxo completo, formato Dribbble/Behance, posts de produto sem depender de vídeo.

</td></tr>
</table>

<table>
<tr><td width="50%">

![Carrossel Educativo Dev/Design](assets/style-carousel.png)

</td><td width="50%">

### 7 · `dev-carousel-explainer`
Carrossel educativo quadrado: slides numerados com badge azul de progresso, comparações antes vs depois com pills semânticas vermelho/verde, janela de código estilo macOS com anotações, fundo creme `#F7F1E6` unificado do primeiro ao último slide.

**Quando usar:** explicar um conceito de UX/dev em passos (problema, causa, solução, código, benefícios) num carrossel de Instagram, sem depender de vídeo.

<br>

> As regras que valem em **todos** os 7 registros: herói flutuante num palco limpo, hierarquia por cor (não por tamanho), um único acento por peça, base neutra, cantos generosos, microinteração como conteúdo, respiro generoso, zero travessão em qualquer texto.

</td></tr>
</table>

---

## Biblioteca de receitas

Além dos 7 registros visuais, a skill tem 11 livros de receita verificados, lidos **sob demanda** conforme a peça pedida. Destilados das melhores fontes do mundo em motion/visual (Emil Kowalski, Rauno Freiberg, Josh Comeau, Olivier Larose, Codrops, Cassie Evans, dissecação de Linear/Vercel/Stripe/Raycast/Apple) e em conversão/venda (Ogilvy, Cialdini, Kahneman, Baymard Institute, Nielsen Norman Group).

| Situação | Arquivo |
|---|---|
| Antes de animar qualquer coisa: regras de gosto (easing, duração, contenção, acessibilidade) | `references/motion-principios.md` |
| Peça com narrativa de scroll: reveals, parallax, pin, trilho horizontal | `references/motion-scroll.md` |
| Headline animada, palavra de destaque, hover de card/botão, spotlight | `references/motion-texto-cursor.md` |
| CTA com estados, formulário, contadores, toasts, loading, bento | `references/componentes-premium.md` |
| Estrutura de LP/página: hero, prova social, pricing, footer, empty state | `references/secoes-premium.md` |
| Headline, descrição de produto, CTA, prova social, qualquer copy de venda | `references/copywriting-conversao.md` |
| Escassez/urgência, prova social, ancoragem de preço, dark patterns proibidos | `references/vies-cognitivo-persuasao.md` |
| PDP, carrinho, checkout, categoria (PLP) de ecommerce | `references/ecommerce-especialista.md` |
| Navegação, formulário, catálogo, acessibilidade, mobile-first | `references/ux-interface-principios.md` |
| LP de venda longa: infoproduto, curso, stack de oferta, bônus, garantia, FAQ | `references/lp-venda-longa.md` |
| Receita base de springs e microinteração (legado curto) | `references/motion.md` |

**Regra que não se negocia:** os 5 livros de conversão/ecommerce/UX são leitura obrigatória antes de desenhar qualquer PDP, carrinho, checkout, categoria ou LP de venda. **Mecânica de conversão vence estética.**

## Modo Glow Up

A skill não serve só pra criar do zero: é o diretor de arte pra elevar uma página existente com a bagagem instalada. Gatilhos: "melhorar", "dar um glow up", "upar o design", "modernizar", "auditar o visual". Fluxo: ver o site de verdade (nunca diagnosticar de memória) → diagnóstico com três lentes (anti-slop, oportunidades da biblioteca, estrutura) → relatório priorizado → mostrar, não descrever (reconstrói a seção de maior impacto com o conteúdo real, antes vs depois) → identidade da marca é sagrada → página ao vivo é intocável sem aprovação.

## Anti-slop: proibido por padrão

O William rejeita explicitamente o uniforme de página genérica de IA. Reprovam a peça mesmo com todo o resto certo:

- Badge/chip/pill decorativo acima do headline
- Grid quadriculado ou dot-grid cobrindo o fundo
- Gradiente roxo-azul e orbs/blobs de glow nos cantos
- Emoji como ícone de feature
- Três cards idênticos ícone-título-texto
- Copy inflada ("Potencialize", "Revolucione", "Eleve seu negócio")
- Glass genérico repetido em tudo
- Hero centralizado com dois botões por reflexo (primário + ghost sem segunda ação real)
- Travessão (—) em qualquer texto, título ou legenda

## Checklist antes de entregar

- [ ] Um único acento vibrante? (conte os acentos, sério)
- [ ] Herói flutuando com sombra difusa num palco limpo?
- [ ] Ênfase do título feita por cor/peso, não por tamanho gigante?
- [ ] CTA com estados de interação funcionando?
- [ ] Zero travessão em qualquer texto?
- [ ] Zero badge/pill acima do headline, zero grid genérico, zero orb de gradiente?
- [ ] Copy concreta, sem palavras de hype?
- [ ] Responsivo (mobile primeiro nas LPs)?
- [ ] Parece um objeto desejável que alguém salvaria?

---

## Estrutura

```
SKILL.md                  # porta de entrada: direção, tabela de estilos, regras globais, checklist
assets/                    # banner + demos visuais de cada um dos 7 estilos (este README)
references/                # 18 livros de receita, lidos sob demanda conforme a peça
  ├─ apple-premium.md, dark-ui-lab.md, soft-neumorphism-light.md,
  │  editorial-minimal-mockup.md, app-flow-showcase.md,
  │  dev-tutorial-code-showcase.md, dev-carousel-explainer.md    → 7 estilos visuais
  ├─ motion*.md, componentes-premium.md, secoes-premium.md       → motion e componentes
  ├─ copywriting-conversao.md, vies-cognitivo-persuasao.md,
  │  ecommerce-especialista.md, ux-interface-principios.md,
  │  lp-venda-longa.md                                           → conversão e venda
evals/evals.json           # suite de avaliação da skill (prompts + asserções automáticas)
```

## Uso

Repositório de uso interno da equipe. Conteúdo reflete decisões de gosto e regras de negócio específicas do William; use como referência, não como padrão genérico de mercado.
