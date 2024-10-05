# Web Scraping de Mercadinhos

Este projeto utiliza Selenium e Python para coletar informações de mercadinhos, supermercados e estabelecimentos similares. O objetivo é extrair dados úteis e organizá-los em formatos acessíveis para análise.

## Estrutura do Repositório

- `src/`: contém os scripts Python do projeto.
  - `main.py`: script principal que inicia o scraper e coleta os links.
  - `map_scraper.py`: classe que implementa a lógica de coleta de links e dados.
  - `data_extractor.py`: contém funções para extrair dados de URLs específicas.
- `data/`: pasta para armazenar os arquivos de saída.
  - `mercadinhos_links.csv`: arquivo CSV contendo os links coletados.
  - `mercadinhos_dados.xlsx`: arquivo Excel com os dados extraídos.

## Observações sobre a LGPD

Este projeto foi desenvolvido em conformidade com a Lei Geral de Proteção de Dados (LGPD) do Brasil. Os dados coletados são informações públicas disponíveis na internet, especificamente no Google Maps. A coleta de dados foi realizada de forma ética e responsável, e não inclui informações pessoais ou sensíveis.

## Acesso aos Dados

Os dados coletados estão disponíveis na pasta `data` deste repositório e podem ser acessados livremente. Você pode utilizá-los para análises e estudos, respeitando sempre a legislação vigente e os direitos dos proprietários dos dados.

## Instalação

1. Clone este repositório:
   ```bash
   git clone https://github.com/seuusuario/web-scraping-mercadinhos.git
   cd web-scraping-mercadinhos
2. Instale as dependências necessárias:
    ```bash
    pip install -r requirements.txt

## Uso
Execute o script principal para coletar os links:
    ```bash
    python src/main.py

Após a coleta, o arquivo mercadinhos_links.csv será gerado na pasta data/.

## Contribuições
Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou enviar pull requests.

## Licença
Este projeto está licenciado sob a Licença MIT.

### Observações sobre o Código

1. **Separação de Responsabilidades**: A classe `MapScraper` em `map_scraper.py` deve ser responsável apenas pela coleta de links e interações com a página. A lógica de extração de dados de cada link deve ficar em `data_extractor.py`.

2. **Organização do Código**: O arquivo `main.py` deve ser o ponto de entrada do projeto, enquanto o restante da lógica de scraping pode ser organizada em funções e classes.

3. **Manutenção do Código**: Use um arquivo `requirements.txt` para listar todas as dependências do projeto. Você pode gerá-lo com:
   ```bash
   pip freeze > requirements.txt