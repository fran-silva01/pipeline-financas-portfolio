import os # Para manipulação de arquivos e diretórios
import sqlite3 # Para interação com o banco de dados SQLite
import pandas as pd # Para manipulação de dados
import plotly.express as px # Para visualização de dados
import streamlit as st # Para criar a interface web

# Configuração da página do Streamlit
st.set_page_config(
    page_title='Dashboard de Cotações Financeiras', page_icon='📈', layout='wide'
)

# Função para conectar ao banco de dados e carregar os dados
def carregar_dados():
    # 1. Pega o caminho absoluto de onde o arquivo app.py está (dentro de src/)
    diretorio_script = os.path.dirname(os.path.abspath(__file__))

    # 2. Sobe um nível (sai de src/) e vai direto para data/financas.db
    caminho_banco = os.path.abspath(
        os.path.join(diretorio_script, '..', 'data', 'financas.db')
    )

    # Imprime no terminal para checarmos se o caminho corrigiu
    print(f"Buscando banco de dados no caminho correto: {caminho_banco}")

    if not os.path.exists(caminho_banco):
        print('Arquivo NÃO encontrado neste caminho!')
        return None

    conexao = sqlite3.connect(caminho_banco)
    df = pd.read_sql_query(
        'SELECT * FROM cotacoes ORDER BY data_coleta ASC', conexao
    )
    conexao.close()
    return df

# Título principal do dashboard
st.title('Monitoramento Diário de Cotações')
st.markdown(
    'Este dashboard exibe os dados capturados automaticamente pelo pipeline de extração de cotações do dólar e euro.'
)

df = carregar_dados()
if df is None or df.empty: # Verifica se o DataFrame está vazio ou é None
    st.warning('Nenhum dado encontrado no banco de dados. Certifique-se de que o pipeline foi executado.'
    )

else:
    # Garantir que a coluna 'data_coleta' seja do tipo datetime
    df['data_coleta'] = pd.to_datetime(df['data_coleta'])

    # Pegar o registro mais recente para exibir os valores atuais
    ultimo_registro = df.iloc[-1]
    data_formatada = ultimo_registro['data_coleta'].strftime('%d/%m/%Y %H:%M:%S')

    st.write(f"**Última atualização do pipeline:** {data_formatada}")

    # Layout de colunas para exibir os preços atuais do dólar e euro
    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            label=f"Dólar Comercial ({ultimo_registro['moeda_usd']})", 
            value=f"R$ {ultimo_registro['preco_compra_usd']:.3f}",
        )
    
    with col2:
        st.metric(
            label=f"Euro ({ultimo_registro['moeda_eur']})", 
            value=f"R$ {ultimo_registro['preco_compra_eur']:.3f}",
        )
    
    st.markdown('---') # Linha horizontal para separar as seções

    # Seção do Gráfico Histórico
    st.subheader('Histórico de Variações das Moedas')

    # Remodelando o DataFrame para formato longo, facilitando a criação do gráfico
    df_longo = df.melt(
        id_vars=['data_coleta'], 
        value_vars=['preco_compra_usd', 'preco_compra_eur'], 
        var_name='moeda', 
        value_name='Preço de Compra (R$)',
    )

    # Renomeando as legendas para o gráfico
    df_longo['moeda'] = df_longo['moeda'].map(
        {'preco_compra_usd': 'Dólar Comercial', 'preco_compra_eur': 'Euro (EUR)'}
    )

    # Criando o gráfico interativo com o Plotly
    fig = px.line(
        df_longo,
        x='data_coleta',
        y='Preço de Compra (R$)',
        color='moeda',
        labels={'data_coleta': 'Data da Coleta'},
        markers=True, # Adiciona marcadores nos pontos de dados
        template='plotly_white', # Estilo do gráfico
    )

    # Exibindo o gráfico na tela
    st.plotly_chart(fig, use_container_width=True)

