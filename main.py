import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
from headers import headers
from google.cloud import bigquery

# Definir o caminho para o arquivo de credenciais
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="Caminho_da_sua_chave_no_seu_pc"

def fetch_html(url: str, headers: dict) -> str:
    response = requests.get(url, headers=headers)
    return BeautifulSoup(response.content, 'html.parser')

def scrape_table(soup: BeautifulSoup) -> pd.DataFrame:
    table = soup.find('table')
    if table is None:
        print("Nenhuma tabela encontrada na página.")
        return pd.DataFrame()

    data = [
        [element.text.strip() for element in row.find_all('td') if element.text.strip()]
        for row in soup.find_all('tr')
    ]

    df = pd.DataFrame(data)
    if not df.empty:
        df = df.replace('[^A-Za-z0-9 ]+', '', regex=True)
        df = df.rename(columns={0: 'Nome_do_jogo', 1: 'Desconto_porcent', 2: 'Preco', 3: 'Rating_porcent', 5: 'Data'})

        df['Rating_porcent'] = df['Rating_porcent'].str[:2]
        df['Preco'] = df['Preco'].str.replace('R', '').str.replace(',', '').apply(lambda x: float(x)/100 if x is not None else None)
        df['Nome_do_jogo'] = df['Nome_do_jogo'].apply(lambda x: ' '.join(x.split()[:3]) if x is not None else None)
        df = df.dropna()

        if 4 in df.columns:
            df = df.drop(columns=4)

    return df

def save_to_csv(df: pd.DataFrame, file_path: str):
    df.to_csv(file_path, index=False)

def load_df_to_bigquery(df: pd.DataFrame, table_id: str):
    client = bigquery.Client()
    job = client.load_table_from_dataframe(df, table_id)
    job.result() # Espera a conclusão do job
    print("Dados carregados com sucesso para a tabela do BigQuery.")

if __name__ == "__main__":
    url = 'https://steamdb.info/sales/'
    soup = fetch_html(url, headers)
    df = scrape_table(soup)
    
    if not df.empty:
        save_to_csv(df, 'C:/Users/tarsi/OneDrive/Documentos/Projects/Data Science/Dados da Steam/Data/output.csv')
        
        table_id = 'primeval-lotus-392716.steamvendas.steamvendas'
        load_df_to_bigquery(df, table_id)
