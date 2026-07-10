# Apple Premium (Refinamento Extremo) (`apple-premium`)

Registro de refinamento máximo inspirado na linguagem de design da Apple (apple.com, páginas de produto, keynotes). Não vem das referências do Instagram: é um módulo de conhecimento adicionado a pedido do William para quando ele quiser o grau mais alto de sofisticação. A essência é CONTENÇÃO: a página parece cara porque quase tudo foi removido. Tipografia gigante e precisa, espaço em branco como material de luxo, o produto como único protagonista, e nenhum elemento decorativo que não carregue informação.

**Quando usar:** Página de produto high-end, LP institucional, apresentação de app/serviço, ou sempre que o William disser "estilo apple", "extremamente refinado", "sofisticado", "minimalista premium". Também é o registro certo quando o produto em si é bonito e merece ser o herói absoluto.

## A mentalidade (leia antes dos tokens)

Cada seção é um CAPÍTULO com uma única ideia. A Apple não empilha features: ela apresenta uma afirmação grande, uma frase curta de apoio, uma imagem enorme do produto, e respira antes do próximo capítulo. Se uma seção tem três mensagens, são três seções. Na dúvida, corte.

## Tokens do estilo

- **Paleta:** `#FFFFFF` fundo principal; `#F5F5F7` fundo alternado de seção (o cinza-pérola Apple); `#1D1D1F` texto principal e seções dark "soft"; `#000000` seções dark de impacto; `#86868B` texto secundário; `#D2D2D7` hairlines e bordas; `#0071E3` acento único (CTA, links). **Nunca aplique gradiente multi-cor (tipo azul-roxo-rosa) em texto do headline**: benchmark real mostrou que isso quebra a regra de "um único acento" em 100% dos casos testados, mesmo descrito como "momento especial". Pra destacar a palavra-chave do headline, use a MESMA cor de acento em bloco sólido atrás do texto (`background: var(--accent); color: var(--accent-ink); padding: 0 .08em; border-radius: .12em;`), nunca `background-clip:text` com gradiente.
- **Tipografia:** System stack Apple-like: `-apple-system, BlinkMacSystemFont, "SF Pro Display", "SF Pro Text", "Helvetica Neue", Inter, sans-serif`. Headlines: peso 600-700, letter-spacing negativo (-0.015em a -0.03em), tamanhos grandes (56-96px desktop) com line-height apertado (1.05-1.08). Corpo: 17-21px, line-height ~1.47, peso 400. Texto secundário em `#86868B`, nunca em opacidade sobre cor. Hierarquia por tamanho E contenção: um headline afirma, um subtítulo de uma linha explica.
- **Layout:** Seções full-bleed empilhadas alternando `#FFFFFF` e `#F5F5F7` (ou dark). Texto centrado com max-width ~700-980px; visual do produto pode expandir até ~1440px. Padding vertical de seção generoso: 120-160px desktop, 80px mobile. Divisores hairline `1px #D2D2D7` quando precisar separar sem mudar fundo. Sem sidebar, sem densidade: uma coluna, um fluxo, uma história.
- **Componentes:** CTA pill (`border-radius: 980px`, padding confortável, fundo `#0071E3`, texto branco, sem borda). Link secundário no padrão Apple: texto azul + chevron ("Saiba mais >"), nunca botão ghost. Navegação minimal com frosted glass real: `backdrop-filter: blur(20px) saturate(180%); background: rgba(255,255,255,0.72)` (ou rgba escuro equivalente). Cards, quando existirem, são grandes, com radius ~28px, fundo sólido e sombra quase invisível.
- **Materiais:** Sombras discretas ao ponto de quase não existirem (`0 4px 24px rgba(0,0,0,0.06)`). Frosted glass SÓ em nav e overlays, nunca como decoração de card. Zero neon, zero glow, zero borda brilhante.
- **Motion:** Reveal no scroll com fade + translateY pequeno (12-24px), duração 0.6-0.8s, easing `cubic-bezier(0.25, 0.1, 0.25, 1)`. Nada de spring saltitante neste estilo: precisão em vez de personalidade. Hovers de 300ms com mudança sutil (escurecer CTA ~8%, elevar card 2-4px). Scroll-driven (produto que gira/monta conforme o scroll) é o toque de mestre quando couber.
- **Copy:** Frases curtas e declarativas. Headline com no máximo 6-8 palavras que AFIRMA ("Finanças, finalmente claras."), subtítulo de uma linha que explica. Zero hype words, zero exclamação em série, zero travessão (regra permanente do William). O tom é confiança silenciosa: quem é premium não grita.

## Anti-slop reforçado (neste estilo a régua sobe)

Tudo da seção anti-slop da SKILL.md vale em dobro aqui. Em especial: nenhum badge acima do headline, nenhum grid de fundo, nenhum orb de gradiente, nenhum emoji, nenhuma fileira de três cards idênticos. Se a página parecer "template SaaS de IA", ela reprovou por definição, mesmo bonita.

## Vale roubar (assinaturas do estilo)

- Headline gigante centrado com tracking negativo + subtítulo de UMA linha em `#86868B`
- Alternância de fundo `#FFFFFF` / `#F5F5F7` marcando capítulos sem precisar de divisores
- Seção dark `#000000` de impacto no meio da página light (o "momento cinema")
- CTA pill azul + link "Saiba mais >" como par padrão de ações
- Produto renderizado grande, centrado, com sombra suave, sem moldura nem palco decorado
- Destaque sólido (não gradiente) na palavra-chave do headline: mesmo acento único da página, em bloco atrás do texto
- Specs/números em tipografia enorme com rótulo pequeno embaixo (ex: "2x" gigante, "mais rápido" pequeno)
- Frosted glass na nav que revela o conteúdo passando por baixo

## Checklist específico do estilo

- [ ] Cada seção tem UMA ideia só?
- [ ] Headline afirma em até 8 palavras, com tracking negativo?
- [ ] Só existe UM acento (azul ou equivalente) na página inteira, em bloco sólido, nunca gradiente de texto?
- [ ] Padding vertical de seção >= 120px no desktop?
- [ ] Nenhuma sombra ou glow chamando atenção pra si?
- [ ] Motion preciso e calmo, sem bounce?
- [ ] A página parece cara pelo que NÃO tem?
