# Portal técnico | MVP 0.1.1

> **Implementação experimental** na branch `feature/portal-tecnico-mvp`. Não utilizar os resultados para laudo formal ou atribuição de responsabilidade elétrica. Portal **técnico apenas**; as duas versões (cliente e técnico) existem exclusivamente na exportação PDF.

## Compatibilidade e execução

A versão de Python está definida em **`.python-version` (`3.11`)** e **`pyproject.toml` (`>=3.11,<3.12`)**. O inicializador `portal/run.py` verifica o interpretador e informa quando não for compatível. Evite Python 3.12/3.13 nesta fase, mesmo que outras dependências funcionem.

Para iniciar diretamente, sem ativar o ambiente virtual, utilize na raiz:

**Windows PowerShell:** `./Start-Portal.ps1` (ou `& .\\Start-Portal.ps1`).

**Linux:** `bash start-portal.sh`.

Os scripts preparam `.venv` com Python 3.11, instalam dependências e iniciam o serviço exclusivamente em `127.0.0.1:8080`. No Windows, o launcher `py -3.11` precisa estar disponível. Em ambos os sistemas, o instalador de pacotes precisa acessar o índice na primeira instalação; **a operação do portal depois disso é offline**.

## Testes de usabilidade sem hardware

1. Abra `http://127.0.0.1:8080`.
2. Em **Explorar sem hardware**, escolha **Oscilações de tensão** e clique em **Abrir demonstração**.
3. Confira indicadores, gráfico e eventos; clique em **SUBTENSAO** ou **SOBRETENSAO** e observe detalhe, amostras próximas e zoom.
4. Troque para o cenário **Interrupções de energia**; confira que apenas eventos do detector AC são classificados como interrupções, enquanto timeout PZEM é uma falha distinta.
5. Teste **Rede estável**; a ausência de eventos detectados não significa ausência de qualquer distúrbio.
6. Baixe **PDF técnico**, **PDF cliente** e **CSV**. A diferenciação cliente/técnico existe **somente nesses PDFs**, não na navegação do portal.
7. Execute o roteiro completo em [ROTEIRO_USABILIDADE_PORTAL_V011.md](../docs/validacao/ROTEIRO_USABILIDADE_PORTAL_V011.md).

Os cenários incorporados no portal são 100% sintéticos, têm horário histórico fixo e são sinalizados visualmente e no PDF. Não servem como prova de comportamento da rede.

## Recursos incluídos

- FastAPI local, frontend responsivo com a identidade visual aprovada.
- Importação de arquivos `.log` do protocolo versão 1, com CRC32 e agrupamento de sessões.
- Preservação dos originais por hash SHA-256 na pasta de dados do usuário.
- Estatísticas de tensão e frequência, análise inicial de eventos sustentados, eventos de detector AC, avisos e registros brutos.
- Gráfico Plotly inteiramente local, sem CDN.
- Relatórios PDF **executivo/cliente** e **técnico/profissional**; exportação CSV.
- Três cenários sintéticos carregados com um clique; filtros de eventos, zoom, detalhe e amostras próximas.
- Simulador determinístico, testes unitários do parser e da análise e testes HTTP de importação/exportação.
- Inicialização facilitada via scripts PowerShell e Bash, com verificação de Python 3.11.

## Requisitos

Python **3.11.x** (obrigatório para este MVP) e dependências em `portal/requirements.txt`.

### Windows PowerShell

```powershell
git clone --branch feature/portal-tecnico-mvp --single-branch https://github.com/ChristopherNicolasSMM/Monitor-Eletrico-IOT.git
cd Monitor-Eletrico-IOT
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r portal/requirements.txt
python -m portal.tools.generate_demo
python -m portal.run
```

### Linux

```bash
git clone --branch feature/portal-tecnico-mvp --single-branch https://github.com/ChristopherNicolasSMM/Monitor-Eletrico-IOT.git
cd Monitor-Eletrico-IOT
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r portal/requirements.txt
python -m portal.tools.generate_demo
python -m uvicorn portal.app:app --host 127.0.0.1 --port 8080
```

Abra **http://127.0.0.1:8080/** e importe `portal/sample_data/demo_127v.log` (gerado acima). É **dado fictício** com subtensão, sobretensão e interrupção simulada, não medição real.

## Testes

```bash
python -m unittest discover -s portal/tests -v
```

### Limites do MVP

- O protocolo e seu CRC32 são **experimentais**: definidos no parser/produtor para permitir integração, mas ainda precisam de congelamento formal do contrato de firmware.
- Apenas `.log`, máximo 32 MiB por arquivo e 30 arquivos por importação.
- As análises ficam em **memória durante a execução**; reiniciar o servidor perde o índice das importações (mas os arquivos originais continuam preservados em `~/.monitor-eletrico-iot/raw/`).
- Ainda não há base SQLite, contas, calibração, reprocessamento parametrizável nem cobertura temporal rigorosa.
- Critérios de sobretensão/subtensão são **configuráveis conceitualmente**, mas o MVP usa 90% e 110% da tensão nominal e duração mínima de 1s. Esses limiares não expressam conformidade regulatória.
- Eventos sustentados são aproximações pelo espaçamento das amostras; o PZEM não comprova afundamentos rápidos, surtos ou ausência total de distúrbios.
- A interrupção só é declarada quando o log contém estado do detector AC isolado, cuja existência física ainda não foi validada.
- PDF atual é um relatório inicial de indicadores/eventos, ainda sem gráficos impressos ou identidade completa; a versão técnica precisa de ampliação de evidências.
- O arquivo `portal/static/mark.svg` é uma cópia do símbolo aprovado para servir o portal offline.
- A análise atual não tem avaliação metrológica ou cálculo formal de cobertura com as normas de qualidade de energia.
- O gráfico marca lacunas acima de 2,5 segundos como interrupções visuais, sem atribuir zero volt.
- A rotina de GitHub Actions precisa ser conferida: não considerar CI aprovado enquanto os jobs não concluírem com êxito.

## Segurança

Servidor restrito a `127.0.0.1`; não executar com `--host 0.0.0.0` sem implementar autenticação e controles adicionais. Não compartilhar ou instalar em campo sem validação. Não tratar os arquivos importados como código.

## Documentação

- [Especificação funcional do portal](../docs/technical/portal/README.md)
- [Contrato do log](../docs/PROTOCOLO_LOG.md)
- [Plano de testes e aceite](../docs/technical/portal/05-testes-aceite.md)
