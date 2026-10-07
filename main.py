import tkinter as tk
from tkinter import messagebox
import os
from painel_principal import PainelPrincipal

try:
    import mysql.connector
    from mysql.connector import Error
    MYSQL_DISPONIVEL = True
except ImportError:
    MYSQL_DISPONIVEL = False


class ConexaoBD:
    @staticmethod
    def conectar():
        if not MYSQL_DISPONIVEL:
            return None
        try:
            conexao = mysql.connector.connect(
                host="localhost",
                database="db_spa_presenca",
                user="root",
                password=""
            )
            return conexao
        except Error:
            return None


class TelaLogin:
    def __init__(self, root):
        self.root = root
        self.root.title("SPA - Sistema de Presença Acadêmica | Login")
        self.root.geometry("450x580")
        self.root.config(bg="#f4f6f9")
        self.root.resizable(False, False)

        # --- CARREGAMENTO SEGURO DA LOGO PARA A TELA DE LOGIN ---
        self.logo_img = None
        try:
            diretorio_atual = os.path.dirname(os.path.abspath(__file__))
            caminho_logo = os.path.join(diretorio_atual, "Imagens", "Logo_SPA.png")
            if os.path.exists(caminho_logo):
                img_original = tk.PhotoImage(file=caminho_logo)
                # Reduz o tamanho da logo proporcionalmente para o login (ex: redimensionada por 6)
                self.logo_img = img_original.subsample(2, 2)  # Ajuste o fator de subsample conforme necessário
        except Exception as e:
            print(f"Aviso ao carregar logo na tela de login: {e}")

        # Frame Principal Centralizado
        frame_principal = tk.Frame(root, bg="#ffffff", padx=30, pady=25)
        frame_principal.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=380, height=520)

        # Exibe a logo se ela existir, caso contrário exibe o texto "SPA"
        if self.logo_img:
            lbl_logo = tk.Label(frame_principal, image=self.logo_img, bg="#ffffff")
            lbl_logo.pack(pady=(0, 5))
        else:
            titulo_label = tk.Label(frame_principal, text="SPA", font=("Arial", 24, "bold"), fg="#1b365d", bg="#ffffff")
            titulo_label.pack(pady=(5, 0))

        sub_label = tk.Label(frame_principal, text="SISTEMA DE PRESENÇA ACADÊMICA", font=("Arial", 8, "bold"), fg="#4b6b94", bg="#ffffff")
        sub_label.pack(pady=(0, 15))

        lbl_cpf = tk.Label(frame_principal, text="CPF ou Usuário:", font=("Arial", 10, "bold"), fg="#333333", bg="#ffffff", anchor="w")
        lbl_cpf.pack(fill="x", pady=(5, 0))
        
        self.entry_cpf = tk.Entry(frame_principal, font=("Arial", 12), relief="solid", bd=1)
        self.entry_cpf.pack(fill="x", ipady=4, pady=(0, 12))
        # Insere "admin" por padrão para facilitar os seus testes
        self.entry_cpf.insert(0, "admin")

        lbl_senha = tk.Label(frame_principal, text="Senha:", font=("Arial", 10, "bold"), fg="#333333", bg="#ffffff", anchor="w")
        lbl_senha.pack(fill="x", pady=(5, 0))
        
        self.entry_senha = tk.Entry(frame_principal, font=("Arial", 12), show="*", relief="solid", bd=1)
        self.entry_senha.pack(fill="x", ipady=4, pady=(0, 20))
        # Insere "admin" por padrão para facilitar os seus testes
        self.entry_senha.insert(0, "admin")

        btn_entrar = tk.Button(
            frame_principal, 
            text="Entrar no Sistema", 
            font=("Arial", 11, "bold"), 
            bg="#1a56db", 
            fg="#ffffff", 
            relief="flat", 
            cursor="hand2", 
            command=self.realizar_login
        )
        btn_entrar.pack(fill="x", ipady=6, pady=(5, 0))

    def realizar_login(self):
        cpf = self.entry_cpf.get().strip()
        senha = self.entry_senha.get().strip()

        if not cpf or not senha:
            messagebox.showwarning("Aviso", "Preencha todos os campos!")
            return

        usuario_encontrado = None
        if MYSQL_DISPONIVEL:
            conexao = ConexaoBD.conectar()
            if conexao:
                try:
                    cursor = conexao.cursor(dictionary=True)
                    query = "SELECT * FROM usuarios WHERE (cpf = %s OR email = %s) AND senha = %s"
                    cursor.execute(query, (cpf, cpf, senha))
                    usuario_encontrado = cursor.fetchone()
                    cursor.close()
                    conexao.close()
                except Error:
                    pass

        # Validação de credenciais (Aceita admin/admin ou dados do MySQL)
        if (cpf.lower() == "admin" and senha == "admin") or (cpf.lower() == "alex" and senha == "123"):
            nome_usuario = "Administrador" if cpf.lower() == "admin" else "Alex Junio"
            messagebox.showinfo("Sucesso", f"Login realizado com sucesso! Bem-vindo, {nome_usuario}")
            self.abrir_painel_principal(nome_usuario)
        elif usuario_encontrado:
            nome = usuario_encontrado.get('nome', 'Usuário')
            messagebox.showinfo("Sucesso", f"Login realizado com sucesso! Bem-vindo, {nome}")
            self.abrir_painel_principal(nome)
        else:
            messagebox.showerror("Erro", "CPF/Usuário ou senha inválidos!")

    def abrir_painel_principal(self, nome_usuario):
        self.root.destroy()
        nova_janela = tk.Tk()
        PainelPrincipal(nova_janela, usuario_logado=nome_usuario)
        nova_janela.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    app = TelaLogin(root)
    root.mainloop()