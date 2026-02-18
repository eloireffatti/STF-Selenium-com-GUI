# STF-Selenium-com-GUI



## Visão geral
Este repositório contém uma solução modular em Python para:
1. **Raspar dados do Portal do STF** via Selenium/WebDriver (Chrome).
2. **Enriquecer os dados** via **API DataJud (CNJ)**.
3. **Consolidar e analisar** os dados, exportando **XLSX** e **JSON consolidado**.
4. Operar tudo por meio de uma **GUI (Tkinter)**, sem necessidade de conhecimento de programação.

## Componentes
- **GUI_Extrator_STF1**: interface gráfica com 3 abas (Extração STF, DataJud, Consolidação).
- **STF_Selenium_v3**: extração no Portal STF (TXT/JSON por processo + logs).
- **API_DataJud_v3**: consulta à DataJud e grava JSON por processo.
- **Mon_Plan_c_dados_API**: consolidação, indicadores e exportação final.
- **ModuloSTFSelenium**: biblioteca interna com XPaths, parsing e funções analíticas.

## Fluxo recomendado
1. **Aba 1 – Extração STF** → gera `{CLASSE} {NUMERO}.json` e `.txt` por processo.
2. **Aba 2 – DataJud** → gera JSON por processo na pasta da API.
3. **Aba 3 – Consolidação** → gera `dados_compilados.xlsx` e `dados_compilados.json` (nomes configuráveis).

## Dados extraídos (resumo)
### STF (por processo)
- Classe, número, incidente, número único (CNJ), origem/UF, tramitação, publicidade, prioridades
- Relator/redator/último incidente
- Assuntos, partes (com separação por polos e procuradores)
- Andamentos (padronizados com delimitadores)
- Links de decisões e outros documentos

### DataJud (por processo)
- Classe e dados da origem: classe, sistema, órgão julgador, grau, tribunal, sigilo
- Assuntos e movimentos (andamentos) na origem

## Tratamento de falhas (resumo)
- Pausas anti-bloqueio, reinício periódico do navegador e retomada após falhas
- Logs provisórios (snapshots) + logs definitivos (sucesso/erro/interrupção)
- DataJud: validação de chave + reconsulta automática em falhas de conexão

## Saídas
- **Por processo (STF)**: `{CLASSE} {NUMERO}.json` e `.txt`
- **Por processo (DataJud)**: JSON correspondente
- **Consolidado**: XLSX + JSON consolidado

## Recomendações
- Manter ChromeDriver compatível com a versão do Chrome.
- Executar grandes lotes em horários de menor carga para reduzir bloqueios.
- Externalizar chave da API em configuração local/variável de ambiente em ambientes compartilhados

## Passo a passo


# Abra a GUI → Aba “Extração STF”:

selecione classe,
escolha intervalo ou lista,
defina pasta de dados e pasta de logs,
iniciar.



# Aba “Consulta DataJud”:

indique pasta de dados do extrator,
indique pasta de saída da API,
informe/valide chave,
iniciar.



# Aba “Consolidar Dados”:

indique pasta do extrator,
indique pasta da API,
indique pasta de saída,
defina nomes dos arquivos,
iniciar.
