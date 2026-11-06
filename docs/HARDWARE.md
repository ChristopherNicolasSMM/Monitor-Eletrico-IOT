# Hardware e lista de materiais (v0.1)

| Item | Escolha | Estado | Observações |
|---|---|---|---|
| Controlador | ESP32-S3 N16R8 | Definido conceitualmente | Conferir pinagem, slot SD e alimentação da variante adquirida |
| Medição | PZEM-004T V3.0 100 A + CT | Definido conceitualmente | 80–260 V AC; validar variante, comunicação Modbus RTU e segurança |
| Relógio | DS3231 + bateria | Definido | Conferir módulo/circuito de recarga; não usar CR2032 não recarregável em circuito que tente carregá-la |
| Memória | microSD | Definido | Usar slot integrado só se houver; caso contrário leitor SPI 3,3 V externo |
| Backup | 18650 protegida + UPS 5 V com power-path | Direção definida, modelo pendente | Comutação sem reset, proteção de carga/descarga, operação com carga conectada |
| Fonte principal | AC/DC isolada → UPS | Pendente | Segurança elétrica e capacidade de corrente comprovadas |
| Detector de rede | Entrada AC isolada independente | Pendente | Diferencia falta real de rede e falha do PZEM |
| Interface serial | UART PZEM ↔ ESP32 | Pendente validação | Isolamento e níveis lógicos 5 V/3,3 V; não assumir compatibilidade direta |
| Gabinete | Caixa isolante, fixação, conectores e proteção | Pendente | Dimensionar para instalação real com profissional qualificado |

## Energia

A pilha alcalina 9 V não foi escolhida: normalmente possui menos energia útil, não recarrega e exige troca. Uma 18650 típica de 2600 mAh fornece energia nominal de aproximadamente 9,6 Wh, antes de perdas; autonomia real depende do consumo medido. O RTC usa bateria própria apenas para retenção do relógio.

Requisitos do UPS: entrada 5 V por fonte isolada; saída 5 V estável; carga e alimentação simultâneas com power-path verdadeiro; baixa tensão protegida; dimensionamento de corrente para pico de ESP32 e SD. Não presumir que TP4056 isolado atenda tais funções.

## Arquitetura funcional (não é esquema elétrico)

```text
Rede AC ──> Proteção + fonte isolada 5V ──> UPS + 18650 ──> ESP32-S3
    │                                                  ├─ RTC DS3231
    ├─> PZEM-004T / CT ──> interface serial segura ────┤
    └─> Detector AC isolado ──> entrada protegida ─────┤
                                                       └─ microSD
```

## Pré-condições para instalação real

1. Definir se haverá versão de tomada, quadro ou duas versões distintas.
2. Conferir separação galvânica, isolamento da interface PZEM e quaisquer portas USB expostas.
3. Dimensionar fusível/proteção, bornes, cabos, distâncias de isolamento, gabinete e dissipação.
4. Ensaiar com alimentação protegida e instrumentos de referência, conduzidos por profissional habilitado.
5. Não afirmar conformidade metrológica ou segurança certificada sem ensaios.
