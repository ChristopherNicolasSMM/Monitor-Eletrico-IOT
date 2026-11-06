# 01 — Visão geral técnica

**Estado:** proposta de arquitetura, não implementação.

## Contexto

Um registrador embarcado coleta grandezas elétricas disponíveis no PZEM-004T, utiliza detector AC independente para identificar interrupção, RTC DS3231 para datas e UPS 18650 para continuidade de gravação, com arquivos microSD importados posteriormente por portal Python offline.

## Diagrama de contexto

```mermaid
flowchart LR
  T["Técnico"] --> D["Registrador ESP32-S3"]
  R["Rede 127/220 V"] --> M["PZEM + detector isolado"]
  M --> D
  D --> SD["MicroSD"]
  SD --> P["Portal local FastAPI"]
  T --> P
  P --> O["Gráficos, CSV e PDF"]
```

## Contêineres lógicos

```mermaid
flowchart TB
  subgraph E["Dispositivo embarcado"]
    A["Aquisição: PZEM e estado AC"] --> B["Normalizador e eventos"]
    C["RTC e saúde"] --> B
    B --> D["Escritor de logs versionados"]
    D --> F["microSD"]
  end
  subgraph P["Portal offline no computador"]
    I["Importador e validador"] --> J["Séries temporais e agregações"]
    J --> K["Interface de gráficos"]
    J --> L["Gerador de relatórios"]
  end
  F --> I
```

## Contratos e restrições

A fonte principal é a rede, mas a lógica de interrupção não deve depender de timeout do PZEM. Leituras abaixo de 80 V ou acima de 260 V não são consideradas medidas confiáveis pelo módulo na variante prevista. Corrente e potência dependem do CT. O parser aceita apenas versões declaradas e preserva o arquivo original.

## Desdobramentos

Consultar [hardware](../HARDWARE.md), [protocolo](../PROTOCOLO_LOG.md) e [portal](../PORTAL.md).
