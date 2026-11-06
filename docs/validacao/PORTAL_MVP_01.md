# Entrega MVP 0.1 — Portal técnico

**Status:** implementado em branch de revisão; validação de execução ainda pendente.  
**Branch:** `feature/portal-tecnico-mvp`. **PR:** [#1](https://github.com/ChristopherNicolasSMM/Monitor-Eletrico-IOT/pull/1).

## Escopo entregue em código

- Portal único, **somente técnico**, responsivo, com identidade visual aprovada.
- Seleção/importação de arquivos `.log`, CRC32 experimental, hash de originais, avisos e sessões.
- Estatísticas iniciais, gráfico de tensão, eventos de tensão sustentada e detector AC declarado.
- Auditoria e tabela de registros.
- PDFs técnico e cliente, disponibilizados **apenas como modelos de exportação**, sem duas interfaces.
- CSV, simulador determinístico e testes unitários (não executados nesta revisão).

## Não implementado ainda

- Persistência de índice das importações (somente cache em memória; os originais ficam no disco).
- Cobertura temporal robusta; cálculos de duração total por evento de interrupção e variações mais complexas.
- Reprocessamento com parâmetros de análise via interface.
- PDF com gráficos e apêndices completos por evidência.
- Paginação completa dos registros na UI.
- Paridade metrológica, hardware em bancada, calibração e certificação.
- Múltiplos perfis de usuário ou interface cliente.

## Critérios para promover à branch principal

1. CI compilando código, testes unitários e geração/ingestão do log sintético.
2. Teste manual Windows e Linux conforme `portal/README.md`.
3. Conferência das saídas PDF técnico e cliente, CSV e gráficos offline.
4. Verificação de segurança local, limites de upload e comportamento com arquivo corrompido.
5. Revisão e congelamento do protocolo CRC32 entre firmware e portal.
6. Evidências de funcionamento registradas na pasta `docs/validacao/`.

Não confundir código publicado com resultado de testes comprovado.
