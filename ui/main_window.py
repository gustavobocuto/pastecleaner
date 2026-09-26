import os
from pathlib import Path

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QListWidget, QFileDialog, QTabWidget, QTreeWidget, QTreeWidgetItem,
    QMessageBox, QLabel
)
from PySide6.QtCore import Qt
from send2trash import send2trash

from core.worker import VarreduraWorker


class JanelaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pasta Cleaner")
        self.resize(900, 600)

        self.pastas_selecionadas = []
        self.worker = None

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        linha_pastas = QHBoxLayout()
        self.lista_pastas = QListWidget()
        linha_pastas.addWidget(self.lista_pastas)

        botoes_pastas = QVBoxLayout()
        botao_adicionar = QPushButton("Adicionar pasta")
        botao_adicionar.clicked.connect(self.adicionar_pasta)
        botao_remover = QPushButton("Remover pasta")
        botao_remover.clicked.connect(self.remover_pasta)
        botoes_pastas.addWidget(botao_adicionar)
        botoes_pastas.addWidget(botao_remover)
        botoes_pastas.addStretch()
        linha_pastas.addLayout(botoes_pastas)
        layout.addLayout(linha_pastas)

        self.botao_buscar = QPushButton("Buscar duplicados")
        self.botao_buscar.clicked.connect(self.iniciar_busca)
        layout.addWidget(self.botao_buscar)

        self.status = QLabel("")
        layout.addWidget(self.status)

        self.abas = QTabWidget()
        self.arvore_duplicados = self._criar_arvore()
        self.arvore_versoes = self._criar_arvore()
        self.arvore_imagens = self._criar_arvore()
        self.arvore_textos = self._criar_arvore()

        self.abas.addTab(self.arvore_duplicados, "Duplicados exatos")
        self.abas.addTab(self.arvore_versoes, "Possíveis versões")
        self.abas.addTab(self.arvore_imagens, "Imagens parecidas")
        self.abas.addTab(self.arvore_textos, "Textos parecidos")
        layout.addWidget(self.abas)

        self.botao_apagar = QPushButton("Apagar selecionados (vai para a lixeira)")
        self.botao_apagar.clicked.connect(self.apagar_selecionados)
        layout.addWidget(self.botao_apagar)

    def _criar_arvore(self):
        arvore = QTreeWidget()
        arvore.setHeaderLabels(["Arquivo", "Tamanho"])
        arvore.setColumnWidth(0, 600)
        arvore.itemDoubleClicked.connect(self.abrir_pasta_do_item)
        return arvore

    def adicionar_pasta(self):
        pasta = QFileDialog.getExistingDirectory(self, "Selecionar pasta")
        if pasta and pasta not in self.pastas_selecionadas:
            self.pastas_selecionadas.append(pasta)
            self.lista_pastas.addItem(pasta)

    def remover_pasta(self):
        item = self.lista_pastas.currentItem()
        if item:
            self.pastas_selecionadas.remove(item.text())
            self.lista_pastas.takeItem(self.lista_pastas.row(item))

    def iniciar_busca(self):
        if not self.pastas_selecionadas:
            QMessageBox.warning(self, "Nenhuma pasta", "Adicione ao menos uma pasta antes de buscar.")
            return

        self.botao_buscar.setEnabled(False)
        self.worker = VarreduraWorker(list(self.pastas_selecionadas))
        self.worker.progresso.connect(self.status.setText)
        self.worker.concluido.connect(self.mostrar_resultado)
        self.worker.start()

    def mostrar_resultado(self, resultado):
        self.botao_buscar.setEnabled(True)
        self.status.setText("Busca concluída.")

        self._preencher_arvore(self.arvore_duplicados, resultado["duplicados"].values())
        self._preencher_arvore(self.arvore_versoes, resultado["versoes"].values())
        self._preencher_arvore(self.arvore_imagens, resultado["imagens_similares"])
        self._preencher_arvore(self.arvore_textos, resultado["textos_similares"])

    def _preencher_arvore(self, arvore, grupos):
        arvore.clear()
        for grupo in grupos:
            pai = QTreeWidgetItem([f"Grupo ({len(grupo)} arquivos)"])
            arvore.addTopLevelItem(pai)
            for caminho in grupo:
                caminho = Path(caminho)
                try:
                    tamanho = f"{caminho.stat().st_size / 1024:.1f} KB"
                except OSError:
                    tamanho = "?"
                filho = QTreeWidgetItem([str(caminho), tamanho])
                filho.setFlags(filho.flags() | Qt.ItemIsUserCheckable)
                filho.setCheckState(0, Qt.Unchecked)
                pai.addChild(filho)
            pai.setExpanded(True)

    def abrir_pasta_do_item(self, item, _coluna):
        if item.childCount() > 0:
            return
        caminho = Path(item.text(0))
        if caminho.exists():
            os.startfile(caminho.parent)

    def apagar_selecionados(self):
        selecionados = []
        for arvore in (self.arvore_duplicados, self.arvore_versoes, self.arvore_imagens, self.arvore_textos):
            for i in range(arvore.topLevelItemCount()):
                pai = arvore.topLevelItem(i)
                for j in range(pai.childCount()):
                    filho = pai.child(j)
                    if filho.checkState(0) == Qt.Checked:
                        selecionados.append(Path(filho.text(0)))

        if not selecionados:
            QMessageBox.information(self, "Nada selecionado", "Marque os arquivos que deseja apagar.")
            return

        tamanho_total = sum(c.stat().st_size for c in selecionados if c.exists())
        resposta = QMessageBox.question(
            self,
            "Confirmar exclusão",
            f"Você está prestes a mover {len(selecionados)} arquivo(s) para a lixeira "
            f"({tamanho_total / 1024 / 1024:.1f} MB no total).\n\nDeseja continuar?",
        )
        if resposta != QMessageBox.Yes:
            return

        falhas = []
        for caminho in selecionados:
            try:
                send2trash(str(caminho))
            except Exception as erro:
                falhas.append((caminho, erro))

        if falhas:
            texto = "\n".join(f"{c}: {e}" for c, e in falhas)
            QMessageBox.warning(self, "Alguns arquivos não foram apagados", texto)
        else:
            QMessageBox.information(self, "Concluído", "Arquivos movidos para a lixeira.")
