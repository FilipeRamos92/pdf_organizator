import os
import customtkinter as ctk
from tkinter import filedialog, messagebox
from pypdf import PdfWriter

# Configuração visual do CustomTkinter
ctk.set_appearance_mode("System")  # Segue o tema do Windows (Claro ou Escuro)
ctk.set_default_color_theme("blue")

class PDFMergerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Consolidador de PDF Local")
        self.geometry("750x500")
        self.lista_arquivos = []

        # --- INTERFACE GRÁFICA ---

        # Variável para rastrear o índice do arquivo selecionado (começa em -1 significa nenhum)
        self.item_selecionado_idx = -1
        # Lista para guardar os botões/labels visuais de cada arquivo
        self.botoes_arquivos = []
        
        # Título
        self.lbl_titulo = ctk.CTkLabel(self, text="Consolidador de PDFs", font=ctk.CTkFont(size=20, weight="bold"))
        self.lbl_titulo.pack(pady=20)

        # Container para os botões de ação superior (Corrigido: sem o px=20)
        self.frame_botoes = ctk.CTkFrame(self)
        self.frame_botoes.pack(pady=10, fill="x", padx=20)

        self.btn_adicionar = ctk.CTkButton(self.frame_botoes, text="Selecionar PDFs", command=self.adicionar_pdfs)
        self.btn_adicionar.pack(side="left", padx=10, pady=10)

        self.btn_limpar = ctk.CTkButton(self.frame_botoes, text="Limpar Lista", fg_color="gray", command=self.limpar_lista)
        self.btn_limpar.pack(side="right", padx=10, pady=10)

        self.btn_subir = ctk.CTkButton(self.frame_botoes, text="🔼 Subir", width=80, fg_color="#3a3a3a", command=self.mover_subir)
        self.btn_subir.pack(side="left", padx=5, pady=10)

        self.btn_descer = ctk.CTkButton(self.frame_botoes, text="🔽 Descer", width=80, fg_color="#3a3a3a", command=self.mover_descer)
        self.btn_descer.pack(side="left", padx=5, pady=10)
        
        self.btn_excluir = ctk.CTkButton(self.frame_botoes, text="❌ Excluir", width=80, fg_color="#912a2a", hover_color="#b33b3b", command=self.excluir_item)
        self.btn_excluir.pack(side="left", padx=5, pady=10)

        # Substitui o CTkTextbox por um Frame com Scroll integrado
        self.frame_lista = ctk.CTkScrollableFrame(self, width=515, height=200)
        self.frame_lista.pack(pady=10, padx=20, fill="both", expand=True)

        # Botão principal de execução
        self.btn_salvar = ctk.CTkButton(self, text="Mesclar e Salvar PDF", fg_color="green", hover_color="darkgreen", command=self.salvar_pdf)
        self.btn_salvar.pack(pady=20)
        
        # Inicializa o texto padrão
        self.atualizar_interface_lista()

    # --- LÓGICA DO APP ---

    def adicionar_pdfs(self):
        arquivos = filedialog.askopenfilenames(
            title="Selecione os arquivos PDF",
            filetypes=[("Arquivos PDF", "*.pdf")]
        )
        if arquivos:
            self.lista_arquivos.extend(arquivos)
            self.atualizar_interface_lista()

    def limpar_lista(self):
        self.lista_arquivos.clear()
        self.atualizar_interface_lista()

    def atualizar_interface_lista(self):
        # Destrói os componentes visuais antigos de dentro do frame
        for widget in self.frame_lista.winfo_children():
            widget.destroy()
        self.botoes_arquivos.clear()

        if not self.lista_arquivos:
            lbl_vazio = ctk.CTkLabel(self.frame_lista, text="Nenhum arquivo selecionado...")
            lbl_vazio.pack(pady=20)
            self.item_selecionado_idx = -1
            return

        # Desenha cada arquivo como um botão clicável
        for idx, arquivo in enumerate(self.lista_arquivos):
            nome_arquivo = os.path.basename(arquivo)
            
            # Define a cor baseado em estar selecionado ou não
            cor_fundo = "#1f538d" if idx == self.item_selecionado_idx else "transparent"
            
            btn_item = ctk.CTkButton(
                self.frame_lista, 
                text=f"{idx + 1}. {nome_arquivo}", 
                anchor="w",
                fg_color=cor_fundo,
                hover_color="#2a6ab3",
                command=lambda i=idx: self.selecionar_item(i)
            )
            btn_item.pack(fill="x", padx=5, pady=2)
            self.botoes_arquivos.append(btn_item)

    def salvar_pdf(self):
        if not self.lista_arquivos:
            messagebox.showwarning("Aviso", "Por favor, adicione pelo menos um PDF.")
            return

        # Abre a caixa de diálogo para escolher onde salvar o resultado
        local_salvamento = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("Arquivo PDF", "*.pdf")],
            title="Salvar PDF Consolidado como..."
        )

        if local_salvamento:
            try:
                # Usando o PdfWriter atualizado da pypdf
                merger = PdfWriter()
                for pdf in self.lista_arquivos:
                    merger.append(pdf)
                
                with open(local_salvamento, "wb") as f:
                    merger.write(f)
                merger.close()

                messagebox.showinfo("Sucesso!", f"PDF gerado com sucesso em:\n{local_salvamento}")
                self.limpar_lista()
            except Exception as e:
                messagebox.showerror("Erro", f"Ocorreu um erro ao juntar os arquivos:\n{str(e)}")

    def mover_subir(self):
        idx = self.item_selecionado_idx
        # Só pode subir se houver algo selecionado e não for o primeiro item (idx 0)
        if idx > 0:
            # Troca de posição no array
            self.lista_arquivos[idx], self.lista_arquivos[idx-1] = self.lista_arquivos[idx-1], self.lista_arquivos[idx]
            # Atualiza o índice selecionado para acompanhar o arquivo que subiu
            self.item_selecionado_idx = idx - 1
            self.atualizar_interface_lista()

    def mover_descer(self):
        idx = self.item_selecionado_idx
        # Só pode descer se houver algo selecionado e não for o último item
        if idx != -1 and idx < len(self.lista_arquivos) - 1:
            # Troca de posição no array
            self.lista_arquivos[idx], self.lista_arquivos[idx+1] = self.lista_arquivos[idx+1], self.lista_arquivos[idx]
            # Atualiza o índice selecionado para acompanhar o arquivo que desceu
            self.item_selecionado_idx = idx + 1
            self.atualizar_interface_lista()

    def selecionar_item(self, idx):
        self.item_selecionado_idx = idx
        self.atualizar_interface_lista()

    def excluir_item(self):
        idx = self.item_selecionado_idx
        # Só executa se houver um item selecionado válido
        if idx != -1:
            # Remove o arquivo da lista usando o índice selecionado
            self.lista_arquivos.pop(idx)
            # Reseta a seleção para nenhum item
            self.item_selecionado_idx = -1
            # Atualiza a tela
            self.atualizar_interface_lista()

if __name__ == "__main__":
    app = PDFMergerApp()
    app.mainloop()