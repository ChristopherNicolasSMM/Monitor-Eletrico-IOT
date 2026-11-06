# 04 — Perguntas frequentes

**Estado:** respostas com base no projeto proposto.

### O aparelho precisa de internet?

Não, a arquitetura proposta usa cartão microSD e portal offline no computador.

### Ele continua funcionando se faltar energia?

A ESP32 deverá continuar operando enquanto houver autonomia de bateria. O circuito de medição PZEM pode parar de responder; um detector independente é necessário para registrar a falta da rede.

### Posso usar os dados para exigir reparos da concessionária?

Os registros poderão apoiar uma investigação, mas o protótipo não é um analisador certificado e não comprova sozinho a origem do problema. Para evidências formais, utilizar instrumentos e metodologia apropriados.

### Já posso montar e instalar?

Ainda não. A alimentação, o isolamento, o detector de rede, a caixa e a calibração precisam de definição e validação.
