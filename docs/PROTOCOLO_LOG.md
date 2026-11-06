# Protocolo de registro textual (proposta v0.1)

## Princípios

Um registro por linha, delimitado por `|`, fácil de recuperar e auditar. Arquivo UTF-8; separador decimal **ponto** para parsing independente do idioma; timestamp ISO 8601 UTC com milissegundos e campo de offset local opcional. Todos os tipos compartilham um envelope fixo.

Formato:

```text
|type|schema|device_id|session_id|seq|timestamp_utc|uptime_ms|payload|crc32|
```

- `type`: código de bloco com 3 dígitos.
- `schema`: versão do protocolo, ex. `1`.
- `device_id`, `session_id`: IDs sem caractere `|`.
- `seq`: contador monotônico na sessão; falhas/duplicações auditáveis.
- `timestamp_utc`: ex. `2026-11-06T17:48:01.123Z`; qualidade de RTC indicada no payload.
- `uptime_ms`: uptime desde boot; útil quando RTC é inválido.
- `payload`: pares `chave=valor` separados por `;`; codificar caracteres reservados; campos desconhecidos devem ser preservados pelo parser.
- `crc32`: checksum hexadecimal (8 dígitos) do conteúdo entre o primeiro e o último delimitador, excluído o campo crc; cálculo preciso será especificado e testado antes do firmware.

**Estes exemplos são ilustrativos, não uma especificação já implementada.** Todos os tipos aceitam expansão de payload com versionamento.

## Tipos de bloco

| Tipo | Significado | Quando |
|---|---|---|
| 000 | BOOT / abertura de sessão | A cada inicialização, mesmo após reset acidental |
| 100 | SAMPLE / telemetria | Periodicamente, somente valores atualizados ou marcados |
| 110 | EVENT_START | Início de condição anormal validada |
| 111 | EVENT_END | Fim de condição anormal validada |
| 120 | POWER_STATE | Rede presente/ausente/indeterminada |
| 130 | SENSOR_STATE | Estado PZEM, timeout, erro CRC/serial |
| 140 | SYSTEM_HEALTH | Bateria, alimentação, SD, RTC, reset, consumo interno se disponível |
| 200 | CONFIG | Snapshot de configuração e calibração |
| 210 | TIME_SYNC | Ajuste de relógio ou qualidade do timestamp |
| 900 | WARNING | Falta de espaço, buffer, dados inválidos, falha de gravação |
| 999 | SHUTDOWN | Encerramento formal solicitado, **não** emitido retroativamente após queda |

## Campos de medição propostos

`v_rms`, `i_rms`, `p_w`, `e_kwh`, `freq_hz`, `pf`, `v_nom`, `ct_present`, `pzem_valid`, `sample_age_ms`, `ac_state`, `battery_mv`, `battery_pct`, `supply_source`, `rtc_quality`, `sd_free_bytes`, `error_code`, `event_id`, `event_kind`, `event_duration_ms`, `min_v`, `max_v`, `firmware`, `config_hash` (quando disponíveis).

Usar `NA` quando não disponível, nunca inventar zero. Corrente, potência, energia e FP só têm significado conforme CT realmente instalado e topologia de medição. Não representar tensão fora da faixa do PZEM como valor confiável.

## Exemplos simplificados (CRC fictício omitido nesta prévia)

```text
|000|1|MEI-001|S-20261106-001|1|2026-11-06T17:48:01.000Z|0|reason=power_on;firmware=0.1.0;rtc_quality=valid|PENDING|
|200|1|MEI-001|S-20261106-001|2|2026-11-06T17:48:01.050Z|50|v_nom=127;interval_s=1;ct_present=false|PENDING|
|100|1|MEI-001|S-20261106-001|3|2026-11-06T17:48:02.000Z|1000|v_rms=107.21;i_rms=NA;p_w=NA;e_kwh=NA;freq_hz=59.9;pf=NA;ac_state=present;pzem_valid=true|PENDING|
|120|1|MEI-001|S-20261106-001|4|2026-11-06T17:49:00.100Z|59100|ac_state=absent;source=isolated_detector|PENDING|
|130|1|MEI-001|S-20261106-001|5|2026-11-06T17:49:01.000Z|60000|pzem_valid=false;error_code=timeout|PENDING|
|999|1|MEI-001|S-20261106-001|6|2026-11-06T18:00:00.000Z|719000|reason=user_requested;records=5|PENDING|
```

Na implementação, substituir `PENDING` pelo CRC calculado. Formatos de tempo, checksum e tolerância a perdas serão congelados por testes de compatibilidade.

## Política de escrita

- Telemetria periódica sugerida: 1 s (sujeita ao tempo real de atualização do PZEM).
- Eventos de interrupção e erros: gravar imediatamente quando constatados, sem bloquear aquisição.
- Buffer em RAM e flush frequente para limitar perda na falha abrupta.
- Particionar por sessão e, se necessário, por dia; não alterar registros originais na análise.
- Ao reiniciar, **nova sessão** `000`; ausência de `999` na sessão anterior evidencia encerramento não formal, mas não identifica sozinha a causa.
