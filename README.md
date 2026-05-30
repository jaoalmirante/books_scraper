# Books Scraper

Scraper desenvolvido em Python para coletar dados de livros do site [books.toscrape.com](https://books.toscrape.com).

## Funcionalidades

- Coleta título, preço, rating e disponibilidade de todos os 1000 livros
- Paginação automática (50 páginas)
- Retry com backoff exponencial
- Simulação de comportamento humano com delays aleatórios e headers reais
- Saída em CSV e JSON
- Containerizado com Docker

## Tecnologias

- Python 3.12
- requests + BeautifulSoup4
- pandas
- Docker + Docker Compose

## Como rodar

### Com Docker (recomendado)
```bash
docker-compose up --build
```

### Localmente
```bash
pip install -r requirements.txt
python main.py
```

Os arquivos gerados ficam na pasta `output/`.