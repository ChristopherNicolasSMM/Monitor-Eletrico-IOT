---
name: documentacao-profissional
description: "Planejar, criar, revisar e manter documentação profissional de projetos de software, IoT e hardware; READMEs, manuais, documentação técnica, casos de uso, arquitetura C4, ADRs, validações, FAQs e identidade visual. Usar ao iniciar um projeto, documentar funcionalidades, preparar releases ou auditar documentação."
---

# Skill: Documentação Profissional

**Versão da skill:** 1.0.0  
**Idioma de saída:** pt-BR, salvo requisito explícito diferente.  
**Escopo:** reutilizável em qualquer repositório. Não presume stack, nome, licença, funcionalidades ou maturidade.

## Quando ativar

Ative esta skill ao criar ou revisar README, manuais, documentação técnica, diagramas, casos de uso, contratos, ADRs, roadmap/backlog, changelog, relatórios de testes e documentação de hardware. Use-a também em mudanças de funcionalidade que alterem operação, API, formato de arquivo, instalação ou segurança.

## Prioridade das regras

1. Segurança, veracidade, direitos e exigências explícitas do projeto.
2. Documentos de configuração específicos do repositório (`docs/PROJECT_DOCS_CONFIG.md`, se existir).
3. Esta skill.
4. Modelos de `references/`, adaptados ao contexto.

A skill é um padrão **mínimo**: adaptar com rigor crescente; não reduzir conteúdo apenas para cumprir um checklist.

## Entrada e auditoria antes de escrever

1. Identifique repositório, produto, público, uso principal, estado atual, branch e stack **a partir de evidências**, não suposições.
2. Inspecione README, árvore documental, manifestos, código, testes, releases, marca, screenshots e decisões já existentes.
3. Reutilize fontes canônicas; não duplique regras em documentos diferentes.
4. Classifique cada informação: **PROPOSTO**, **DECIDIDO**, **IMPLEMENTADO**, **TESTADO**, **VALIDADO EM CAMPO**, **DEPRECIADO**.
5. Apresente lacunas e riscos materiais; não chame protótipo de produto validado.
6. Se o projeto ainda não tem código, entregue documentação de projeto e fluxo planejado, nunca instalações falsas.

## Entregáveis documentais

### 1. README como porta de entrada

- Logo real/versionada ou título tipográfico provisório (não referenciar arquivo inexistente).
- Nome, slogan, problema real e proposta de valor em linguagem direta.
- Badges somente quando sustentados por recursos existentes; licença/CI/release jamais inventados.
- Resumo de funcionamento e diagrama **útil**, não decorativo.
- Recursos e status por capacidade; riscos e limites relevantes.
- Início rápido **executável e testado**, ou aviso explícito de que ainda não há execução.
- Índice navegável para manual, técnicos, operação, suporte, testes e contribuição.
- Capturas reais da versão correspondente, com fonte/legenda; mocks marcados como concept.
- Mínima repetição: detalhes residem em docs, não em README enorme.
- Autoria e licença somente conforme evidência do repositório.

### 2. Dois trilhos obrigatórios (quando aplicável)

`docs/technical/`: visão geral, arquitetura C4 proporcional, fluxos, contratos, modelo de dados, casos de uso, manutenção/expansão, segurança, ensaios, migrações e decisões.

`docs/manual/`: introdução, primeiros passos, operação por tarefa, interpretações, avisos, falhas comuns e FAQ. **Não** inserir C4, tabelas internas ou nomes de classes no manual final.

Projetos simples podem combinar capítulos, mas preservar **distinção explícita de público**. Para projetos IoT, separar ainda firmware/hardware, circuitos de referência, pinagem e normas, validação elétrica e firmware.

### 3. Casos de uso (obrigatório para funcionalidades importantes)

Cada caso de uso deve registrar:
- ID estável `UC-XXX`, nome, versão e status.
- Objetivo/valor e ator principal; atores/sistemas externos.
- Disparador, pré-condições, pós-condições e invariantes.
- Fluxo principal em passos numerados; fluxos alternativos e falhas com identificadores.
- Validação, permissões, riscos, regras de negócio, dados de entrada/saída.
- Requisitos vinculados (`RF-XXX`) e testes de aceite (`AT-XXX`).
- Evidências reais quando implementado, ou sinalização `não testado`.
- Diagramas Mermaid apenas se acrescentarem clareza.

Modelos em [references/CASO_DE_USO.md](references/CASO_DE_USO.md).

### 4. Arquitetura e contratos

- Contexto e contêiner C4; componentes somente quando necessários.
- Fluxos com Mermaid `flowchart`, `sequenceDiagram`, `stateDiagram-v2`; `erDiagram` quando houver entidades.
- Especificar limites, propriedades não funcionais, falhas, retries, dados persistidos e pontos de extensão.
- Contratos de API/protocolo versionados com campos, tipos, unidades, formato, obrigatoriedade, exemplos e erros.
- Compatibilidade e migrações descritas explicitamente; exemplos verificáveis.
- Para hardware, incluir isolação/aterramento/proteção, condições de operação e restrições de instalação; diagramas conceituais **não** são esquemas de ligação.

### 5. Manual operacional

Descrever ações pelo modo como o usuário navega e decide, não pela estrutura do código. Cada tarefa deve ter pré-condições, instruções reproduzíveis, resultado esperado, alternativa em falha e aviso de segurança relevante. Screenshots devem apontar para arquivos existentes, numerados, com legenda, versão e natureza (**real** ou **simulada**). Nunca gerar telas falsas como evidência.

### 6. Decisões e planejamento

- Manter ADRs/DECISOES com ID, data, contexto, opções, decisão, justificativa, consequências, pendências e status.
- Backlog por fase, entregável, dependências, validação, evidência e estado atual.
- Histórico de release/changelog distingue funcionalidade de documentação.
- Preferir links relativos e referências estáveis em vez de transcrever a mesma informação.

## Política de evidência

**Documentado ≠ implementado ≠ testado ≠ validado.**

- Somente afirmar `implementado` ao encontrar código ou artefato efetivo.
- Somente afirmar `testado` com teste executado ou evidência registrada, incluindo ambiente, versão e resultado.
- Somente afirmar `validado em campo` com evidências de operação real e escopo.
- Não converter simulações em testes de hardware.
- Não inventar comandos, screenshots, status de CI, certificações, protocolos ou URLs.
- Marcar `TODO` com responsável ou condição de desbloqueio quando possível.
- Descrever limites e incertezas nas áreas relevantes, sem esconder no rodapé.

## Procedimento de criação/revisão

1. **Auditar** o estado e registrar fatos e lacunas.
2. **Planejar** público, estrutura documental, links canônicos e critérios de aceite.
3. **Redigir** README, trilho técnico, trilho manual e registros de decisão conforme escala.
4. **Rastrear** cada requisito importante a casos de uso e testes.
5. **Checar** caminhos, Markdown, Mermaid, links, imagens, exemplos e terminologia.
6. **Verificar** comandos com ambiente compatível quando possível; não afirmá-los testados caso contrário.
7. **Publicar** preservando documentos e histórico existentes, com mudanças mínimas coerentes.
8. **Relatar** arquivos modificados, estado real, pendências e evidências.

## Checklist de qualidade antes de concluir

- [ ] README explica problema, funcionamento, público, status e limites.
- [ ] Índice orienta usuário e desenvolvedor com links válidos.
- [ ] Técnica e manual separados, cada qual com linguagem adequada.
- [ ] Casos de uso importantes incluem principal, alternativos, erros e aceite.
- [ ] Requisitos e contratos têm IDs, unidades, exemplos e versão quando cabível.
- [ ] Diagramas representam a arquitetura real ou estão sinalizados como proposta.
- [ ] Nenhuma funcionalidade imaginada aparece como implementada.
- [ ] Telas/figuras existentes com legenda, versão e origem; sem imagem quebrada.
- [ ] Riscos e segurança documentados proporcionalmente ao produto.
- [ ] ADRs, backlog e FAQs atualizados com a mudança.
- [ ] Sem segredos, tokens, senhas reais, endereços privados ou credenciais em exemplos.
- [ ] Caminhos, código, títulos e comandos conferidos.
- [ ] Mudanças incompatíveis contam com impacto e compatibilidade documentados.

## Referências e personalização

- [Caso de uso completo](references/CASO_DE_USO.md)
- [ADR e decisão arquitetural](references/ADR.md)
- [Checklist para revisão e aceite documental](references/REVISAO.md)
- [Perfil do projeto: exemplo portável](references/PROJECT_DOCS_CONFIG.example.md)

**Portabilidade:** copie **esta pasta inteira** para `.github/skills/documentacao-profissional/` em outro repositório. Crie `docs/PROJECT_DOCS_CONFIG.md` com os parâmetros locais. A skill não tem dependências de um projeto específico. Ferramentas/agentes que reconheçam skills por essa convenção poderão descobri-la; em outros ambientes, referencie explicitamente este `SKILL.md`. Publicar no GitHub não a instala automaticamente no ChatGPT ou em outras ferramentas.
