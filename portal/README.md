# Portal técnico | MVP 0.1

> **Implementação experimental** na branch `feature/portal-tecnico-mvp`. Não utilizar os resultados para laudo formal ou atribuição de responsabilidade elétrica. Portal **técnico apenas**; as duas versões (cliente e técnico) existem exclusivamente na exportação PDF.

## Recursos incluídos

- FastAPI local, frontend responsivo com a identidade visual aprovada.
- Importação de arquivos `.log` do protocolo versão 1, com CRC32 e agrupamento de sessões.
- Preservação dos originais por hash SHA-256 na pasta de dados do usuário.
- Estatísticas de tensão e frequência, análise inicial de eventos sustentados, eventos de detector AC, avisos e registros brutos.
- Gráfico Plotly inteiramente local, sem CDN.
- Relatórios PDF **executivo/cliente** e **técnico/profissional**; exportação CSV.
- Simulador determinístico e testes unitários do parser e da análise.

## Requisitos

Python 3.11+ (recomendado) e dependências em `portal/requirements.txt`.

### Windows PowerShell

```powershell
git clone --branch feature/portal-tecnico-mvp --single-branch https://github.com/ChristopherNicolasSMM/Monitor-Eletrico-IOT.git
cd Monitor-Eletrico-IOT
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r portal/requirements.txt
python -m portal.tools.generate_demo
python -m uvicorn portal.app:app --host 127.0.0.1 --port 8080
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

## Segurança

Servidor restrito a `127.0.0.1`; não executar com `--host 0.0.0.0` sem implementar autenticação e controles adicionais. Não compartilhar ou instalar em campo sem validação. Não tratar os arquivos importados como código.

## Documentação

- [Especificação funcional do portal](../docs/technical/portal/README.md)
- [Contrato do log](../docs/PROTOCOLO_LOG.md)
- [Plano de testes e aceite](../docs/technical/portal/05-testes-aceite.md)
