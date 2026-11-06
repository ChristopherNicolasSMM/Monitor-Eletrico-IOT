# Requisitos e limites (rascunho v0.1)

## Caso de uso

Um técnico instala o equipamento por 7 dias em local onde falhas elétricas intermitentes afetam aparelhos. Ao final recupera os dados do microSD e analisa datas, duração e características dos eventos.

## Requisitos funcionais

- RF01: registrar tensão (V), corrente (A), potência ativa (W), energia (kWh), frequência (Hz), fator de potência, quando válidos.
- RF02: gravar arquivos texto com uma linha por registro e formato versionado.
- RF03: RTC fornece data/hora persistente e identificação de qualidade do horário.
- RF04: abrir sessão `000` a cada boot; emitir `999` apenas em encerramento formal; reinício inesperado permanece identificável pela ausência de fechamento.
- RF05: registrar eventos de perda de AC **somente se confirmados por detector isolado independente**; falha serial do PZEM é categoria distinta.
- RF06: persistir snapshots operacionais periódicos, eventos, mudanças de estado e saúde do equipamento.
- RF07: preservar dados durante uso pela bateria e detectar bateria fraca quando hardware suportar.
- RF08: leitura offline de microSD e portal web no computador para importar, validar, visualizar e exportar dados.
- RF09: manter identificadores de dispositivo, instalação, sessão e versão do protocolo.
- RF10: manter rastreabilidade dos dados originais e permitir reprovar registros inválidos sem apagá-los.

## Requisitos não funcionais

- Operação por pelo menos 7 dias com alimentação da rede; bateria cobre apenas falhas de energia dentro de autonomia validada.
- Resistência a perda inesperada de energia: flush periódico, trilha de integridade e recuperação de arquivo.
- Não assumir um valor de corrente quando transformador de corrente não estiver instalado; usar `NA`.
- Wi-Fi não é pré-requisito e pode ficar desabilitado.
- Esquema e hardware modulares; troca de controlador não altera formato lógico dos logs.
- Limites/limiares de tensão dependem da tensão nominal e da metodologia de análise, não são uma classificação regulatória presumida.

## Limites e incertezas

- PZEM-004T: faixa de tensão nominalmente especificada 80 a 260 V AC, sujeito à variante e validação.
- As grandezas devolvidas podem atualizar mais lentamente que as consultas UART; consultar mais vezes **não** garante resolução de milissegundos.
- Falta de leitura PZEM não comprova falta de rede; necessária detecção AC independente para essa conclusão.
- A medição de corrente por CT requer instalação adequada envolvendo um único condutor da carga.
- Não detecta com confiabilidade transientes de microssegundos, surtos ou distorção harmônica detalhada.
- Para alegações formais de conformidade de concessionária, exigir metodologia, instrumentação e calibração apropriadas.

## Critérios iniciais de aceite (a refinar em testes)

- Sessões com identificação inequívoca, `000` e fechamento `999` quando solicitado.
- Arquivo parcial recuperável após corte abrupto, com relato explícito da perda potencial.
- Parser rejeita linha truncada/CRC incorreto e informa posição, sem perder registros válidos.
- Importação sem conexão com internet.
- Dados sintéticos de tensão/queda geram gráficos e relatório consistentes.
