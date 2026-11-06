# Padrão editorial e documental

**Versão:** 0.2 (proposta adotada em 2026-11-06)  
**Referências de estilo:** MD2Doc, DeviceMQTT, CardForge_v2, iot_smart_irrigation e Tesseract, todos do mesmo autor.

## Princípio

O README é a porta de entrada, **não** a documentação inteira. Deve apresentar logo, propósito, problema, funcionamento, estado real, recursos, limites, navegação e caminho de execução somente quando validado.

Manter **dois trilhos independentes**:

1. `docs/technical/`: arquitetura, requisitos, contratos, fluxos, dados, testes, calibração, riscos e manutenção, voltados ao desenvolvimento.
2. `docs/manual/`: linguagem acessível ao operador, instalação por profissional, uso do dispositivo, importação, interpretação, solução de problemas.

A documentação de requisitos, protocolo, hardware e portal existente em `docs/*.md` permanece canônica durante a transição. Os índices devem apontar para ela, **sem duplicar e divergir**.

## Estrutura editorial mínima

Cada documento deve ter título, propósito, estado (proposto/implementado/validado), pré-requisitos quando aplicáveis, fluxo ou contrato, critérios de validação, limitações e links relacionados.

Diagramas: Mermaid quando pertinente, priorizando C4/contexto, fluxo de estados, sequência e modelo lógico. Capturas de tela: preferir imagens reais, numeradas, legendadas, com versão do software. Demonstrações sintéticas devem ser explicitamente rotuladas. Não apresentar mockup como tela implementada.

## Rigor de documentação

- Diferenciar **decidido**, **proposto**, **implementado** e **validado em hardware**.
- Nunca declarar funcional uma leitura, precisão, hardware, relatório ou comando sem evidência.
- Datas em ISO 8601 nas evidências técnicas; texto do manual em PT-BR.
- Identificar versões de firmware, portal, protocolo, hardware e dados de teste.
- Explicar erros, recuperação, integridade e cenários negativos, não apenas caminho feliz.
- Toda decisão importante atualiza `docs/DECISOES.md` e documento específico.
- Toda mudança de protocolo incompatível exige versão e fixture de retrocompatibilidade.
- Links relativos devem ser conferidos, e imagens precisam existir no repositório.
- Nunca acrescentar badges de CI, licença, release ou cobertura que não existam realmente.

## Referências estudadas

- [MD2Doc](https://github.com/ChristopherNicolasSMM/MD2Doc): identidade, navegação, manuais de execução e distribuição.
- [DeviceMQTT](https://github.com/ChristopherNicolasSMM/DeviceMQTT): C4, sequências, API e portal embarcado.
- [CardForge v2](https://github.com/ChristopherNicolasSMM/CardForge_v2): README ilustrado, screenshots, início rápido e distribuição portátil.
- [IoT Smart Irrigation](https://github.com/ChristopherNicolasSMM/iot_smart_irrigation): validações, hardware, contratos, manuais com evidências.
- [Tesseract](https://github.com/ChristopherNicolasSMM/Tesseract/blob/main/docs/skills/04-padrao-de-documentacao.md): dois trilhos separados, manutenção e expansão.
