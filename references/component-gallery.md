# Galeria rápida de componentes vivos

Use esta galeria para escolher uma assinatura de interação antes de abrir o livro de 1.300 linhas `componentes-premium.md`. Os GIFs são previews; a implementação canônica está nas seções correspondentes do livro.

## Botão Assinatura

Preview: `../assets/components/button.gif`

Use em CTA assíncrono importante. A sequência é idle → progresso → sucesso; o container mantém geometria estável e o checkmark é desenhado depois do círculo. Garanta nome acessível e anúncio do resultado.

Leia em `componentes-premium.md`: botão com estados, barra de progresso e checkmark.

## Anel de foco premium

Preview: `../assets/components/focus.gif`

Use em formulário ou busca. O anel duplo aparece com `:focus-visible`, não em todo clique. Contraste e offset precisam sobreviver em tema light e dark.

Leia em `componentes-premium.md`: focus ring e campos de formulário.

## Esqueleto espelho

Preview: `../assets/components/skeleton.gif`

Use quando o layout final é previsível. O skeleton imita a forma e o peso do conteúdo real para evitar salto de layout; shimmer fica contido e respeita reduced motion.

Leia em `componentes-premium.md`: skeleton, loading e blur-up.

## Toast empilhado

Preview: `../assets/components/toast.gif`

Use para feedback temporário. A pilha sugere histórico, expande no hover e no foco e preserva acesso por teclado. Não esconda erro crítico num toast que desaparece.

Leia em `componentes-premium.md`: toast, pilha e feedback.

## Spotlight de borda

Preview: `../assets/components/spotlight.gif`

Use como detalhe local em busca, card ou input protagonista. O efeito acende a borda perto do cursor sem iluminar toda a superfície. Desative ou simplifique em reduced motion e touch.

Leia em `motion-texto-cursor.md`: cursor e spotlight; consulte `componentes-premium.md` para o componente.

## Bento animado

Preview: `../assets/components/bento.gif`

Use em features com pesos de conteúdo diferentes. A cascata reforça a hierarquia existente; não transforma três cards clones em bento apenas com `grid-span`.

Leia em `componentes-premium.md`: bento e entrada escalonada. Consulte `secoes-premium.md` para a narrativa da seção.

## Outros padrões do livro

O livro também cobre contadores, validação inline, barras de progresso, marquee, feed cíclico, imagem blur-up, listas, loading e estados vazios. Abra apenas a seção ligada ao componente escolhido.

Antes de implementar motion, leia `motion-principios.md`. Depois valide foco, teclado, reduced motion e estabilidade de layout com `quality-gates.md`.
