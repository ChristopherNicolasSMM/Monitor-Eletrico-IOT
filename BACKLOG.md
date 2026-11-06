# Backlog de implantação

**Estado:** planejamento. Documentação funcional do portal v0.3 concluída; hardware e software ainda não iniciados.

| Fase | Entrega | Evidência requerida | Estado |
|---|---|---|---|
| 0 | Padrão documental e identidade provisória | Links, documentos e decisões coerentes | Documentado |
| 1 | Fechamento elétrico seguro/BOM | Modelos, isolamento, alimentação e desenho revisados | Pendente |
| 2 | Contrato de log v1 congelado | CRC implementado em fixture, parser compatível e casos de truncamento | Pendente |
| 3 | Simulador de logs | Dados sintéticos determinísticos, eventos e erros controlados | Pendente |
| 4 | Portal: importação e validação | Parser/CRC, idempotência, arquivos originais e qualidade temporal | Especificado, implementação pendente |
| 4b | Motor de análise elétrica | Testes determinísticos, eventos, cobertura e rastreabilidade | Especificado, implementação pendente |
| 4c | Interface Cliente/Técnico | Mesmo resultado, filtros e evidências em duas visões | Especificado, implementação pendente |
| 5 | Relatórios executivo e técnico | Dois PDFs coerentes com a mesma análise, metadados, proveniência e ressalvas | Especificado, implementação pendente |
| 6 | Firmware na bancada | Aquisição, RTC, SD, power fail, watchdog | Pendente |
| 7 | Ensaios de bancada e campo | Comparação instrumental, falhas, autonomia, segurança | Pendente |
| 8 | Manual ilustrado e release | Capturas da versão real e instalador verificado | Pendente |

Não avançar para instalação em cliente sem critérios elétricos e de segurança demonstrados. Alterações incompatíveis em formatos de logs exigem versionamento e testes de migração.
