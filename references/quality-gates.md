# Gates de qualidade

Use estes gates no fim de `build` e `glow-up`. Eles não substituem julgamento visual: tornam a revisão reproduzível e impedem que acabamento esconda falhas funcionais.

## Como avaliar

Classifique cada gate como:

- `pass`: evidência observável e suficiente;
- `warn`: aceitável com ressalva registrada;
- `fail`: bloqueia entrega como pronta.

Corrija `fail` antes de entregar. Se uma ferramenta não estiver disponível, marque `warn` e diga qual verificação não ocorreu.

## Gate 1: intenção e conteúdo

- A ação principal é evidente sem depender de animação.
- Headline, subtítulo e CTA dizem coisas específicas.
- Preço, prazo, disponibilidade, requisito ou risco relevante não está escondido.
- Não existem logos, depoimentos, números, selos, escassez ou resultados inventados.
- Assets reais fornecidos pelo usuário têm prioridade sobre placeholders.
- A peça comunica o produto real; não herdou o produto fictício de uma referência.

Falha bloqueante: conteúdo enganoso, CTA ambíguo ou informação essencial ausente.

## Gate 2: coerência visual

- Uma direção estética domina a peça.
- Base, surface, text, muted, accent e status têm papéis claros.
- O acento dominante existe e não compete com decoração multicolorida.
- Status, syntax highlight e data viz ficam confinados à função que justificou a exceção.
- Tipografia forma uma hierarquia inequívoca.
- Radius, borda, sombra e glass variam por função, não por reflexo.
- Há um protagonista e os elementos secundários apoiam sua leitura.

Falha bloqueante: duas identidades cromáticas concorrentes, contraste insuficiente ou hierarquia que esconde a ação principal.

## Gate 3: anti-slop e originalidade

- Nenhum badge decorativo foi colocado acima do headline por hábito.
- Não há grid, dot-grid, orb ou glow genérico sem função.
- Não há gradiente multicolorido em texto.
- Features não são três cards clones quando a composição pede protagonismo.
- CTA secundário existe por função, não para completar um par visual.
- Ícones são coerentes e emojis não substituem iconografia.
- Não há travessão `—` na copy nova, título, metadata ou acessibilidade gerados pela skill; conteúdo obrigatório ou pré-existente do usuário não foi alterado silenciosamente.
- A peça extrai técnicas das referências sem copiar capa, copy, produto ou sequência.

Falha bloqueante: cópia reconhecível de uma referência ou padrão genérico que contradiz diretamente o contrato visual.

## Gate 4: responsividade

Verifique pelo menos:

- desktop amplo, por exemplo 1440 × 900;
- mobile estreito, por exemplo 390 × 844;
- uma largura intermediária quando houver grid ou navegação complexa.

Confirme:

- ausência de overflow horizontal;
- texto sem corte ou sobreposição;
- CTA alcançável e área de toque confortável;
- imagens e mockups mantêm proporção;
- ordem de leitura permanece lógica;
- componentes não dependem de hover para revelar conteúdo essencial.

Falha bloqueante: perda de conteúdo, CTA inacessível ou navegação quebrada em uma viewport principal.

## Gate 5: acessibilidade e interação

- Estrutura semântica, idioma, título e viewport estão corretos.
- Imagens têm `alt` adequado; decorativas usam `alt=""`.
- Inputs têm label e mensagens de erro associadas.
- Teclado percorre controles em ordem útil.
- `:focus-visible` é perceptível e não depende só de cor.
- Contraste é suficiente nos estados normal, hover, focus e disabled.
- Motion respeita `prefers-reduced-motion` em CSS e, quando houver loop JS, também em JavaScript.
- Loading, sucesso e erro são anunciáveis quando a ação exigir.

Falha bloqueante: ação principal impossível por teclado, controle sem nome acessível ou conteúdo crítico ilegível.

## Gate 6: comportamento e performance

- A peça abre, compila ou renderiza no formato prometido.
- Console não registra erro relevante.
- CTAs, formulários, estados e navegação executam o fluxo principal.
- Listeners, animações e loops não continuam fora da viewport sem necessidade.
- Imagens usam dimensões e carregamento adequados.
- Dependências externas foram autorizadas e têm fallback razoável.
- Motion mantém leitura fluida em dispositivo comum.

Falha bloqueante: erro de runtime, fluxo principal quebrado ou animação que impede uso.

## Gate 7: entrega

- Arquivos finais estão no local informado.
- O formato entregue corresponde ao pedido: código, SVG, PNG, PDF, GIF ou vídeo.
- A resposta diferencia o que foi implementado, o que foi validado e o que ficou sem verificação.
- Não houve deploy, publicação ou alteração externa sem autorização.

## Ferramentas locais

Para HTML/CSS/JS, rode quando disponível:

```bash
python3 scripts/preflight.py caminho/do/arquivo.html
```

Para a integridade do pacote da skill:

```bash
python3 scripts/doctor.py .
```

Trate alertas heurísticos como pontos de inspeção. Um script pode detectar cores e padrões, mas não decide sozinho se a composição é boa.
