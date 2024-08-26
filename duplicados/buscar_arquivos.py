import os
from collections import defaultdict
from duplicados.calcular_hash import calcular_hash_arquivo  # Certifique-se de que a importação está correta

def buscar_arquivos_duplicados(diretorio_inicial):
    arquivos_por_hash = defaultdict(list)
    
    for raiz, _, arquivos in os.walk(diretorio_inicial):
        for arquivo in arquivos:
            caminho_completo = os.path.join(raiz, arquivo)
            try:
                hash_arquivo = calcular_hash_arquivo(caminho_completo)
                arquivos_por_hash[hash_arquivo].append(caminho_completo)
            except (OSError, IOError):
                continue
    
    duplicados = {hash_: paths for hash_, paths in arquivos_por_hash.items() if len(paths) > 1}
    return duplicados

# Teste a função (opcional)
if __name__ == "__main__":
    diretorio_teste = "C:/Users/gusta/Documents"  # Substitua pelo caminho do diretório que deseja testar
    duplicados = buscar_arquivos_duplicados(diretorio_teste)
    if duplicados:
        print("Arquivos duplicados encontrados:")
        for hash_, arquivos in duplicados.items():
            print(f"Hash: {hash_}")
            for arquivo in arquivos:
                print(f" - {arquivo}")
    else:
        print("Nenhum arquivo duplicado encontrado.")
