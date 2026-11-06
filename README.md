# Monitor Elétrico IoT

Registrador portátil de comportamento da rede elétrica, com aquisição pelo ESP32-S3, medição PZEM-004T V3.0 100 A, relógio DS3231, registros em microSD e análise posterior em portal web local.

> **Estado:** planejamento e documentação, versão 0.1 (2026-11-06). Ainda não há hardware validado nem firmware implementado.

## Objetivo

Registrar durante pelo menos 7 dias variações sustentadas de tensão, corrente (quando instalada a sonda), potência, frequência, fator de potência e energia, além de falhas da alimentação. O dispositivo deve continuar registrando estados durante interrupções usando bateria, dentro de sua autonomia.

O produto é um **registrador experimental de tendências e eventos**, não um analisador de qualidade de energia certificado. O PZEM-004T mede dentro de sua faixa especificada de 80–260 V AC e não garante detecção de afundamentos rápidos, transientes ou surtos.

## Decisões já tomadas

- Controlador: ESP32-S3 N16R8, variante física a confirmar.
- Medição principal: PZEM-004T V3.0 100 A com transformador de corrente externo.
- Tempo: RTC DS3231 com bateria de retenção.
- Armazenamento: microSD integrado, se a placa realmente possuir slot; senão, leitor SPI 3,3 V externo.
- Backup: módulo UPS apropriado com célula 18650 recarregável, em vez de bateria alcalina de 9 V. Modelo exato ainda pendente.
- Aquisição e armazenamento offline, sem dependência de Wi-Fi.
- Log texto com **uma linha por registro**, delimitadores `|` e tipos de bloco. `000` abre sessão ao iniciar, `999` fecha somente no desligamento formal.
- Portal de análise no computador: **Python + FastAPI**; interface web local; análise Pandas/NumPy; gráficos Plotly; exportação PDF e CSV.

## Documentação

- [Requisitos e limites](docs/REQUISITOS.md)
- [Hardware e lista de materiais](docs/HARDWARE.md)
- [Protocolo de registros](docs/PROTOCOLO_LOG.md)
- [Portal de análise](docs/PORTAL.md)
- [Decisões e pendências](docs/DECISOES.md)

## Fluxo de uso

1. Preparar dispositivo, identificar cliente/local, configurar data, tensão nominal e amostragem.
2. Iniciar sessão de medição e instalar por profissional habilitado em conexão elétrica protegida.
3. Capturar e gravar continuamente os resumos e eventos por 7 dias.
4. Efetuar desligamento formal quando possível e retirar o microSD.
5. Importar a sessão no portal local, conferir integridade, analisar e emitir relatório.

## Segurança

**Não ligar módulos eletrônicos genéricos diretamente à instalação elétrica sem projeto e validação de isolamento, proteção e acondicionamento.** O circuito de medição, alimentação AC/DC, detector de rede e serial precisam de verificação técnica. Nunca conectar condutores da rede aos GPIOs. A bateria requer proteção e módulo UPS com power-path efetivo.

## Próximos marcos

1. Validar variantes reais da ESP32-S3, PZEM, DS3231, leitor SD e UPS.
2. Fechar topologia de instalação (tomada, quadro ou ambos) e isolamento.
3. Prototipar logs e importador com dados sintéticos.
4. Testar alimentação ininterrupta, relógio, integridade do SD e recuperação pós-queda.
5. Calibrar e validar medições comparadas a instrumento de referência.
6. Desenvolver portal e relatório técnico.
