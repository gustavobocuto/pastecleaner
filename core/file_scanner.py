import os
from collections import defaultdict
from pathlib import Path

from core.hash_utils import hash_arquivo


def escanear_pastas(pastas):
    arquivos = []
    for pasta in pastas:
        for raiz, _, nomes in os.walk(pasta):
            for nome in nomes:
                arquivos.append(Path(raiz) / nome)
    return arquivos


def agrupar_por_hash(arquivos):
    por_hash = defaultdict(list)
    for caminho in arquivos:
        try:
            h = hash_arquivo(caminho)
        except (OSError, IOError):
            continue
        por_hash[h].append(caminho)
    return {h: c for h, c in por_hash.items() if len(c) > 1}


def agrupar_por_nome(arquivos):
    por_nome = defaultdict(list)
    for caminho in arquivos:
        por_nome[caminho.name].append(caminho)
    return {nome: c for nome, c in por_nome.items() if len(c) > 1}


def separar_versoes(grupos_por_nome, grupos_por_hash):
    ja_marcados = {c for grupo in grupos_por_hash.values() for c in grupo}
    versoes = {}
    for nome, caminhos in grupos_por_nome.items():
        distintos = [c for c in caminhos if c not in ja_marcados]
        if len(distintos) > 1:
            versoes[nome] = distintos
    return versoes
