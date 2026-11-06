# Aceite e testes planejados para o portal

**Estado:** somente plano, nenhum teste executado.

| Grupo | Cenário sintético | Resultado obrigatório |
|---|---|---|
| Parser | Linhas válidas em ordem | 100% importado, origem preservada |
| Parser | Truncamento e CRC incorreto | Problemas listados por linha; registros válidos recuperáveis |
| Parser | Versão desconhecida | Sem interpretar arbitrariamente |
| Sessões | `000` sem `999` e posterior novo `000` | Sessões separadas e aviso de encerramento não formal |
| Tempo | DST/UTC, ajuste RTC, timestamp inválido | Não ordenar cegamente ou inventar continuidade |
| Integridade | Arquivo repetido | Não contaminar cálculo por importação duplicada |
| Rede | Detector AC ausente + timeout PZEM | **Sem afirmar interrupção** |
| Rede | Detector isolado acusa falta | Evento confirmado dentro da capacidade do detector |
| Energia | CT ausente / `NA` | Não mostrar zeros artificiais |
| Cálculos | Lacuna de vários minutos | Cobertura reduzida e intervalos desconhecidos |
| Eventos | Histerese e duração mínima | Não alternar evento por ruído de limiar |
| Visões | Alternância Cliente/Técnico | Exatamente os mesmos indicadores canônicos |
| Relatórios | Alterar limites após emitir PDF | PDF antigo continua rastreável ao snapshot anterior |
| Segurança | Arquivo malicioso/nome inválido | Rejeição segura e sem execução |
| Operação | Internet desconectada | Importação, análise e PDF operam localmente |

## Artefatos de teste futuros

`tests/fixtures/`: conjunto determinístico de logs válidos, truncados, duplicados, RTC inválido e detector AC vs PZEM. Os dados sintéticos devem ter gabarito externo com número esperado de eventos, mínimos/máximos e cobertura.

`tests/integration/`: API de importação e análise, idempotência, persistência de originais, PDF e exportações.

`tests/ui/`: navegação por teclado, responsividade, contraste, consistência de números nas visões.

`docs/validacao/`: versão, ambiente, dados de entrada, comando de execução, resultado e evidência por ciclo de testes. Não confundir resultado simulado com ensaio de rede elétrica.

## Gates

- G1: contrato de logs CRC/escape/versionamento fechado antes de parser de produção.
- G2: importação mantém arquivo original e relatório de problemas verificável.
- G3: análise determinística e correta diante de lacunas.
- G4: visões Cliente/Técnico compartilham o mesmo motor.
- G5: PDF inclui proveniência e ressalvas obrigatórias.
- G6: aplicativo offline empacotado testado em Windows/Linux antes de declarar suporte.
