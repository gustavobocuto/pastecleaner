from buscar_arquivos import buscar_arquivos_duplicados
from buscar_registros import buscar_registros_duplicados

import os

def buscar_duplicados(diretorio_inicial):
    # Buscar arquivos duplicados
    arquivos_duplicados = buscar_arquivos_duplicados(diretorio_inicial)
    if arquivos_duplicados:
        print("Arquivos duplicados encontrados:")
        for hash_, arquivos in arquivos_duplicados.items():
            print(f"Hash: {hash_}")
            for arquivo in arquivos:
                print(f" - {arquivo}")
    
    # Buscar registros duplicados em arquivos de texto
    for raiz, _, arquivos in os.walk(diretorio_inicial):
        for arquivo in arquivos:
            caminho_completo = os.path.join(raiz, arquivo)
            if arquivo.endswith('.txt'):
                registros_duplicados = buscar_registros_duplicados(caminho_completo)
                if registros_duplicados:
                    print(f"Registros duplicados encontrados no arquivo {caminho_completo}:")
                    for hash_, registros in registros_duplicados.items():
                        print(f"Hash: {hash_}")
                        for registro in registros:
                            print(f" - {registro}")

# Executar a busca
if __name__ == "__main__":
    # Substitua pelo caminho do diretório que deseja testar
    diretorio = "/caminho/para/o/diretorio"  
    buscar_duplicados(diretorio)
