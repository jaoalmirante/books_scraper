import logging
import time
from scraper import criar_sessao, buscar_pagina, montar_url, START_URL
from parser import parse_livros, get_proxima_pagina
from storage import salvar_tudo

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

def coletar_todos_livros() -> list[dict]:
    """
    Navega por todas as páginas do site coletando os dados de cada livro.
    Para quando não houver mais página seguinte.
    """
    sessao = criar_sessao()
    todos_livros = []
    url_atual = START_URL
    pagina = 1

    while url_atual:
        logger.info(f"Coletando página {pagina} — {url_atual}")

        html = buscar_pagina(sessao, url_atual)

        if html is None:
            logger.error(f"Não foi possível obter a página {pagina}. Encerrando.")
            break

        livros = parse_livros(html)
        todos_livros.extend(livros)
        logger.info(f"Página {pagina} — {len(livros)} livros coletados "
                    f"(total até agora: {len(todos_livros)})")
        
        proxima = get_proxima_pagina(html)
        url_atual = montar_url(proxima) if proxima else None
        pagina += 1
    
    return todos_livros

def main():
    logger.info("Iniciando scraper — books.toscrape.com")
    inicio = time.time()

    dados = coletar_todos_livros()

    if dados:
        salvar_tudo(dados)
        duracao = time.time() - inicio
        logger.info(f"Concluído — {len(dados)} livros salvos em {duracao:.1f}s")
    else:
        logger.error("Nenhum dado coletado. Verifique os logs acima.")

if __name__ == "__main__":
    main()