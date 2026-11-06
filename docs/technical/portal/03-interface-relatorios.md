# 03 — Interface de análise e relatórios

**Estado:** desenho funcional v0.3, sem protótipo executável.

## Dois modos de apresentação, um só resultado

**Visão Cliente:** linguagem acessível, indicadores de maior relevância, resumo da confiabilidade, gráfico principal, eventos explicados sem jargão e próximos passos de investigação. Não deve ocultar dados ruins ou transmitir certeza inexistente.

**Visão Técnica:** todas as grandezas válidas, zoom, filtros, eventos completos, parâmetros de análise, dados brutos, auditoria de integridade, erros e referências a linhas de origem.

Os dois modos derivam do **mesmo snapshot versionado de análise**. Alternar modo não altera cálculos, apenas apresentação e nível de detalhe. Modo de visualização **não é perfil de segurança**: acesso a dados do cliente e alterações de configuração precisam de regras próprias.

## Navegação proposta

```text
Início / Campanhas
├── Importar arquivos
│   ├── Seleção e progresso
│   └── Resultado de integridade
├── Campanha / Visão geral
│   ├── Cliente: resumo e eventos essenciais
│   └── Técnico: painel e filtros completos
├── Linha do tempo e gráficos
├── Ocorrências
│   └── Evidências da ocorrência
├── Qualidade do registro
│   └── Linhas brutas e auditoria
├── Relatórios
│   ├── Executivo (cliente)
│   └── Técnico (profissional)
└── Configurações de análise / Metadados
```

## Design e comportamento

Identidade visual aprovada: grafite `#101E2C`, azul técnico `#1C3445`, verde-água `#3DD8C5`, âmbar `#F7B955`. Não usar somente cor para indicar risco: combinar ícone, rótulo e texto. Responsivo para desktop/tablet; layouts densos de registros podem usar rolagem horizontal. Acessibilidade: contraste, teclado, legendas, datas legíveis e impressão monocromática.

### Tela 1 — Importação

Seletor de arquivos, processamento, número de linhas válidas/ inválidas, sessões, reinícios, data inicial/final, cobertura, SHA-256, warnings e ação 'Continuar com ressalvas' quando possível. Linha com erro permite inspeção, nunca edição do original.

### Tela 2 — Visão Cliente

Cabeçalho: cliente/local, dispositivo, período e estado da qualidade dos dados. Cards com comportamento geral (sem nota universal de 'rede boa'), min/máx da tensão válida, número de eventos observados e tempo de interrupção **confirmado**. Gráfico de tensão com bandas apenas quando limites configurados; uma linha de tempo com principais ocorrências e explicações curtas. Sessão incompleta e lacunas aparecem de maneira explícita.

Texto de conclusão deve usar: 'Foi observado...', 'Os dados sugerem investigar...' e 'Não foi possível determinar...'.

### Tela 3 — Visão Técnica

Filtros por campanha, sessão, data, intervalo, grandeza, classificação, qualidade, origem de sensor. Gráficos interativos Plotly para tensão, frequência e, quando válido, corrente/potência/fator de potência; overlay de interrupções, lacunas, resets e falhas de sensor. Tabela de eventos com tempos observados, regras/limiares, duração conhecida, confiança e links para registros. Painel de diagnósticos com configuração aplicada e versão analítica.

### Tela 4 — Evidência individual

Mostra: ID e classificação, descrição, horário, início/fim (ou indeterminado), duração medida ou estimada com ressalva, tensão min/max válida, regra aplicada, janela de amostras, gaps, linha inicial/final, dados brutos e possível relação temporal com carga. Botão para exportar o recorte com metadados.

### Tela 5 — Qualidade do dado

Indicadores de registros válidos, descartados, duplicados, versões não suportadas, saltos temporais, amostras obsoletas, `000` sem `999`, sensor indisponível e intervalos não observados. Link por falha até arquivo/linha/seq.

## Relatórios

| Seção | Executivo / cliente | Técnico |
|---|---|---|
| Capa | Marca, cliente, período | Marca, identificação e instrumento |
| Síntese | Explicação clara | Resumo técnico |
| Qualidade dos dados | Qualidade/cobertura e limitações resumidas | Percentuais, categorias e evidências |
| Medidas | Tensão e principais achados | Todas válidas, estatísticas e metodologia |
| Eventos | Seleção relevante e linha do tempo | Tabela completa, regras e referências |
| Gráficos | Seleção simples e legível | Séries detalhadas, bandas, lacunas |
| Recomendações | Próximas verificações sem conclusões absolutas | Hipóteses com evidência, restrições e sugestões |
| Apêndices | Glossário e ressalvas | CRC/versão/hash, metadados, amostras, exportações |

PDF deve carregar `report_id`, `analysis_run_id`, versão do portal, timestamp de emissão, período observado, parâmetros, hash(es) SHA-256 dos arquivos fonte e advertência de que o protótipo não é analisador certificado. Evitar despejar todos os registros no PDF: exportar CSV bruto/normalizado separado e referenciar pacote auditável.

## Regras de apresentação

- 'Sem eventos detectados' **não significa** ausência de perturbações rápidas que o PZEM não captura.
- '0 V' somente se houver medição válida; detector de rede pode registrar interrupção sem valor de RMS.
- Sem CT, esconder métricas indisponíveis ou marcar N/D; não mostrar `0 A` fictício.
- Mostrar fuso local para leitura, conservar UTC no registro original.
- Gráficos devem preservar mínimos/máximos por janela no downsampling; não eliminar ocorrências ao reduzir pontos.
- O relatório reproduz exatamente a análise selecionada, mesmo se os limiares foram alterados depois.

## Exportações e privacidade

Exportar PDF executivo, PDF técnico, CSV normalizado com flags, JSON estruturado com eventos e manifesto de proveniência. Os arquivos de origem são preservados separadamente. Dados pessoais do cliente não entram em um export bruto por padrão. Exigir confirmação explícita antes de exportar dados identificáveis.

## Implantação proposta

FastAPI em loopback, frontend servido localmente; acesso via navegador. Portabilidade Windows/Linux; usar pastas separadas para recursos empacotados e dados do usuário. Não afirmar instalador pronto sem build/teste. Mecanismo de PDF (WeasyPrint/Playwright/ReportLab) será escolhido por testes multiplataforma e fidelidade visual.
