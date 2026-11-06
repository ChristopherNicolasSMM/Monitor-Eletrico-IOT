# Registro de decisões (ADR leve)

Atualizado em 2026-11-06. Os itens abaixo são decisões de arquitetura; não significam hardware testado.

| ID | Decisão | Justificativa | Estado |
|---|---|---|---|
| D001 | ESP32-S3 N16R8 como controlador | Baixo custo e periféricos adequados | Aprovada, variante pendente |
| D002 | PZEM-004T V3.0 100 A | Valores elétricos já calculados; serial | Aprovada, validar limites |
| D003 | DS3231 com bateria própria | Timestamp preservado entre reinícios | Aprovada, conferir módulo |
| D004 | microSD integrado se existente; senão SPI 3,3 V | Hardware intercambiável | Aprovada |
| D005 | UPS com 18650, em vez de pilha 9 V | Recarga automática e maior energia útil | Aprovada, modelo pendente |
| D006 | Log `|...` de linha única com tipos 000 e 999 | Recuperação, rastreabilidade e inspeção textual | Aprovada em princípio, esquema proposto |
| D007 | 000 em todo boot; 999 somente em desligamento formal | Evitar falsificar encerramento | Aprovada |
| D008 | Portal offline em Python/FastAPI | Bibliotecas para estatística, gráficos e PDF | Recomendação arquitetural |
| D009 | Detector AC independente do PZEM | Timeout PZEM não prova ausência de rede | Requisito técnico |
| D010 | Documentação antes do código | Consolidar requisitos, segurança e protocolo | Aprovada |

## Questões abertas

- Modelo físico exato da ESP32-S3 e presença real de slot microSD.
- Módulo UPS 5 V compatível com power-path, capacidade e telemetria de bateria.
- Sensor isolado para detecção de ausência de rede.
- Topologia de instalação: tomada, quadro ou ambas, implicações de CT e gabinete.
- Proteção, isolamento da UART PZEM e segurança da USB acessível.
- Taxa efetiva de atualização do PZEM e comportamento sem AC.
- Definir e congelar CRC, codificação do payload e tratamento de linhas parcialmente escritas.
- Limiares e critérios técnicos de eventos por tensão nominal.
- Política de armazenamento de metadados de cliente e privacidade no portal.
- Selecionar motor PDF e empacotamento de instalação.

## Processo de mudança

Toda nova decisão deve atualizar este arquivo e o documento específico correspondente. Alterações incompatíveis no protocolo exigem nova versão de esquema e testes de leitura de dados antigos.
