# Portal de análise offline (proposta v0.1)

## Decisão de tecnologia

**Python + FastAPI** como backend local; Pandas/NumPy para análise; Plotly.js para gráficos navegáveis; interface HTML/CSS/JavaScript; exportação PDF por motor de HTML→PDF a selecionar. Uma aplicação Node.js também seria viável, mas Python favorece a análise de séries temporais e geração de relatórios.

O portal roda em `127.0.0.1` por padrão e deve funcionar sem internet. Sem autenticação, não liberar operações administrativas na rede local. CORS/origem, upload, caminhos de arquivos e tamanho máximo precisam de proteção.

## Fluxo principal

1. Importar arquivos `.log` de uma sessão ou pasta copiada do microSD, por seleção no navegador.
2. Validar versão do esquema, códigos, timestamps, sequências e CRC; aceitar recuperação parcial com avisos.
3. Exibir resumo: período, tempo efetivamente coberto, lacunas, sessões, reinícios, erros e eventos.
4. Construir gráficos (tensão ao longo do tempo; corrente/potência quando CT disponível; frequência; eventos e energia).
5. Filtrar por equipamento, sessão, data/hora, tipo de evento, severidade e validade.
6. Exportar relatório PDF e CSV derivado, mantendo original imutável.
7. Permitir histórico local de importações sem banco obrigatório na primeira versão; índice SQLite opcional para evolução.

## Telas

- Início: importar medição, ver últimas análises, estado dos dados.
- Importação: arrastar/selecionar arquivo, pré-validação, relatório de integridade.
- Visão geral: KPIs, gráfico principal, período, duração e distribuição de eventos.
- Detalhamento: zoom temporal, curva por grandeza, tabela de eventos e dados brutos.
- Qualidade do dado: erros CRC, seq faltante, timestamp inválido, sensor indisponível, RTC não sincronizado.
- Relatório: cliente/local (dados adicionados pelo técnico), medições, metodologia, limitações e hipóteses de causa.
- Configurações: limites configuráveis e metadados de calibração, sem reescrever os logs.

## Diagnóstico responsável

Separar: **fatos observados**, **indicadores derivados**, **hipóteses** e **limitações**. Não diagnosticar origem na concessionária apenas por haver subtensão; a investigação depende do ponto de medição, instalações e cargas.

## Estrutura futura de código (ainda não implementada)

```text
portal/
  backend/
    app/
      main.py
      parsers/
      analysis/
      reports/
  frontend/
  tests/
  sample_data/
```

## Ordem de implementação

1. Especificar e testar parser v1 com logs sintéticos e truncados.
2. Importação local e validação de integridade.
3. Gráficos de tensão, frequência e eventos.
4. Suporte condicionado à medição de corrente e potência.
5. Relatório HTML/PDF e exportações.
6. Empacotamento para Windows e Linux.
