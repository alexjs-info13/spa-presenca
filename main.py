import tkinter as tk
from tkinter import messagebox
import mysql.connector
from mysql.connector import Error

# ===============================================
# CLASSE DE CONEXÃO COM O BANCO DE DADOS
# ===============================================
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

# ===============================================
# TELA DE LOGIN - SISTEMA DE PRESENÇA ACADÊMICA (SPA)
# ===============================================
class TelaLogin:
    def __init__(self, root):
        self.root = root
        self.root.title("SPA - Sistema de Presença Acadêmica | Login")
        self.root.geometry("450x550")
        self.root.config(bg="#f4f6f9")
        self.root.resizable(False, False)

        # Container Principal
        frame_principal = tk.Frame(root, bg="#ffffff", padx=30, pady=30)
        frame_principal.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=380, height=480)

        # Título / Cabeçalho
        titulo_label = tk.Label(frame_principal, text="SPA", font=("Arial", 24, "bold"), fg="#1b365d", bg="#ffffff")
        titulo_label.pack(pady=(10, 0))

        sub_label = tk.Label(frame_principal, text="SISTEMA DE PRESENÇA ACADÊMICA", font=("Arial", 9, "bold"), fg="#4b6b94", bg="#ffffff")
        sub_label.pack(pady=(0, 20))

        # Campo CPF
        lbl_cpf = tk.Label(frame_principal, text="CPF:", font=("Arial", 10, "bold"), fg="#333333", bg="#ffffff", anchor="w")
        lbl_cpf.pack(fill="x", pady=(5, 0))
        
        self.entry_cpf = tk.Entry(frame_principal, font=("Arial", 12), relief="solid", bd=1)
        self.entry_cpf.pack(fill="x", ipymin=6, pady=(0, 15))

        # Campo Senha
        lbl_senha = tk.Label(frame_principal, text="Senha:", font=("Arial", 10, "bold"), fg="#333333", bg="#ffffff", anchor="w")
        lbl_senha.pack(fill="x", pady=(5, 0))
        
        self.entry_senha = tk.Entry(frame_principal, font=("Arial", 12), show="*", relief="solid", bd=1)
        self.entry_senha.pack(fill="x", ipymin=6, pady=(0, 20))

        # Botão Entrar
        btn_entrar = tk.Button(frame_principal, text="Entrar no Sistema", font=("Arial", 11, "bold"), 
                               bg="#1a56db", fg="#ffffff", relief="flat", cursor="hand2", command=self.realizar_login)
        btn_entrar.pack(fill="x", ipymin=8, pady=(10, 0))

    def realizar_login(self):
        cpf = self.entry_cpf.get().strip()
        senha = self.entry_senha.get().strip()

        if not cpf or not senha:
            messagebox.showwarning("Aviso", "Preencha todos os campos!")
            return

        # Teste de conexão e validação básica simulada/banco
        conexao = ConexaoBD.conectar()
        if conexao:
            try:
                cursor = conexao.cursor(dictionary=True)
                query = "SELECT * FROM usuarios WHERE cpf = %s AND senha = %s"
                cursor.execute(query, (cpf, senha))
                usuario = cursor.fetchone()
                
                if usuario or (cpf == "admin" and senha == "123"): # Exemplo de fallback para testes
                    messagebox.showinfo("Sucesso", "Login realizado com sucesso como Administrador!")
                    # Aqui você chamaria a próxima tela do sistema (Painel do Professor/Aluno)
                else:
                    messagebox.showerror("Erro", "CPF ou senha inválidos!")
                
                cursor.close()
                conexao.close()
            except Error as e:
                messagebox.showerror("Erro de Banco", f"Erro ao consultar banco de dados: {e}")
        else:
            # Fallback caso o banco não esteja ativo no momento do teste visual
            if cpf == "00000000000" and senha == "123":
                messagebox.showinfo("Sucesso", "Login realizado com sucesso!")
            else:
                messagebox.showerror("Erro de Conexão", "Não foi possível conectar ao banco de dados MySQL.")

# Execução da Aplicação
if __name__ == "__main__":
    root = tk.Tk()
    app = TelaLogin(root)
    root.mainloop()