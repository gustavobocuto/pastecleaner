from PySide6.QtCore import QThread, Signal

from core.file_scanner import escanear_pastas, agrupar_por_hash, agrupar_por_nome, separar_versoes
from core.similarity import encontrar_imagens_similares, encontrar_textos_similares


class VarreduraWorker(QThread):
    progresso = Signal(str)
    concluido = Signal(dict)

    def __init__(self, pastas):
        super().__init__()
        self.pastas = pastas

    def run(self):
        self.progresso.emit("Listando arquivos...")
        arquivos = escanear_pastas(self.pastas)

        self.progresso.emit("Calculando hashes...")
        duplicados = agrupar_por_hash(arquivos)

        self.progresso.emit("Verificando nomes repetidos...")
        por_nome = agrupar_por_nome(arquivos)
        versoes = separar_versoes(por_nome, duplicados)

        self.progresso.emit("Comparando imagens parecidas...")
        imagens_similares = encontrar_imagens_similares(arquivos)

        self.progresso.emit("Comparando textos parecidos...")
        textos_similares = encontrar_textos_similares(arquivos)

        self.concluido.emit({
            "duplicados": duplicados,
            "versoes": versoes,
            "imagens_similares": imagens_similares,
            "textos_similares": textos_similares,
        })
