import hashlib
from collections import defaultdict


def buscar_registros_duplicados(caminho_arquivo):
    registros_por_hash = defaultdict(list)

    try:
        with open(caminho_arquivo, "r", encoding="utf-8", errors="ignore") as arquivo:
            for linha in arquivo:
                linha = linha.strip()
                if not linha:
                    continue
                h = hashlib.md5(linha.encode("utf-8")).hexdigest()
                registros_por_hash[h].append(linha)
    except (OSError, IOError):
        return {}

    return {h: linhas for h, linhas in registros_por_hash.items() if len(linhas) > 1}
