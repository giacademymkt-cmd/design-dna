# Linguagem de Motion

Framer Motion como lingua franca: springs elasticos (stiffness ~200 / damping ~20), whileHover com scale 1.05 e whileTap 0.95, transicoes de largura/opacity/translate curtas (duration ~0.4) e AnimatePresence para troca de estados. Ritmo tranquilo e em loop, tipo screen-recording de produto, com cursor animado guiando o olho ate o CTA. Nos cases premium, camera com dolly/parallax lento e desfoque seletivo sobre mockups em perspectiva.

## Receita padrão (Framer Motion / React)

```jsx
// Spring padrão do DNA
const spring = { type: "spring", stiffness: 200, damping: 20 }

// Interação padrão de botão/card
<motion.button
  whileHover={{ scale: 1.05 }}
  whileTap={{ scale: 0.95 }}
  transition={spring}
/>

// Troca de estados (idle -> loading -> sucesso)
<AnimatePresence mode="wait">
  <motion.span key={state}
    initial={{ opacity: 0, y: 6 }}
    animate={{ opacity: 1, y: 0 }}
    exit={{ opacity: 0, y: -6 }}
    transition={{ duration: 0.4 }}
  />
</AnimatePresence>
```

## Equivalente em CSS puro (páginas estáticas)

Quando a peça for HTML estático (deploy GI), traduza a mesma linguagem:

```css
.btn { transition: transform .2s cubic-bezier(.34,1.56,.64,1), box-shadow .2s ease; }
.btn:hover { transform: scale(1.05); }
.btn:active { transform: scale(.95); }
/* trocas de estado: transições de width/opacity/translate de ~0.4s */
/* revelar no scroll: IntersectionObserver + classe .visible, nunca bibliotecas pesadas */
```

Princípios: ritmo tranquilo e em loop (screen-recording de produto), o movimento guia o olho até o CTA, estados sempre com feedback (progresso com glow, checkmark de sucesso). Nos cases premium: parallax lento e desfoque seletivo sobre mockups em perspectiva.