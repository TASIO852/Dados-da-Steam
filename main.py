import requests
from bs4 import BeautifulSoup
import pandas as pd
from headers import headers

def fetch_html(url: str, headers: dict) -> str:
    """
    Esta função busca o conteúdo HTML bruto de uma determinada URL.
    """
    response = requests.get(url, headers=headers)
    return BeautifulSoup(response.content, 'html.parser')

def scrape_table(soup: BeautifulSoup) -> pd.DataFrame:
    """
    Esta função extrai o conteúdo da tabela do HTML parseado.
    """
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
        df = df.rename(columns={0: 'Nome do jogo', 1: 'Desconto %', 2: 'Preco', 3: 'Rating %', 5: 'Data'})
        
        # Mantém apenas os dois primeiros dígitos na coluna 'rating'.
        df['Rating %'] = df['Rating %'].str[:2]
        df['Preco'] = df['Preco'].str.replace('R', '').str.strip()
        
        # Mantém apenas as três primeiras palavras na primeira coluna.
        df['Nome do jogo'] = df['Nome do jogo'].apply(lambda x: ' '.join(x.split()[:3]) if x is not None else None)
        
        # Remove linhas nulas.
        df = df.dropna()

        if 4 in df.columns:
            df = df.drop(columns=4)

    return df

def save_to_csv(df: pd.DataFrame, file_path: str):
    """
    Esta função salva o DataFrame em um arquivo CSV.
    """
    df.to_csv(file_path, index=False)

if __name__ == "__main__":
    url = 'https://steamdb.info/sales/'
    soup = fetch_html(url, headers)
    df = scrape_table(soup)
    
    if not df.empty:
        save_to_csv(df, 'C:/Users/tarsi/OneDrive/Documentos/Projects/Data Science/Dados da Steam/Data/output.csv')
