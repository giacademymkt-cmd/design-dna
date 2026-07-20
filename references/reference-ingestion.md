# Protocolo de ingestão de referências

Use este protocolo quando o usuário fornecer imagens, vídeos, links, moodboards ou uma pasta para “alimentar” a Design DNA. O resultado deve enriquecer o sistema de decisão, não transformar a skill num arquivo de cópias.

## 1. Registre proveniência antes de analisar

Para cada lote, registre quando a informação estiver disponível:

- origem e autor/handle;
- URL ou caminho relativo;
- data de coleta;
- tipo de mídia;
- direito de uso conhecido, desconhecido ou apenas referência interna;
- direção estética, formato e função prováveis;
- confiança da classificação.

Não publique mídia de terceiros dentro do repositório quando os direitos não estiverem claros. Um manifesto com hash e metadados pode ser versionado sem redistribuir o arquivo.

## 2. Resolva o corpus sem caminho absoluto

Procure nesta ordem:

1. caminho informado pelo usuário;
2. variável `DESIGN_DNA_REFERENCE_ROOT`;
3. `../referencias-instagram/por-estilo/` em relação ao diretório da skill;
4. previews empacotados em `assets/`.

Nunca grave um caminho absoluto específico de máquina em `SKILL.md` ou nas referências portáteis.

## 3. Faça amostragem deliberada

Não leia o corpus inteiro por reflexo.

- Comece por 3 a 5 itens de um lote ou direção.
- Em carrossel, observe capa, um slide de desenvolvimento e fechamento.
- Em vídeo, observe primeiro frame, transição principal, estado final e loop.
- Amplie a amostra apenas quando houver contradição ou baixa confiança.
- Compare com o `corpus-profile.yaml` para não deixar o maior lote dominar todas as decisões.

## 4. Extraia em três eixos

### Direção estética

- base e contraste;
- paleta por papéis, não apenas lista de hex;
- tipografia e densidade;
- materiais: sólido, glass, grain, sombra, borda;
- nível de contenção.

### Formato e composição

- proporção e safe area;
- grid e ritmo;
- protagonista;
- sequência narrativa;
- enquadramento, crop e profundidade.

### Função

- ação que a peça conduz;
- componente ou estado demonstrado;
- padrão de conversão ou UX;
- papel do motion;
- riscos de acessibilidade ou dark pattern.

## 5. Separe técnica de conteúdo

Promova para a skill apenas princípios transferíveis. Exemplos:

- “estado idle → progresso → sucesso com checkmark desenhado” é técnica;
- “botão Uploading 68% do post X” é conteúdo específico e não deve virar template;
- “macro em perspectiva com depth of field” é técnica;
- o mesmo produto, copy e composição da referência são cópia.

Reescreva cada achado como decisão, motivo, uso e armadilha. Evite “vale roubar” sem explicar por que funciona e em qual contexto deixa de funcionar.

## 6. Decida onde o aprendizado vive

- Atualize um registro estético quando o aprendizado muda paleta, tipografia, material ou composição daquele registro.
- Atualize um formato quando o aprendizado muda sequência, proporção ou enquadramento.
- Atualize um pacote funcional quando traz código, UX, conversão ou motion reutilizável.
- Atualize `SKILL.md` apenas quando muda precedência, workflow ou regra global.
- Acrescente ao `design-registry.yaml` somente decisões estáveis e canônicas.

Não duplique a mesma regra em vários livros. Faça cross-link para a fonte canônica.

## 7. Valide antes de promover

Um aprendizado entra na V2 quando:

- aparece em mais de uma referência ou tem justificativa funcional forte;
- não contradiz marca, acessibilidade ou conversão;
- pode ser expresso sem copiar conteúdo;
- inclui exceções e contexto de uso;
- tem ao menos um exemplo original ou teste que demonstra transferência.

Quando for preferência ainda incerta, registre como hipótese e crie um eval holdout antes de torná-la regra global.

## 8. Atualize cobertura e testes

Depois da ingestão:

1. atualize contagens e lacunas em `corpus-profile.yaml`;
2. rode `python3 scripts/doctor.py .`;
3. acrescente ou refine um eval que teste transferência para outro produto;
4. compare contra a versão anterior e verifique se a regra não overfitou o exemplo de origem.
