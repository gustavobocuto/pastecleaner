import hashlib

def calcular_hash_arquivo(caminho_arquivo, algoritmo='md5'):
    hash_alg = hashlib.new(algoritmo)
    with open(caminho_arquivo, 'rb') as arquivo:
        for bloco in iter(lambda: arquivo.read(4096), b""):
            hash_alg.update(bloco)
    return hash_alg.hexdigest()