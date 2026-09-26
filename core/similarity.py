import difflib

from PIL import Image
import imagehash

EXTENSOES_IMAGEM = {".jpg", ".jpeg", ".png", ".bmp", ".gif", ".webp"}
EXTENSOES_TEXTO = {".txt", ".md", ".csv", ".json", ".py"}


def _hash_perceptual(caminho):
    with Image.open(caminho) as img:
        return imagehash.phash(img)


def encontrar_imagens_similares(arquivos, limite=5):
    imagens = [a for a in arquivos if a.suffix.lower() in EXTENSOES_IMAGEM]

    hashes = []
    for caminho in imagens:
        try:
            hashes.append((caminho, _hash_perceptual(caminho)))
        except Exception:
            continue

    return _agrupar_por_proximidade(hashes, lambda a, b: a - b <= limite)


def _similaridade_texto(caminho_a, caminho_b):
    texto_a = caminho_a.read_text(encoding="utf-8", errors="ignore")
    texto_b = caminho_b.read_text(encoding="utf-8", errors="ignore")
    return difflib.SequenceMatcher(None, texto_a, texto_b).ratio()


def encontrar_textos_similares(arquivos, limite=0.85):
    textos = [a for a in arquivos if a.suffix.lower() in EXTENSOES_TEXTO]

    grupos = []
    usados = set()
    for i, caminho_a in enumerate(textos):
        if caminho_a in usados:
            continue
        grupo = [caminho_a]
        for caminho_b in textos[i + 1:]:
            if caminho_b in usados:
                continue
            try:
                razao = _similaridade_texto(caminho_a, caminho_b)
            except Exception:
                continue
            if razao >= limite:
                grupo.append(caminho_b)
                usados.add(caminho_b)
        if len(grupo) > 1:
            usados.add(caminho_a)
            grupos.append(grupo)
    return grupos


def _agrupar_por_proximidade(itens_com_chave, sao_proximos):
    grupos = []
    usados = set()
    for i, (caminho_a, chave_a) in enumerate(itens_com_chave):
        if caminho_a in usados:
            continue
        grupo = [caminho_a]
        for caminho_b, chave_b in itens_com_chave[i + 1:]:
            if caminho_b in usados:
                continue
            if sao_proximos(chave_a, chave_b):
                grupo.append(caminho_b)
                usados.add(caminho_b)
        if len(grupo) > 1:
            usados.add(caminho_a)
            grupos.append(grupo)
    return grupos
