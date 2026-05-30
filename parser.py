from bs4 import BeautifulSoup

RATING_MAP = {
    "One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5
}

def parse_livros(html: str) -> list[dict]:
    """
    Recebe o HTML de uma página e retorna
    uma lista de dicionários com os dados de cada livro.
    """
    soup = BeautifulSoup(html, "html.parser")
    livros = []

    for article in soup.select("article.product_pod"):
        titulo = article.select_one("h3 a")["title"]
        preco = article.select_one("p.price_color").text.strip()
        rating_texto = article.select_one("p.star-rating")["class"][1]
        rating = RATING_MAP.get(rating_texto, 0)
        disponivel = article.select_one(".availability").text.strip()

        livros.append({
            "titulo": titulo,
            "preco": preco,
            "rating": rating,
            "disponivel": disponivel
        })

    return livros

def get_proxima_pagina(html: str) -> str | None:
    """
    Verifica se existe botão 'next' na paginação.
    Retorna o caminho relativo da próxima página ou None.
    """
    soup = BeautifulSoup(html, "html.parser")
    next_btn = soup.select_one("li.next a")
    return next_btn["href"] if next_btn else None