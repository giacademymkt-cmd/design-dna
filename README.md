# design-dna

Skill do [Claude Code](https://claude.com/claude-code) com o DNA de design pessoal do William: estilos visuais, paletas, tipografia, motion, copy e regras de qualidade, destilados de referências curadas (rondesignlab, iconlypro, code.xr e outras fontes de UI premium).

Não é um gerador genérico de LP. É um sistema de gosto: qualquer peça nova (landing page, dashboard, componente, post de social, criativo de anúncio) deve sair como se tivesse vindo da mesma prancheta.

## Como usar

`SKILL.md` é o ponto de entrada e já traz tudo mastigado pra qualquer agente: direção geral, tabela de escolha de estilo, ritual de alinhamento antes de desenhar, modo Glow Up (pra melhorar site existente), regras globais, mapa da biblioteca de receitas e checklist final antes de entregar. Um agente que carregue essa skill não precisa de contexto adicional para saber o que fazer.

### Instalar no Claude Code

Clone o repositório dentro da pasta de skills:

```bash
git clone https://github.com/giacademymkt-cmd/design-dna.git ~/.claude/skills/design-dna
```

Ou, se preferir manter o repositório em outro lugar e só linkar:

```bash
git clone https://github.com/giacademymkt-cmd/design-dna.git ~/algum-lugar/design-dna
ln -s ~/algum-lugar/design-dna ~/.claude/skills/design-dna
```

Depois de instalado, a skill é acionada automaticamente pelo Claude Code sempre que o pedido envolver criar, desenhar, redesenhar ou melhorar (`glow up`) uma peça visual.

## Estrutura

```
SKILL.md              # porta de entrada: direção, tabela de estilos, regras globais, checklist
references/            # 18 livros de receita, lidos sob demanda conforme a peça
  ├─ apple-premium.md, dark-ui-lab.md, soft-neumorphism-light.md,
  │  editorial-minimal-mockup.md, app-flow-showcase.md, ...   → estilos visuais
  ├─ motion*.md, componentes-premium.md, secoes-premium.md    → motion e componentes
  ├─ copywriting-conversao.md, vies-cognitivo-persuasao.md,
  │  ecommerce-especialista.md, ux-interface-principios.md,
  │  lp-venda-longa.md                                        → conversão e venda
evals/evals.json        # suite de avaliação da skill (prompts + asserções automáticas)
```

## Os três registros visuais

- **light minimal-neumórfico** (`soft-neumorphism-light`) — SaaS/app claro, tátil
- **dark glass-tech** (`dark-ui-lab`) — dev-tool, dashboard escuro premium
- **apple-premium** — refinamento máximo, tipografia protagonista, sob demanda

Regras que valem em todos os registros: herói flutuante num palco limpo, hierarquia por cor (não por tamanho), um único acento por peça, base neutra (nunca cinza médio), cantos generosos, microinteração como conteúdo, respiro generoso, zero travessão em qualquer texto, e uma lista explícita de anti-slop (sem badge acima do headline, sem grid genérico, sem orbs de gradiente, sem copy inflada).

## Uso

Repositório de uso interno da equipe. Conteúdo reflete decisões de gosto e regras de negócio específicas do William; use como referência, não como padrão genérico de mercado.
