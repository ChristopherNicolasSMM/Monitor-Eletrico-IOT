# Roteiro de usabilidade do Portal Técnico — MVP 0.1.1

**Estado:** roteiro preparado, **sem validação manual concluída**.  
**Data:** 2026-11-06.  
**Branch:** `feature/portal-tecnico-mvp`.  
**PR:** [#1](https://github.com/ChristopherNicolasSMM/Monitor-Eletrico-IOT/pull/1).

## Objetivo e limites

Validar navegabilidade do portal técnico, coerência dos indicadores, importação local, investigação de eventos e a geração de PDFs **cliente** e **técnico**. A interface do portal é exclusivamente técnica nesta etapa. Os dados de demonstração não vieram de um PZEM real e **não** certificam precisão elétrica.

## Preparação (Windows)

1. Instalar Python 3.11.x com Python Launcher (`py -3.11 --version`).
2. Clonar branch do PR e entrar na pasta do projeto.
3. Executar `& .\Start-Portal.ps1` na raiz do repositório. O script cria a `.venv`, instala dependências e abre o serviço em loopback. Se a política de execução bloquear scripts, use uma autorização limitada à sessão do PowerShell e repita o comando.
4. Abrir `http://127.0.0.1:8080` no navegador. Conferir que o modo indica **Portal Técnico**.
5. Manter o console aberto para verificar erros e finalizar com Ctrl+C.

**Linux:** `bash start-portal.sh` com Python 3.11 disponível.

## Casos de teste funcionais

| ID | Ação | Resultado esperado | Status |
|---|---|---|---|
| UX-01 | Abrir o portal sem registros | Navegação funcional, cards sem valores indevidos | Não executado |
| UX-02 | Carregar cenário **Oscilações** | Dados claramente marcados como fictícios; tensão abaixo/acima dos limiares e eventos listados | Não executado |
| UX-03 | Selecionar evento na tabela | Detalhe com origem e amostras próximas; gráfico amplia o período | Não executado |
| UX-04 | Filtrar por tipo de evento | Apenas eventos da categoria selecionada, contagem consistente | Não executado |
| UX-05 | Restaurar zoom | Gráfico volta à janela completa | Não executado |
| UX-06 | Carregar cenário **Interrupções** | Estados de rede derivados do detector isolado, não de timeout PZEM | Não executado |
| UX-07 | Carregar cenário **Rede estável** | Indicadores e gráfico presentes, sem alarmes artificiais | Não executado |
| UX-08 | Exportar PDF **técnico** | Abre como PDF, exibe estatísticas, rastreabilidade e aviso de dados fictícios | Não executado |
| UX-09 | Exportar PDF **cliente** | PDF mais resumido, sem portal separado, mesmas estatísticas-base | Não executado |
| UX-10 | Exportar CSV | Arquivo legível, campos tabulares sem execução de fórmulas | Não executado |
| UX-11 | Importar `.log` criado pelo gerador | Integridade, sessões, ocorrências e dados brutos | Não executado |
| UX-12 | Importar arquivo truncado ou CRC incorreto | Inconsistência identificada, sem lançar falso resultado de tensão | Não executado |
| UX-13 | Abrir em janela estreita/celular | Menu, controles e tabelas navegáveis, sem perder conteúdo | Não executado |
| UX-14 | Reiniciar o servidor | Originais preservados no disco; sessão em memória perdida conforme limitação documentada | Não executado |
| UX-15 | Desconectar internet após instalar dependências | Portal, gráficos e relatórios continuam funcionais | Não executado |

## Perguntas orientadas à experiência

- A importação transmite confiança? O usuário entende o que é um arquivo íntegro ou parcial?
- Está claro o que é uma **medição real** versus uma **demonstração sintética**?
- Os indicadores ajudam a encontrar rapidamente períodos problemáticos?
- O clique em um evento facilita investigar o que ocorreu?
- As cores e rótulos comunicam claramente informação, atenção e indisponibilidade?
- Qual a informação mais importante que faltou no painel técnico?
- Os PDFs têm profundidade adequada para o técnico e legibilidade para o cliente?
- A interface é confortável em notebook pequeno? Há informações escondidas em tabelas?
- A coleta de feedback deve diferenciar defeito funcional, dúvida de leitura e sugestão de melhoria.

## Registro de evidências por execução

Preencher para cada ciclo:

```text
Data/ambiente:
Sistema operacional:
Versão do Python (python --version):
Navegador e versão:
Commit / branch testado:
Cenário / arquivo:
IDs de teste executados:
Resultado esperado vs observado:
Capturas de tela (caminhos reais):
Defeitos e severidade:
Sugestões e prioridades:
```

Não anexar captura sintética como medição real. Somente após testes locais efetivos atualizar os status da tabela e publicar screenshots identificados com versão e cenário.

## Limitações técnicas de atenção

O PZEM-004T V3.0 possui restrições de faixa e atualização; a camada atual de análise usa limiares experimentais, não limites regulatórios. Gaps são identificados visualmente, mas cobertura temporal regulatória, autoauditoria completa e cálculos de duração das interrupções ainda não estão concluídos. Não tomar decisão de segurança elétrica com base nos resultados desta versão.

## Automação

Workflow `.github/workflows/portal-tests.yml`: matriz Windows/Linux, Python 3.11, testes unitários, HTTP, geração de logs e smoke test. **Estado verificado em 2026-11-06:** execuções retornaram falha sem etapas reportadas nem runner atribuído; a causa da infraestrutura precisa ser verificada no painel do GitHub, não há evidência de execução dos testes. Não anunciar CI verde.
