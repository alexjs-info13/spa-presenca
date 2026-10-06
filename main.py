import tkinter as tk
from tkinter import messagebox
import mysql.connector
from mysql.connector import Error
import os

# ==========================================
# CLASSE DE CONEXÃO COM O BANCO DE DADOS
# ==========================================
class ConexaoBD:
    @staticmethod
    def conectar():
        try:
            conexao = mysql.connector.connect(
                host="localhost",
                database="db_spa_presenca",
                user="root",
                password=""
            )
            return conexao
        except Error as e:
            return None

# ==========================================
# INTERFACE GRÁFICA (TELA DE LOGIN - TKINTER)
# ==========================================
class TelaLogin:
    def __init__(self, master):
        self.master = master
        self.master.title("SPA - Sistema de Presença Acadêmica | Login")
        self.master.geometry("400x480")
        self.master.config(bg="#f0f2f5")
        self.master.resizable(False, False)

        # Centralizar a janela na tela
        self.centralizar_janela()

        # --- TÍTULO E LOGO ---
        try:
            # Caminho correto considerando a pasta "Imagens"
            self.logo_img = tk.PhotoImage(file="Imagens/Logo_SPA.png")
            self.logo_pequena = self.logo_img.subsample(2, 2) 
            
            self.lbl_logo = tk.Label(master, image=self.logo_pequena, bg="#f0f2f5")
            self.lbl_logo.pack(pady=(15, 5))
        except Exception as e:
            # Mostra o erro exato no terminal para sabermos o porquê de falhar
            print(f"Erro ao carregar a imagem: {e}")
            
            # Se a imagem não for encontrada, exibe um título em texto
            self.lbl_titulo = tk.Label(master, text="🎓 Sistema SPA", font=("Arial", 18, "bold"), bg="#f0f2f5", fg="#1f2937")
            self.lbl_titulo.pack(pady=20)

        self.lbl_sub = tk.Label(master, text="Controle de Frequência Escolar", font=("Arial", 10), bg="#f0f2f5", fg="#4b5563")
        self.lbl_sub.pack(pady=(0, 15))

        # --- FRAME DO FORMULÁRIO ---
        form_frame = tk.Frame(master, bg="#ffffff", bd=2, relief="groove")
        form_frame.pack(pady=10, padx=30, fill="both", expand=True)

        # Campo CPF
        tk.Label(form_frame, text="CPF:", font=("Arial", 10, "bold"), bg="#ffffff", fg="#374151").pack(anchor="w", padx=20, pady=(20, 5))
        self.entry_cpf = tk.Entry(form_frame, font=("Arial", 12), bd=1, relief="solid")
        self.entry_cpf.pack(fill="x", padx=20, pady=(0, 10))

        # Campo Senha
        tk.Label(form_frame, text="Senha:", font=("Arial", 10, "bold"), bg="#ffffff", fg="#374151").pack(anchor="w", padx=20, pady=(5, 5))
        self.entry_senha = tk.Entry(form_frame, font=("Arial", 12), show="*", bd=1, relief="solid")
        self.entry_senha.pack(fill="x", padx=20, pady=(0, 20))

        # Botão de Login
        self.btn_login = tk.Button(form_frame, text="Entrar no Sistema", font=("Arial", 11, "bold"), bg="#2563eb", fg="white", bd=0, relief="flat", cursor="hand2", command=self.realizar_login)
        self.btn_login.pack(fill="x", padx=20, pady=(10, 20))

        # Rodapé
        lbl_rodape = tk.Label(master, text="Grau Técnico • Curso de TI", font=("Arial", 8), bg="#f0f2f5", fg="#9ca3af")
        lbl_rodape.pack(side="bottom", pady=15)

    def centralizar_janela(self):
        self.master.update_idletasks()
        largura = 400
        altura = 480
        x = (self.master.winfo_screenwidth() // 2) - (largura // 2)
        y = (self.master.winfo_screenheight() // 2) - (altura // 2)
        self.master.geometry(f"{largura}x{altura}+{x}+{y}")

    def realizar_login(self):
        cpf = self.entry_cpf.get().strip()
        senha = self.entry_senha.get().strip()

        if not cpf or not senha:
            messagebox.showwarning("Atenção", "Preencha todos os campos (CPF e Senha)!")
            return

        # Simulação de verificação inicial (depois ligaremos direto com o MySQL)
        if cpf == "admin" and senha == "admin":
            messagebox.showinfo("Sucesso", "Login realizado com sucesso como Administrador!")
        else:
            # Testando conexão com o banco ao tentar logar
            conexao = ConexaoBD.conectar()
            if conexao:
                messagebox.showinfo("Conexão", "Conexão com o banco ativa, validando credenciais...")
                conexao.close()
            else:
                messagebox.showerror("Erro", "Falha na conexão com o banco de dados ou usuário inválido.")

# ==========================================
# EXECUÇÃO DA APLICAÇÃO
# ==========================================
if __name__ == "__main__":
    root = tk.Tk()
    app = TelaLogin(root)
    root.mainloop()
