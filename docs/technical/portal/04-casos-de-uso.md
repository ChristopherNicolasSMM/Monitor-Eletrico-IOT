# Casos de uso do portal (v0.3)

**Estado:** PROPOSTO, ainda não testado. **UC-001** já possui detalhes em [05-casos-de-uso.md](../05-casos-de-uso.md).

## UC-002 — Validar e recuperar importação parcial

**Ator:** técnico. **RF:** RF02, RF09, RF10. **Pré-condição:** arquivo original selecionado.
**Fluxo principal:** (1) parser processa linhas; (2) registra inconsistências estruturais, CRC e tempo; (3) separa válidas, incertas e inválidas; (4) mostra integridade e cobertura; (5) técnico aceita dados recuperáveis com ressalvas; (6) importação guarda rastros e alertas.  
**Alternativos:** arquivo sem `000` vira sessão órfã; sem `999` é marcado como não formalmente encerrado.  
**Erros:** versão desconhecida, arquivo excessivo, CRC inválido, timestamp inconsistente; não executar conteúdo importado.  
**Pós-condição:** originais preservados, dataset parcial sinalizado.  
**Aceite:** AT-002-01 arquivo com linha truncada recupera linhas posteriores íntegras; AT-002-02 nenhum erro fica invisível; AT-002-03 arquivo duplicado não duplica observações.

## UC-003 — Analisar uma campanha elétrica

**Ator:** técnico. **RF:** RF01, RF05, RF08. **Pré-condições:** sessão importada, tensão nominal/configuração definidas e registradas.  
**Fluxo principal:** (1) selecionar campanha; (2) validar parâmetros; (3) calcular séries de grandezas válidas e cobertura; (4) detectar eventos segundo configuração versionada; (5) produzir indicadores, gráficos e evidências; (6) gravar snapshot da análise.  
**Alternativos:** ausência de CT remove métricas de carga; RTC inválido restringe análise temporal; arquivo com lacunas apresenta cobertura parcial.  
**Erros:** falta de dados válidos impede métrica e apresenta 'não determinado'; configuração inadequada pede revisão.  
**Pós-condição:** conjunto de resultados reprodutível por hash, versão e parâmetros.  
**Aceite:** AT-003-01 timeout PZEM isolado não vira apagão; AT-003-02 `NA` não vira zero; AT-003-03 gaps não são preenchidos artificialmente; AT-003-04 análise repetida com mesmos dados/parâmetros gera mesmos resultados.

## UC-004 — Investigar ocorrência e evidências

**Ator:** técnico. **RF:** RF08, RF10. **Pré-condição:** campanha analisada.  
**Fluxo principal:** (1) filtrar evento; (2) abrir detalhe; (3) observar regra, início/fim ou incerteza; (4) examinar contexto temporal; (5) localizar arquivo, linha e seq; (6) exportar recorte ou marcar hipótese para relatório.  
**Alternativos:** evento aberto sem fim comprovado mostra duração limitada/incompleta; relógio duvidoso sinaliza incerteza.  
**Erros:** registros corrompidos continuam acessíveis na auditoria, excluídos de indicadores.  
**Aceite:** AT-004-01 cada finding tem record_refs; AT-004-02 regras e limiares são exibidos; AT-004-03 o detalhe não inventa duração para evento aberto.

## UC-005 — Consultar visão simplificada do cliente

**Ator:** técnico ou cliente autorizado (apresentação). **Pré-condição:** análise disponível.  
**Fluxo:** (1) selecionar visão Cliente; (2) exibir síntese, gráfico básico, principais eventos e cobertura; (3) orientar próximos passos; (4) abrir relatório executivo.  
**Alternativo:** cobertura baixa ou anomalia de relógio gera aviso destacado.  
**Pós-condição:** nenhuma alteração na análise.  
**Aceite:** AT-005-01 os números coincidem com a visão técnica; AT-005-02 limitações não desaparecem; AT-005-03 linguagem não atribui culpa sem evidência.

## UC-006 — Emitir relatórios executivo e técnico

**Ator:** técnico. **Pré-condição:** análise versionada disponível e metadados de cliente revisados.  
**Fluxo:** (1) escolher perfil; (2) prévia com limitações; (3) confirmar dados identificáveis; (4) gerar PDF; (5) armazenar identificador e hash das fontes; (6) exportar.  
**Alternativos:** cliente sem metadados gera relatório anônimo ou solicita preenchimento; sessão parcial exibe ressalva obrigatória.  
**Erros:** falha do motor PDF preserva análise e apresenta erro sem criar documento vazio.  
**Aceite:** AT-006-01 números consistentes com snapshot; AT-006-02 PDF contém proveniência e versão; AT-006-03 relatório técnico inclui referência de evidências; AT-006-04 exportação funciona offline.

## UC-007 — Reprocessar campanha com novos limiares

**Ator:** técnico. **Pré-condição:** análise anterior preservada.
**Fluxo:** (1) selecionar snapshot; (2) alterar parâmetros; (3) obter novo `analysis_run_id`; (4) comparar resultados; (5) escolher versão para relatório.
**Erros:** parâmetros fora do domínio aceito impedem processamento.
**Aceite:** AT-007-01 original e análises anteriores não mudam; AT-007-02 resultados ficam vinculados aos respectivos limiares.

## Matriz de rastreabilidade

| Caso | Requisitos | Aceites |
|---|---|---|
| UC-001 | RF02 RF04 RF08 RF09 RF10 | AT-001-01 a 05 |
| UC-002 | RF02 RF09 RF10 | AT-002-01 a 03 |
| UC-003 | RF01 RF05 RF08 | AT-003-01 a 04 |
| UC-004 | RF08 RF10 | AT-004-01 a 03 |
| UC-005 | RF08 RF10 | AT-005-01 a 03 |
| UC-006 | RF08 RF09 RF10 | AT-006-01 a 04 |
| UC-007 | RF08 RF10 | AT-007-01 a 02 |
