import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
from duplicados.buscar_arquivos import buscar_arquivos_duplicados
from duplicados.buscar_registros import buscar_registros_duplicados
import threading

class Aplicacao:
    def __init__(self, master):
        self.master = master
        self.master.title("Busca de Arquivos e Registros Duplicados")
        
        self.frame = tk.Frame(master, padx=20, pady=20)
        self.frame.pack(padx=10, pady=10)

        self.label = tk.Label(self.frame, text="Selecione um diretório para buscar duplicados:")
        self.label.pack(pady=10)

        self.botao_selecionar = tk.Button(self.frame, text="Selecionar Diretório", command=self.selecionar_diretorio)
        self.botao_selecionar.pack(pady=10)

        self.botao_varredura_completa = tk.Button(self.frame, text="Varredura Completa", command=self.varredura_completa)
        self.botao_varredura_completa.pack(pady=10)

        self.tree = None
        self.progress = None

    def selecionar_diretorio(self):
        diretorio = filedialog.askdirectory()
        if diretorio:
            self.iniciar_varredura([diretorio])

    def iniciar_varredura(self, diretorios_iniciais):
        self.progress = ttk.Progressbar(self.frame, orient="horizontal", length=300, mode="indeterminate")
        self.progress.pack(pady=10)
        self.progress.start()

        self.thread = threading.Thread(target=self.buscar_duplicados, args=(diretorios_iniciais,))
        self.thread.start()
        self.master.after(100, self.verificar_thread)

    def verificar_thread(self):
        if self.thread.is_alive():
            self.master.after(100, self.verificar_thread)
        else:
            self.progress.stop()
            self.progress.destroy()

    def buscar_duplicados(self, diretorios_iniciais):
        arquivos_duplicados = {}
        for diretorio_inicial in diretorios_iniciais:
            duplicados = buscar_arquivos_duplicados(diretorio_inicial)
            arquivos_duplicados.update(duplicados)
        
        if arquivos_duplicados:
            self.exibir_duplicados(arquivos_duplicados)
        else:
            messagebox.showinfo("Resultado da Busca", "Nenhum arquivo duplicado encontrado.")

    def exibir_duplicados(self, arquivos_duplicados):
        if self.tree:
            self.tree.destroy()
        
        self.tree = ttk.Treeview(self.frame, columns=("Arquivo", "Hash"), show='headings', selectmode='extended')
        self.tree.heading("Arquivo", text="Arquivo")
        self.tree.heading("Hash", text="Hash")
        self.tree.pack(pady=10)
        
        for hash_, arquivos in arquivos_duplicados.items():
            for arquivo in arquivos:
                self.tree.insert("", tk.END, values=(arquivo, hash_))

        self.botao_eliminar = tk.Button(self.frame, text="Eliminar Selecionados", command=self.eliminar_selecionados)
        self.botao_eliminar.pack(pady=10)

    def eliminar_selecionados(self):
        selecionados = self.tree.selection()
        if not selecionados:
            messagebox.showwarning("Nenhuma Seleção", "Por favor, selecione os arquivos a serem eliminados.")
            return

        for item in selecionados:
            arquivo = self.tree.item(item, "values")[0]
            try:
                os.remove(arquivo)
                print(f"Arquivo removido: {arquivo}")
                self.tree.delete(item)
            except Exception as e:
                print(f"Erro ao remover {arquivo}: {e}")

        messagebox.showinfo("Eliminação Concluída", "Arquivos duplicados selecionados foram eliminados.")

    def varredura_completa(self):
        diretorios_iniciais = [
            os.path.expandvars(r'%ProgramFiles%'),
            os.path.expandvars(r'%ProgramFiles(x86)%'),
            os.path.expandvars(r'%USERPROFILE%')
        ]
        self.iniciar_varredura(diretorios_iniciais)

# Configuração da interface gráfica
app = tk.Tk()
Aplicacao(app)
app.mainloop()
