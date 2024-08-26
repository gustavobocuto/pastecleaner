from collections import defaultdict
import hashlib

def buscar_registros_duplicados(caminho_arquivo):
    registros_por_hash = defaultdict(list)
    
    try:
        with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
            for linha in arquivo:
                # Calcula o hash da linha
                hash_linha = hashlib.md5(linha.strip().encode('utf-8')).hexdigest()
                # Adiciona a linha à lista de registros para o hash calculado
                registros_por_hash[hash_linha].append(linha.strip())
    except (OSError, IOError):
        return {}
    
    # Filtra registros que aparecem mais de uma vez
    duplicados = {hash_: linhas for hash_, linhas in registros_por_hash.items() if len(linhas) > 1}
    return duplicados
