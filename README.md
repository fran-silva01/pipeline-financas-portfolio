# Pipeline Automatizado de Cotações Financeiras & Dashboard Interativo

Este é um projeto ponta a ponta (End-to-End) focado em Engenharia e Análise de Dados. O ecossistema automatiza a coleta diária de cotações de moedas (Dólar e Euro), realiza o tratamento e a consolidação dos dados em um banco relacional e disponibiliza as informações em um painel interativo dinâmico na nuvem.

**[CLIQUE AQUI PARA ACESSAR O DASHBOARD EM TEMPO REAL](https://pipeline-financas-portfolio-r3uges8ba7ewhszcdpk4cd.streamlit.app/)**

---

## Tecnologias e Ferramentas

* **Linguagem Principal:** Python 3.12
* **Manipulação e Modelagem de Dados:** Pandas
* **Consumo de API:** Requests (Integração com a AwesomeAPI para dados JSON em tempo real)
* **Banco de Dados:** SQLite3 (Armazenamento relacional estruturado e persistente)
* **Orquestração e CI/CD:** GitHub Actions (Automação de rotinas via agendamento *cron*)
* **Visualização de Dados:** Streamlit & Plotly Express (Gráficos interativos de séries temporais)

---

## Arquitetura e Fluxo de Dados

1. **Agendamento (Orquestração):** O GitHub Actions aciona um gatilho de execução automatizado diariamente.
2. **Extração (Ingestão):** O script `pipeline.py` realiza requisições HTTP na API financeira para capturar os preços de compra vigentes do Dólar e do Euro comercial.
3. **Tratamento e Carga (ETL):** O Pandas estrutura os dados brutos e executa uma operação de *append* (inserção contínua) na tabela `cotacoes` dentro do banco `data/financas.db`, preservando o histórico sem sobrescrever registros antigos.
4. **Automação de CI/CD:** O robô do GitHub Actions realiza o commit e o push do banco de dados atualizado de volta para o repositório automaticamente.
5. **Consumo e Visualização:** A aplicação web do Streamlit (`app.py`) monitora o banco de dados utilizando caminhos dinâmicos absolutos, atualizando os indicadores e o gráfico de linhas do Plotly de forma instantânea na nuvem.

---

## Estrutura do Repositório

```text
pipeline-financas-portfolio/
│
├── .github/
│   └── workflows/
│       └── pipeline.yml       # Configuração do Cron Job do GitHub Actions
│
├── data/
│   └── financas.db            # Banco de dados SQLite contendo o histórico de cotações
│
├── src/
│   ├── pipeline.py            # Script de extração da API e carga no banco
│   └── app.py                 # Código da aplicação interativa do Streamlit
│
├── requirements.txt           # Dependências e pacotes necessários para o projeto
└── README.md                  # Documentação oficial do projeto