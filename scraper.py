import requests
import time
import random
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

BASE_URL = "https://books.toscrape.com/catalogue/"
START_URL = "https://books.toscrape.com/catalogue/page-1.html"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
}

def criar_sessao() -> requests.Session:
    """
    Cria uma sessão HTTP reutilizável com headers padrão.
    Sessão mantém cookies automaticamente entre requests.
    """
    sessao = requests.Session()
    sessao.headers.update(HEADERS)
    return sessao

def buscar_pagina(sessao: requests.Session, url: str, tentativas: int = 3) -> str | None:
    """
    Faz GET na URL com retry manual.
    Aguarda um tempo aleatório entre tentativas para não parecer um bot.
    Retorna o HTML como string ou None se falhar.
    """
    for tentativa in range(1, tentativas + 1):
        try:
            espera = random.uniform(1.0, 2.5)
            time.sleep(espera)

            response = sessao.get(url, timeout=10)

            if response.status_code == 200:
                logger.info(f"OK ({response.status_code}) — {url}")
                response.encoding = "utf-8"
                return response.text
            elif response.status_code == 429:
                logger.warning(f"Rate limit atingido (429). Aguardando 10s...")
                time.sleep(10)
            else:
                logger.warning(f"Status inesperado {response.status_code} — {url}")
        except requests.exceptions.ConnectionError as e:
            logger.error(f"Erro de conexão na tentativa {tentativa} — {url}")
        
        if tentativa < tentativas:
            backoff = 2 ** tentativa
            logger.info(f"Aguardando {backoff}s antes de tentar novamente...")
            time.sleep(backoff)
    logger.error(f"Falhou após {tentativas} tentativas — {url}")
    return None

def montar_url(caminho_relativo: str) -> str:
    """
    Converte caminho relativo da paginação em URL absoluta.
    Ex: '../page-2.html' → 'https://books.toscrape.com/catalogue/page-2.html'
    """
    caminho = caminho_relativo.replace("../", "")
    return BASE_URL + caminho