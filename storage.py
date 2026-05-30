import json
import logging
import pandas as pd
from pathlib import Path

logger = logging.getLogger(__name__)

OUTPUT_DIR = Path("output")

def garantir_pasta():
    """"
    Cria a pasta output se não existir.
    exist_ok=True evita erro se já existir.
    """
    OUTPUT_DIR.mkdir(exist_ok=True)

def salvar_csv(dados: list[dict], nome_arquivo: str = "livros.csv"):
    """"
    Recebe lista de dicionários e salva como CSV.
    encoding utf-8-sig garante que acentos abrem corretamente no Excel.
    """
    garantir_pasta()
    caminho = OUTPUT_DIR / nome_arquivo

    df = pd.DataFrame(dados)
    df.to_csv(caminho, index=False, encoding="utf-8-sig")

    logger.info(f"CSV salvo em {caminho} — {len(dados)} registros")

def salvar_json(dados: list[dict], nome_arquivo: str = "livros.json"):
    """
    Recebe lista de dicionários e salva como JSON formatado.
    ensure_ascii=False mantém caracteres especiais como acentos.
    indent=2 deixa o arquivo legível.
    """
    garantir_pasta()
    caminho = OUTPUT_DIR / nome_arquivo

    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)

    logger.info(f"JSON salvo em {caminho} — {len(dados)} registros")

def salvar_tudo(dados: list[dict]):
    """
    Atalho para salvar nos dois formatos de uma vez.
    """
    salvar_csv(dados)
    salvar_json(dados)