import hashlib


def hash_arquivo(caminho, algoritmo="md5", bloco=8192):
    h = hashlib.new(algoritmo)
    with open(caminho, "rb") as arquivo:
        for parte in iter(lambda: arquivo.read(bloco), b""):
            h.update(parte)
    return h.hexdigest()
