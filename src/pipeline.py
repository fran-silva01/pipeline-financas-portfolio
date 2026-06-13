import datetime # Para registrar a data e hora de execução do pipeline
import os # Para manipulação de arquivos e diretórios
import sqlite3
from urllib import response # Para interação com o banco de dados SQLite
import pandas as pd # Para manipulação de dados
import requests # Para fazer requisições HTTP
import time # Para adicionar um delay na verificação do arquivo, se necessário

def extrair_dados():
    print("Iniciando a extração de dados da API...")
    url = 'https://economia.awesomeapi.com.br/last/USD-BRL,EUR-BRL'

    headers = {
        'User-Agent': 'Mozilla/5.0'
    }
    for tentativa in range(3):
        response = requests.get(url, timeout=30, headers=headers)

        if response.status_code == 200:
            break

    print(f"Tentativa {tentativa+1}: Status {response.status_code}")
    time.sleep(10)

    if response.status_code == 200:
        dados = response.json()
        dolar_info = dados['USDBRL']
        euro_info = dados['EURBRL']

        registro = {
            'data_coleta': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'moeda_usd': dolar_info['code'],
            'preco_compra_usd': float(dolar_info['bid']),
            'moeda_eur': euro_info['code'],
            'preco_compra_eur': float(euro_info['bid']),
        }

        return pd.DataFrame([registro])
    else:
        print(f"Erro ao acessar a API. Status Code: {response.status_code}")
        return None

def salvar_no_banco(df):
    if df is None:
        print("Nenhum dado para salvar.")
        return
    
    print( "Conectando ao banco de dados SQLite...")
    # O '..'serve para subir um nível na hierarquia de diretórios, garantindo que o banco de dados seja criado na pasta correta.
    caminho_banco = os.path.join(
        os.path.dirname(__file__), '..', 'data', 'financas.db'
    )

    # Garante que a pasta 'data'existe na raiz do projeto
    os.makedirs(os.path.dirname(caminho_banco), exist_ok=True)

    conexao = sqlite3.connect(caminho_banco)
    df.to_sql('cotacoes', conexao, if_exists='append', index=False)
    conexao.close()
    print("Dados salvos com sucesso no SQLite!.")

if __name__ == "__main__":
    dados_atuais = extrair_dados()
    salvar_no_banco(dados_atuais)