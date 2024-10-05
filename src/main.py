from map_scraper import MapScraper;

def main():
    # Caminho para o ChromeDriver e Chrome
    chrome_driver_path = r'C:\Program Files\Google\chromedriver-win64\chromedriver.exe'
    chrome_path = r'C:\Program Files\Google\chrome-win64\chrome.exe'
    
    # Inicializa o scraper
    scraper = MapScraper(chrome_driver_path, chrome_path)
    
    # Lista de termos de pesquisa
    search_terms = ['Supermercado' ,'Mercado' , 'Mercadinho' , 'Minimercado' , 'Mercearia' , 
    'Quitanda' , 'Hortifruti' , 'Padaria'  , 'Armazém' , 'Market' , 'Marché'] 

    
    all_collected_links = set()  # Usar um set para evitar duplicidades
    
    try:
        for term in search_terms:
            links = scraper.collect_links(term)
            all_collected_links.update(links)  # Atualiza o set com novos links
        
        # Salva os links em um arquivo CSV
        scraper.save_links_to_csv(list(all_collected_links), 'mercadinhos_links.csv')
    
    finally:
        # Fecha o navegador
        scraper.close()

if __name__ == "__main__":
    main()
