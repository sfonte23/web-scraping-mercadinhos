import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re

def create_selenium_driver():
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    
    # Atualize com o caminho para o seu ChromeDriver
    service = Service('C:/Program Files/Google/chromedriver-win64/chromedriver.exe')
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def extract_lat_long_from_url(driver):
    try:
        # Aguarda a URL ser modificada após a página carregar completamente
        WebDriverWait(driver, 10).until(lambda d: '@' in d.current_url)
        # Obtém a URL da página atual
        url = driver.current_url
        # Usa uma expressão regular para extrair latitude e longitude do link
        match = re.search(r'@(.*?),(.*?)(?:,|$)', url)
        if match:
            latitude, longitude = match.groups()
            return f"{latitude},{longitude}"
        return 'N/A'
    except Exception as e:
        print(f"Erro ao extrair lat/long da URL: {e}")
        return 'N/A'

def extract_data_from_url(driver, url):
    try:
        driver.get(url)
        # Aguarda a página carregar completamente e o elemento do nome ficar visível
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div/div[1]/div[1]/h1'))
        )
        
        # Inicializa as variáveis de dados
        data = {
            'Nome': 'N/A',
            'Endereço': 'N/A',
            'Lat/Long': extract_lat_long_from_url(driver),
            'Link': url
        }
        
        # Extração de dados com tratamento de exceções
        try:
            # Extraindo o nome usando o XPath fornecido
            name_element = driver.find_element(By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div/div[1]/div[1]/h1')
            data['Nome'] = name_element.text.strip()
        except Exception as e:
            print(f"Erro ao capturar o nome: {e}")
        
        try:
            address_button = driver.find_element(By.CSS_SELECTOR, 'button.CsEnBe')
            data['Endereço'] = address_button.get_attribute('aria-label').split('Endereço: ')[-1]
        except Exception as e:
            print(f"Erro ao capturar o endereço: {e}")
        
        # Imprime os dados extraídos no console
        print(f"Nome: {data['Nome']}")
        print(f"Endereço: {data['Endereço']}")
        print(f"Lat/Long: {data['Lat/Long']}")
        print(f"Link: {data['Link']}")
        print("-" * 40)
        
        return data
    except Exception as e:
        print(f"Erro ao processar {url}: {e}")
        return {
            'Nome': 'Erro',
            'Endereço': 'Erro',
            'Lat/Long': extract_lat_long_from_url(driver),
            'Link': url
        }

def process_csv_and_save_to_excel(input_csv, output_excel):
    try:
        # Lê o CSV com uma coluna de links usando ; como delimitador
        df = pd.read_csv(input_csv, names=['Links'], delimiter=';')
        
        # Cria uma lista para armazenar os dados extraídos
        data = []
        
        # Inicializa o driver
        driver = create_selenium_driver()
        
        # Extrai os dados de cada URL
        for url in df['Links']:
            print(f"Processando {url}...")
            data.append(extract_data_from_url(driver, url))
        
        # Fecha o driver
        driver.quit()
        
        # Cria um DataFrame com os dados
        df_result = pd.DataFrame(data)
        
        # Salva o DataFrame em um arquivo Excel
        df_result.to_excel(output_excel, index=False)
        print(f"Dados salvos em {output_excel}")
    
    except pd.errors.ParserError as e:
        print(f"Erro ao ler o arquivo CSV: {e}")
    except Exception as e:
        print(f"Erro inesperado: {e}")

if __name__ == "__main__":
    input_csv = 'mercadinhos_links.csv'  # Nome do arquivo CSV com os links
    output_excel = 'mercadinhos_dados.xlsx'  # Nome do arquivo Excel para salvar os dados
    
    process_csv_and_save_to_excel(input_csv, output_excel)
