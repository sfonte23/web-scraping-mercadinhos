from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import csv

class MapScraper:
    def __init__(self, chrome_driver_path, chrome_path):
        # Configura o serviço do ChromeDriver
        self.service = Service(chrome_driver_path)
        # Configurações para rodar o Chrome com interface gráfica
        self.options = Options()
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--disable-dev-shm-usage')
        self.options.binary_location = chrome_path  # Especifica o caminho para o executável do Chrome
        # Inicia o navegador com as opções configuradas
        self.driver = webdriver.Chrome(service=self.service, options=self.options)
        print("Navegador iniciado.")
    
    def scroll_to_bottom(self):
        print("Rolando a página para baixo...")
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        while True:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            print("Aguardando 30 segundos para rolagem manual...")
            time.sleep(30)  # Espera 30 segundos para rolagem manual
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
        print("Rolagem completa.")
    
    def interact_with_page(self):
        # Adiciona uma interação para garantir que a página está ativa
        self.driver.execute_script("window.scrollBy(0, 100);")
        time.sleep(1)
        self.driver.execute_script("window.scrollBy(0, -100);")
        time.sleep(1)
        self.driver.execute_script("window.scrollBy(0, 100);")
        time.sleep(1)

    def collect_links(self, search_term):
        # Atualiza a URL base com o novo termo de pesquisa
        base_url = f"https://www.google.com/maps/search/{search_term}/@-22.9690939,-44.3000384,12z?entry=ttu"
        print(f"Acessando a URL sobre {search_term} no Maps: {base_url}")
        self.driver.get(base_url)
        
        # Interage com a página para garantir que ela esteja ativa
        self.interact_with_page()
        
        # Rolar a página para baixo e permitir rolagem manual
        self.scroll_to_bottom()
        
        # Coleta os links dos mercadinhos
        print("Coletando links...")
        try:
            # Encontra todos os elementos <a> com a classe 'hfpxzc'
            mercadinhos = self.driver.find_elements(By.CLASS_NAME, 'hfpxzc')
            
            # Lista para armazenar todos os links encontrados
            all_links = []
            
            for mercadinho in mercadinhos:
                link = mercadinho.get_attribute('href')
                if link and link not in all_links:  # Verifica se o link não é None e não está duplicado
                    all_links.append(link)
            
            print(f"Total de links encontrados: {len(all_links)}")
            return all_links
        except Exception as e:
            print(f"Erro ao coletar links: {e}")
            return []
    
    def save_links_to_csv(self, links, filename):
        print(f"Salvando links em um arquivo CSV: {filename}")
        with open(filename, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Link'])
            for link in links:
                writer.writerow([link])
        print("Links salvos com sucesso.")

    def close(self):
        # Mantém o navegador aberto por 5 segundos para visualização
        print("Navegador será fechado em 5 segundos...")
        time.sleep(5)
        # Fecha o navegador
        print("Fechando o navegador...")
        self.driver.quit()
