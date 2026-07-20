---
name: design-dna
description: >-
  Sistema de direção visual pessoal do William para criar, redesenhar, auditar ou refinar peças digitais premium. Use quando houver intenção visual explícita em pedidos de landing page, LP, site, seção, hero, dashboard, interface de app, componente visual, mockup, ecommerce, criativo de anúncio, post, carrossel, Reel, "no meu estilo", "capricha no design", "premium", "glow up", modernização ou auditoria visual. Use também quando ele pedir uma nova interface sem direção estética, pois este é o padrão visual dele. A skill decide estética, composição e função; aplica referências sem copiar; e valida coerência, conversão, acessibilidade, responsividade e motion. Não acione só porque aparecem as palavras app, componente, Apple ou premium: ignore correção lógica, debugging, performance sem mudança visual, implementação iOS/Apple técnica, texto puro, edição fotográfica isolada sem direção visual e tarefas com sistema visual explicitamente fechado.
---

# Design DNA v2

Transforme intenção em uma peça reconhecível como do William: clara, contida, funcional e com um momento visual memorável. O objetivo não é aplicar uma skin. É tomar decisões coerentes de hierarquia, composição, cor, tipografia, conteúdo e comportamento.

## Ordem de precedência

Quando regras colidirem, resolva nesta ordem:

1. Pedido explícito, marca e assets reais do usuário.
2. Acessibilidade, legibilidade, veracidade e integridade da interação.
3. Objetivo funcional, conteúdo e conversão.
4. Direção estética e formato selecionados.
5. Defaults globais desta skill.

Nunca sacrifique clareza, função ou identidade de marca para obedecer a um truque visual da biblioteca.

## Compatibilidade e composição com outras skills

Esta skill é dona das decisões visuais, não de todo meio de produção. Combine-a com a ferramenta ou skill especializada quando a entrega exigir frontend, imagem raster, vídeo, slides, PDF ou canvas. A skill especializada controla o formato e a implementação; a Design DNA fornece direção, tokens, composição e gates. Se o usuário já escolheu um design system fechado, preserve-o e use a Design DNA apenas para decisões que não o contradigam.

O filesystem é necessário para projetos locais. Python 3 habilita os validadores em `scripts/`. Browser ou renderizador melhora o QA; sem ele, faça inspeção de código e declare o limite.

## Escolha o modo de trabalho

| Modo | Quando | Profundidade padrão |
|---|---|---|
| `build` | Criar uma peça nova | Produção completa, com render e QA quando possível |
| `glow-up` | Melhorar algo existente | Diagnosticar, preservar o que funciona, implementar e comparar |
| `audit` | Revisar sem pedido de alteração | Somente leitura; evidências e prioridades, sem mutação |
| `concept` | Rascunho rápido, direção ou primeiras opções | Um registro estético e no máximo uma receita funcional |
| `ingest` | Aprender com novas referências | Extrair decisões, registrar proveniência e atualizar a biblioteca sem copiar |

Se o usuário não disser o modo, use `build` para algo novo e `glow-up` para algo existente. Não interrompa o fluxo para confirmar uma escolha reversível: declare a direção em uma atualização curta e prossiga. Peça decisão apenas quando duas direções mudarem materialmente custo, conteúdo ou arquitetura.

## Roteie em três eixos

Não trate formato e estética como a mesma coisa. Selecione um item por eixo quando ele for relevante.

### Eixo A: direção estética

| Direção | Melhor uso | Referência obrigatória |
|---|---|---|
| `soft-light` | SaaS claro, app amigável, UI tátil, biblioteca de componentes | `references/soft-neumorphism-light.md` |
| `dark-technical` | Dev-tool, automação, dashboard, produto técnico noturno | `references/dark-ui-lab.md` |
| `apple-contained` | Página de produto com refinamento máximo e extrema contenção | `references/apple-premium.md` |
| `editorial-signal` | SaaS B2B, fintech, healthtech, case e portfólio com dados | `references/editorial-minimal-mockup.md` |

### Eixo B: formato e composição

| Formato | Melhor uso | Referência obrigatória |
|---|---|---|
| `product-flow` | Jornada de app em 2 ou 3 telas, onboarding, UI/UX mobile | `references/app-flow-showcase.md` |
| `demo-code` | Resultado vivo + código, tutorial, Reel técnico | `references/dev-tutorial-code-showcase.md` |
| `explainer-carousel` | Carrossel educativo, antes/depois, passo a passo | `references/dev-carousel-explainer.md` |

Formatos herdam a direção estética selecionada. Um `product-flow` pode ser light ou dark. Syntax highlight e cores semânticas ficam confinados ao bloco que comunica código ou estado; eles não criam uma segunda identidade cromática para a peça.

### Eixo C: pacote funcional

Leia somente o pacote necessário. Use `references/INDEX.md` quando a tarefa exigir mais de uma receita.

| Necessidade | Pacote mínimo |
|---|---|
| Página/LP curta | `references/secoes-premium.md` + `references/copywriting-conversao.md` |
| LP longa de oferta | anterior + `references/lp-venda-longa.md` + `references/vies-cognitivo-persuasao.md` |
| Ecommerce/PDP | `references/ecommerce-especialista.md` + `references/ux-interface-principios.md` |
| Interface ou dashboard | `references/ux-interface-principios.md`; acrescente apenas as seções necessárias de `references/componentes-premium.md` |
| Motion | `references/motion-principios.md` primeiro; depois `references/motion-scroll.md` ou `references/motion-texto-cursor.md` |
| Componente interativo | `references/component-gallery.md`; então a receita específica em `references/componentes-premium.md` |

## Defina o contrato visual antes de implementar

Registre internamente, em poucas linhas:

- objetivo e ação principal;
- direção estética + formato + pacote funcional;
- composição protagonista;
- paleta por papéis e pares de contraste: `base`, `surface`, `text`, `muted`, `accent`, `accent-foreground`, `status.*`, `status.*-foreground` e `focus-ring`;
- tipografia e escala;
- componente assinatura;
- orçamento de motion;
- três coisas a evitar neste contexto.

Compartilhe com o usuário apenas uma frase útil, por exemplo: “Vou seguir editorial-signal, base off-white, lima como sinal de dado e um mockup financeiro assimétrico como protagonista.” Não transforme isso numa reunião quando o pedido já estiver claro.

## Fluxo de execução

1. **Inspecione a fonte de verdade.** Em projeto existente, leia stack, componentes, tokens, conteúdo e assets antes de propor mudança. Preserve funcionalidade e convenções locais.
2. **Selecione os três eixos.** Escolha uma direção dominante. Uma técnica secundária é permitida; uma segunda paleta completa não é.
3. **Carregue o mínimo necessário.** Leia a referência estética/formato escolhida e apenas as receitas funcionais que a peça realmente usa.
4. **Estruture conteúdo e hierarquia.** Resolva narrativa, ação principal e ordem das seções antes de decorar.
5. **Implemente a peça real.** Use conteúdo e assets fornecidos. Quando faltar algo essencial, crie um substituto honesto e claramente substituível, não um produto fictício copiado da referência.
6. **Renderize cedo.** Verifique uma viewport representativa antes de polir detalhes; depois confira mobile e estados.
7. **Faça uma segunda passada.** Corrija coerência cromática, ritmo, quebras, foco, reduced motion, overflow e detalhes genéricos.
8. **Entregue o artefato e a evidência.** Aponte arquivos, direção escolhida e o que foi validado.

## Como usar as referências

Extraia técnica, nunca conteúdo. Handles, paletas observadas e fichas de posts são evidência por trás dos tokens, não layouts para recriar. Não copie nome, copy, produto fictício, capa, sequência ou composição exata. Misture princípios em um cenário real e original.

Resolva o corpus visual nesta ordem:

1. referências anexadas ou indicadas pelo usuário;
2. variável `DESIGN_DNA_REFERENCE_ROOT`;
3. pasta irmã `../referencias-instagram/por-estilo/`;
4. previews empacotados em `assets/` e as referências textuais.

Não use caminhos absolutos fixos. A ausência do corpus externo não bloqueia a skill. Quando ele existir, inspecione no máximo 3 a 5 itens relevantes do registro selecionado; não carregue a biblioteca inteira. Para aprender novas referências, siga `references/reference-ingestion.md`.

## Gramática visual global

### Cor como sistema

- Comece por uma base neutra e escolha **uma família de acento dominante que esteja realmente presente**.
- Reserve o acento para CTA, dado, estado selecionado ou palavra-chave. Se tudo recebe acento, nada tem hierarquia.
- Não use gradiente azul-roxo-rosa em texto. Gradiente tonal da mesma família pode criar profundidade fora do texto; em `apple-contained`, prefira zero gradiente.
- Cores de `status` são exceções funcionais: vermelho para erro, verde para sucesso, amarelo para alerta. Mantenha-as locais, pequenas e semanticamente consistentes; não as repita como decoração.
- Syntax highlight pode ser multicolorido dentro do bloco de código. Visualização de dados pode usar escala adicional quando a leitura exigir, mas a navegação e os CTAs continuam no acento dominante.
- Em marca multicolorida, preserve a marca e eleja uma cor operacional para interação. As demais aparecem no logo ou em contextos justificados.

### Tipografia e composição

- Use hierarquia evidente por escala, peso, contraste e espaço. Cada registro decide qual desses fatores lidera.
- Prefira headlines curtas, específicas e com uma ideia por bloco. Não quebre a clareza só para encaixar uma palavra colorida.
- Crie um protagonista: produto, mockup, dado, interação ou composição editorial. Cards não são o protagonista por padrão.
- Use assimetria controlada, bento com pesos reais e respiro. Três cards idênticos “ícone + título + texto” são fallback, não direção premium.
- Use radius por função. Evite transformar todo texto, label e container em pill ou squircle.

### Interação e motion

- Toda ação importante deve revelar estado: hover/focus, active, loading, sucesso ou erro quando aplicável.
- Motion explica relação, mudança de estado ou narrativa. Não anime para preencher vazio.
- Use `prefers-reduced-motion`, foco visível, teclado e áreas de toque adequadas.
- Evite bounce/spring em páginas contidas; use spring apenas quando materialidade e feedback justificarem.
- Use glass localmente onde ele comunica camada, overlay ou foco. Mesmo quando o pedido exige vários cards glass, mantenha o restante da página sólido para o efeito não virar ruído.

## Anti-slop por padrão

Evite estes reflexos de design gerado por IA, salvo pedido explícito ou marca que os justifique:

- badge, chip ou pill decorativo acima de todo headline;
- orb roxo-azul, grid técnico ou dot-grid usado como fundo genérico;
- gradiente multicolorido em texto;
- CTA principal acompanhado de botão ghost sem função real;
- fileira de três cards clones;
- excesso de glass, glow, radius e sombras chamativas;
- ícones emoji quando existe ícone consistente;
- travessão `—` em copy nova gerada pela skill; a regra inclui `<title>`, metadata e texto acessível novos, mas conteúdo obrigatório ou já existente do usuário deve ser preservado até ele autorizar edição;
- hotlink aleatório, foto stock genérica ou placeholder quando existe asset real;
- números, logos, depoimentos, urgência ou prova social inventados.

## Contrato por artefato

### Web, React ou interface

Entregue código executável na stack existente. Preserve comportamento, use semântica, responsividade e acessibilidade. Em HTML único, evite dependência externa além do que o usuário autorizar. Rode `python3 scripts/preflight.py <arquivo>` quando disponível e trate seus achados como sinais, não como substituto do render.

### Peça estática, anúncio ou carrossel

Confirme formato por contexto ou use dimensões padrão explícitas no artefato. Respeite safe areas, legibilidade em tela pequena e sequência narrativa. Entregue SVG/PNG/PDF ou fonte editável conforme o pedido; não devolva HTML se o usuário pediu uma imagem final.

### Reel, GIF ou motion

Defina duração, beats, loop, primeiro frame e fallback estático. Mostre resultado e técnica quando for conteúdo educativo. Não prometa vídeo renderizado se só entregou storyboard ou código.

### Direção ou auditoria

Entregue uma decisão acionável: diagnóstico por prioridade, direção recomendada, tokens, composição e amostra suficiente para provar a solução. No modo `audit`, não edite arquivos.

## Glow Up

1. Capture o estado atual em desktop e mobile quando houver renderizador.
2. Liste problemas observáveis por impacto: objetivo/conversão, hierarquia, coerência, responsividade, acessibilidade e acabamento.
3. Preserve marca, conteúdo e funcionalidades que funcionam. Separe correção de redesign.
4. Se a direção for ambígua e cara de refazer, prove 2 ou 3 opções com o mesmo hero real; caso contrário, escolha, declare e implemente.
5. Compare antes/depois e registre o que mudou. Não publique nem faça deploy sem pedido explícito.

## Gate de qualidade antes de entregar

Leia `references/quality-gates.md` em produção ou Glow Up e verifique:

- objetivo e CTA continuam claros sem depender do efeito visual;
- paleta segue papéis e exceções sem criar uma segunda identidade;
- desktop e mobile não têm overflow, corte ou sobreposição;
- teclado, foco, contraste, alt/labels e reduced motion estão cobertos;
- estados interativos funcionam e não há erro de console;
- assets e conteúdo são reais ou honestamente marcados;
- a peça não copiou uma referência nem caiu nos padrões anti-slop;
- o artefato abre, compila ou renderiza no formato prometido.

Se não puder renderizar, diga isso na entrega e faça a inspeção de código disponível. Não alegue validação visual que não ocorreu.

## Formato da resposta final

Lidere com o resultado. Aponte os arquivos criados ou alterados, diga a direção escolhida em uma linha e resuma verificações reais. Evite recontar todo o processo.
