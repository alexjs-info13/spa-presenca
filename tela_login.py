import os
import tkinter as tk
from tkinter import messagebox
from banco import BancoDeDados
from painel_principal import PainelPrincipal

class TelaLogin:
    def __init__(self, master):
        self.master = master
        self.master.title("SPA - Sistema de Presença Acadêmica | Login")
        self.master.geometry("400x520") # Aumentado levemente para acomodar os links confortavelmente
        self.master.config(bg="#f0f2f5")
        self.master.resizable(False, False)

        self.centralizar_janela()

        # --- CARREGAMENTO SEGURO DA LOGO ---
        try:
            self.logo_img = tk.PhotoImage(file="Imagens/Logo_SPA.png")
            self.logo_pequena = self.logo_img.subsample(2, 2)
            self.lbl_logo = tk.Label(master, image=self.logo_pequena, bg="#f0f2f5")
            self.lbl_logo.pack(pady=(15, 5))
        except Exception as e:
            print(f"Aviso ao carregar imagem da logo: {e}")
            self.lbl_titulo = tk.Label(
                master, text="🎓 Sistema SPA", font=("Arial", 18, "bold"), bg="#f0f2f5", fg="#1f2937"
            )
            self.lbl_titulo.pack(pady=20)

        self.lbl_sub = tk.Label(
            master, text="Controle de Frequência Escolar", font=("Arial", 10), bg="#f0f2f5", fg="#4b5563"
        )
        self.lbl_sub.pack(pady=(0, 15))

        # --- FRAME DO FORMULÁRIO ---
        form_frame = tk.Frame(master, bg="#ffffff", bd=2, relief="groove")
        form_frame.pack(pady=10, padx=30, fill="both", expand=True)

        # Campo CPF / Usuário
        tk.Label(
            form_frame, text="CPF ou Usuário:", font=("Arial", 10, "bold"), bg="#ffffff", fg="#374151"
        ).pack(anchor="w", padx=20, pady=(15, 5))
        
        self.entry_cpf = tk.Entry(form_frame, font=("Arial", 12), bd=1, relief="solid")
        self.entry_cpf.pack(fill="x", padx=20, pady=(0, 10))

        # Campo Senha
        tk.Label(
            form_frame, text="Senha:", font=("Arial", 10, "bold"), bg="#ffffff", fg="#374151"
        ).pack(anchor="w", padx=20, pady=(5, 5))
        
        self.entry_senha = tk.Entry(form_frame, font=("Arial", 12), show="*", bd=1, relief="solid")
        self.entry_senha.pack(fill="x", padx=20, pady=(0, 15))

        # Botão de Login Azul
        self.btn_login = tk.Button(
            form_frame,
            text="Entrar no Sistema",
            font=("Arial", 11, "bold"),
            bg="#2563eb",
            fg="white",
            bd=0,
            relief="flat",
            cursor="hand2",
            command=self.realizar_login,
        )
        self.btn_login.pack(fill="x", padx=20, pady=(10, 10))

        # --- FRAME PARA LINKS DE CADASTRO E RECUPERAÇÃO ---
        links_frame = tk.Frame(form_frame, bg="#ffffff")
        links_frame.pack(fill="x", padx=20, pady=(5, 10))

        # Link Esqueceu a Senha (Esquerda)
        self.btn_esqueceu = tk.Button(
            links_frame,
            text="Esqueceu a senha?",
            font=("Arial", 9, "underline"),
            bg="#ffffff",
            fg="#2563eb",
            bd=0,
            activebackground="#ffffff",
            activeforeground="#1d4ed8",
            cursor="hand2",
            command=self.acao_esqueceu_senha,
        )
        self.btn_esqueceu.pack(side=tk.LEFT)

        # Link Cadastrar Usuário (Direita)
        self.btn_cadastrar = tk.Button(
            links_frame,
            text="Cadastrar Usuário",
            font=("Arial", 9, "underline"),
            bg="#ffffff",
            fg="#16a34a",
            bd=0,
            activebackground="#ffffff",
            activeforeground="#15803d",
            cursor="hand2",
            command=self.acao_abrir_cadastro,
        )
        self.btn_cadastrar.pack(side=tk.RIGHT)

        # Rodapé Institucional
        lbl_rodape = tk.Label(
            master, text="Grau Técnico • Curso de TI", font=("Arial", 8), bg="#f0f2f5", fg="#9ca3af"
        )
        lbl_rodape.pack(side="bottom", pady=10)

    def centralizar_janela(self):
        self.master.update_idletasks()
        largura = 400
        altura = 520
        x = (self.master.winfo_screenwidth() // 2) - (largura // 2)
        y = (self.master.winfo_screenheight() // 2) - (altura // 2)
        self.master.geometry(f"{largura}x{altura}+{x}+{y}")

    def realizar_login(self):
        cpf = self.entry_cpf.get().strip()
        senha = self.entry_senha.get().strip()

        if not cpf or not senha:
            messagebox.showwarning("Atenção", "Preencha todos os campos (CPF/Usuário e Senha)!")
            return

        # Master Admin para testes rápidos
        if cpf.lower() == "admin" and senha == "admin":
            messagebox.showinfo("Sucesso", "Login realizado com sucesso como Administrador!")
            self.abrir_painel_principal("Administrador", "ADMIN")
            return

        # Validação segura no arquivo banco.py
        usuario = BancoDeDados.validar_login(cpf, senha)
        if usuario:
            messagebox.showinfo("Sucesso", "Login realizado com sucesso!")
            nome = usuario["nome"]
            tipo = str(usuario["tipo_usuario"]).upper()
            self.abrir_painel_principal(nome, tipo)
        else:
            messagebox.showerror("Erro", "Credenciais inválidas ou utilizador não encontrado.")

    def abrir_painel_principal(self, nome_usuario, tipo_usuario):
        self.master.destroy() # Fecha a tela de login com segurança
        nova_janela = tk.Tk()
        PainelPrincipal(nova_janela, usuario_logado=nome_usuario, tipo_usuario=tipo_usuario)
        nova_janela.mainloop()

    def acao_esqueceu_senha(self):
        """Ação disparada ao clicar no link de recuperação."""
        messagebox.showinfo(
            "Recuperação de Senha", 
            "Para recuperar seu acesso, por favor procure a Secretaria do Grau Técnico\n"
            "ou envie um e-mail para: suporte@grautecnico.com"
        )

    def acao_abrir_cadastro(self):
        """Ação disparada ao clicar em 'Cadastrar Usuário'."""
        messagebox.showinfo(
            "Novo Cadastro", 
            "O auto-cadastro de novos alunos está em fase de homologação.\n\n"
            "Por enquanto, realize seu registro na aba 'Alunos' do Painel com um Administrador."
        )
