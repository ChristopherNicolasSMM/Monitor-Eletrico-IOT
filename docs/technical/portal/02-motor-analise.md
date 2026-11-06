# 02 — Motor de análise elétrica

**Estado:** especificação v0.3, não implementada. **UC-003**, **UC-004**.

## Entradas e saídas

Entradas: dataset canônico validado, parâmetros da campanha (tensão nominal e ponto de medição), limiares/política de evento, configurações de sensores/CT, metadados de calibração e versão do algoritmo. Saídas: indicadores com qualidade/cobertura, eventos referenciados, hipóteses condicionais e dados prontos para gráficos.

### Grandezas disponíveis

| Grandeza | Origem | Unidade | Condição de validade |
|---|---|---|---|
| Tensão RMS | PZEM | V | Faixa e validade do módulo; não interpretar fora de 80–260 V como exata |
| Corrente | PZEM + CT | A | CT instalado e colocado em **um** condutor da carga correta |
| Potência ativa | PZEM + CT | W | CT presente, ligação e leitura válidas |
| Energia acumulada | PZEM + CT | kWh | Distinguir reset de contador, troca de campanha e gaps |
| Frequência | PZEM | Hz | PZEM atualizado e em condições especificadas |
| Fator de potência | PZEM + CT | adimensional | Disponível com CT e grandezas válidas |
| Estado de rede | Detector AC independente | presente/ausente/indeterminado | Fonte confiável e circuito validado |
| Bateria, RTC, SD | Telemetria ESP32 | conforme campo | Somente se hardware efetivamente suportar |

## Estatísticas básicas propostas

Tensão válida: mínimo/máximo, média e mediana, P05/P95, dispersão, histogramas e tendência por hora/dia; número de leituras, tempo coberto e duração das lacunas. Os valores **não** são usados como extremos de transientes entre aquisições.

Frequência: min/máx/média/percentis em observações válidas.

CT presente: corrente, potência, fator de potência, energia e intervalos de carga; nunca inferir consumo de carga não monitorada.

A agregação temporal não deve assumir continuidade entre duas leituras espaçadas por lacuna. Definir `max_sample_gap` em função do intervalo de amostragem real e idade do valor, e computar cobertura como soma de intervalos observados válidos, limitados pelo próximo registro e esse limiar. Sem clock confiável, degradar cobertura e sinalizar incerteza.

## Eventos e regras

### Taxonomia inicial

| Código | Condição | Regra de comprovação |
|---|---|---|
| EVT-AC-LOSS | Falta de rede | Detector AC isolado confirmando ausência |
| EVT-AC-RESTORE | Retorno de rede | Detector AC confirmando retorno |
| EVT-UNDERVOLT | Subtensão sustentada | Medições válidas abaixo do limiar configurado por duração mínima |
| EVT-OVERVOLT | Sobretensão sustentada | Medições válidas acima do limiar configurado por duração mínima |
| EVT-FREQ | Frequência fora do limiar | Medições válidas por período mínimo |
| EVT-SENSOR | Falha de sensor | Timeout/erro PZEM, **não** interrupção comprovada |
| EVT-DATA-GAP | Lacuna de aquisição | Sequência/tempo com cobertura insuficiente |
| EVT-RTC | Ajuste/anomalia do relógio | Bloco TIME_SYNC e/ou inconsistência temporal |
| EVT-POWER-BACKUP | Mudança para bateria | Telemetria disponível, não prova tensão AC |
| EVT-RESTART | Reinício inesperado | Nova abertura `000`; ausência de `999` anterior |

A classificação de afundamentos e sobretensões muito rápidos **não é suportada** nesta versão. Um detector binário de rede registra interrupção somente conforme sua resposta validada.

### Parâmetros versionados

`nominal_voltage_v`, `undervoltage_threshold_v`, `overvoltage_threshold_v`, `frequency_min_hz`, `frequency_max_hz`, `min_event_duration_ms`, `return_hysteresis_v`, `max_sample_gap_ms`, `measurement_policy_version`, `timezone_display`.

Limiar **não** será apresentado como limite regulatório por padrão; valor de tensão nominal, tolerâncias e método precisam de configuração explícita. Histérese e duração impedem oscilações espúrias na categorização. Anotações de ausência de leitura não podem prolongar evento automaticamente: evento fica `open/uncertain` ou encerra em última observação comprovada.

### Severidade

Classificação proposta: informativa, atenção, crítica e indeterminada. Severidade é função de limiar/duração/configuração e cobertura, **nunca** certeza da causa. O nível poderá ser revisado no planejamento.

## Hipóteses e causalidade

Exemplos de hipóteses condicionais permitidas:
- Queda de tensão coincidente com aumento de corrente da mesma carga: investigar partida ou corrente de entrada, se amostragem temporal permitir correlação.
- Subtensão sustentada: investigar instalação, condutores, conexões, cargas e ponto de fornecimento.
- Interrupções confirmadas: investigar histórico da instalação e fornecimento.

Não afirmar 'concessionária causou', 'motor causou' ou 'rede conforme' sem base independente. Correlação não implica causalidade. Não alegar captura de eventos abaixo da resolução observada.

## Modelo de evidência

`Finding(id, category, severity, time_start, time_end, summary, metrics, record_refs[], rule_version, confidence, caveats[])`

Cada indicador e evento conserva seus `record_refs` (arquivo, linha, seq), critério aplicado e versão de cálculo; relatório técnico permite abrir registros sustentadores. Dados inválidos são visíveis na auditoria e excluídos dos cálculos onde inadequados, sem serem apagados.

## Reprodutibilidade

O motor deve produzir mesmos resultados ao importar os mesmos arquivos com a mesma versão de algoritmo e configuração. Reprocessar depois de mudar limiares gera nova `analysis_run`, sem sobrescrever a anterior. Salvar hash de entradas, versão e parâmetros.

## Testes mínimos

- Queda AC confirmada vs timeout PZEM isolado.
- Subtensão acima/abaixo de duração mínima com histérese.
- Lacunas grandes sem falsa imputação.
- Repetição de amostra obsoleta sem inflar cobertura.
- Corrente `NA` por ausência de CT.
- Reinício de energia acumulada sem energia negativa.
- Ajuste RTC com salto de tempo.
- Logs sintéticos determinísticos com indicadores esperados.
