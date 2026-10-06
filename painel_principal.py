import tkinter as tk
from tkinter import messagebox, ttk

class PainelPrincipal:
    def __init__(self, master, usuario_logado="Administrador"):
        self.master = master
        self.master.title("Sistema de Presença Acadêmica (SPA) - Painel Principal")
        self.master.geometry("900x630")
        self.master.config(bg="#f4f6f9")
        
        self.usuario_logado = usuario_logado

        # --- CARREGAMENTO SEGURO DA LOGO ---
        try:
            import os
            diretorio_atual = os.path.dirname(os.path.abspath(__file__))
            caminho_logo = os.path.join(diretorio_atual, "Imagens", "Logo_SPA.png")
            
            self.logo_img = tk.PhotoImage(file=caminho_logo)
            self.logo_mini = self.logo_img.subsample(5, 5) 
        except Exception as e:
            print(f"Aviso detalhado ao carregar a logo: {e}")
            self.logo_mini = None

        # --- CABEÇALHO ---
        self.criar_cabecalho()

        # --- CORPO / ABAS DE NAVEGAÇÃO ---
        self.criar_conteudo()

    def criar_cabecalho(self):
        header_frame = tk.Frame(self.master, bg="#1e293b", height=80)
        header_frame.pack(side=tk.TOP, fill=tk.X)
        header_frame.pack_propagate(False)

        if self.logo_mini:
            lbl_img = tk.Label(header_frame, image=self.logo_mini, bg="#1e293b")
            lbl_img.pack(side=tk.LEFT, padx=20, pady=10)

        titulo_app = tk.Label(
            header_frame, 
            text="SPA - Sistema de Presença Acadêmica", 
            font=("Arial", 16, "bold"), 
            bg="#1e293b", 
            fg="white"
        )
        titulo_app.pack(side=tk.LEFT, pady=20)

        lbl_usuario = tk.Label(
            header_frame, 
            text=f"Usuário: {self.usuario_logado}", 
            font=("Arial", 11), 
            bg="#1e293b", 
            fg="#94a3b8"
        )
        lbl_usuario.pack(side=tk.RIGHT, padx=20, pady=25)

    def criar_conteudo(self):
        self.notebook = ttk.Notebook(self.master)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

        # Aba 1: Início
        self.aba_inicio = ttk.Frame(self.notebook)
        self.notebook.add(self.aba_inicio, text=" Início ")
        self.montar_aba_inicio()

        # Aba 2: Registrar Chamada
        self.aba_chamada = ttk.Frame(self.notebook)
        self.notebook.add(self.aba_chamada, text=" Registrar Chamada ")
        self.montar_aba_chamada()

        # Aba 3: Alunos
        self.aba_alunos = ttk.Frame(self.notebook)
        self.notebook.add(self.aba_alunos, text=" Alunos ")
        self.montar_aba_alunos()

    def montar_aba_inicio(self):
        lbl_bem_vindo = tk.Label(
            self.aba_inicio, 
            text=f"Bem-vindo ao Painel de Controle, {self.usuario_logado}!", 
            font=("Arial", 14, "bold"), 
            bg="#f4f6f9", 
            fg="#334155"
        )
        lbl_bem_vindo.pack(pady=30, padx=20, anchor="w")

        card_frame = tk.Frame(self.aba_inicio, bg="#f4f6f9")
        card_frame.pack(fill=tk.X, padx=20)

        self.criar_card(card_frame, "Turmas Ativas", "6", "#3b82f6")
        self.criar_card(card_frame, "Alunos Matriculados", "142", "#10b981")
        self.criar_card(card_frame, "Chamadas Hoje", "3", "#f59e0b")

    def criar_card(self, parent, titulo, valor, cor):
        card = tk.Frame(parent, bg="white", bd=1, relief=tk.SOLID, width=200, height=100)
        card.pack(side=tk.LEFT, padx=10, ipadx=20, ipady=10)
        card.pack_propagate(False)

        lbl_tit = tk.Label(card, text=titulo, font=("Arial", 10, "bold"), bg="white", fg="#64748b")
        lbl_tit.pack(anchor="w", pady=5)

        lbl_val = tk.Label(card, text=valor, font=("Arial", 22, "bold"), bg="white", fg=cor)
        lbl_val.pack(anchor="w")

    def montar_aba_chamada(self):
        lbl_titulo = tk.Label(self.aba_chamada, text="Painel de Controle de Chamadas", font=("Arial", 14, "bold"), bg="#f4f6f9", fg="#1e293b")
        lbl_titulo.pack(pady=15, padx=20, anchor="w")

        frame_form = tk.LabelFrame(self.aba_chamada, text=" Abrir Nova Chamada de Aula ", font=("Arial", 10, "bold"), bg="#f4f6f9", fg="#2563eb", padx=15, pady=15)
        frame_form.pack(padx=20, pady=10, fill=tk.X)

        lbl_turma = tk.Label(frame_form, text="Turma:", font=("Arial", 9, "bold"), bg="#f4f6f9")
        lbl_turma.grid(row=0, column=0, sticky="w", pady=5)
        
        self.combo_turma = ttk.Combobox(frame_form, values=["Técnico em TI - Módulo 2", "Técnico em TI - Módulo 1"], width=35, state="readonly")
        self.combo_turma.grid(row=0, column=1, sticky="w", pady=5, padx=10)
        self.combo_turma.current(0)

        lbl_disc = tk.Label(frame_form, text="Disciplina:", font=("Arial", 9, "bold"), bg="#f4f6f9")
        lbl_disc.grid(row=1, column=0, sticky="w", pady=5)
        
        self.combo_disc = ttk.Combobox(frame_form, values=["Banco de Dados", "Programação em Python", "Análise de Sistemas"], width=35, state="readonly")
        self.combo_disc.grid(row=1, column=1, sticky="w", pady=5, padx=10)
        self.combo_disc.current(0)

        lbl_codigo = tk.Label(frame_form, text="Código (6 dígitos):", font=("Arial", 9, "bold"), bg="#f4f6f9")
        lbl_codigo.grid(row=2, column=0, sticky="w", pady=5)
        
        self.entry_codigo = tk.Entry(frame_form, font=("Arial", 10), width=15)
        self.entry_codigo.grid(row=2, column=1, sticky="w", pady=5, padx=10)
        self.entry_codigo.insert(0, "A9B2C4")

        btn_iniciar = tk.Button(
            frame_form, 
            text="🚀 Abrir Chamada para os Alunos", 
            bg="#16a34a", 
            fg="white", 
            font=("Arial", 9, "bold"),
            padx=10,
            pady=5,
            command=self.acao_abrir_chamada
        )
        btn_iniciar.grid(row=3, column=1, sticky="w", pady=15, padx=10)

        self.lbl_status_chamada = tk.Label(self.aba_chamada, text="Status: Nenhuma chamada ativa no momento.", font=("Arial", 10, "italic"), bg="#f4f6f9", fg="#64748b")
        self.lbl_status_chamada.pack(padx=20, pady=15, anchor="w")

    def acao_abrir_chamada(self):
        turma = self.combo_turma.get()
        disciplina = self.combo_disc.get()
        codigo = self.entry_codigo.get()
        
        if not codigo:
            messagebox.showwarning("Aviso", "Insira um código de verificação!")
            return

        # Define o tempo inicial em segundos (5 minutos = 300 segundos)
        self.tempo_restante = 300 
        
        # Inicia a contagem regressiva
        self.atualizar_contador(turma, disciplina, codigo)

    def atualizar_contador(self, turma, disciplina, codigo):
        if self.tempo_restante > 0:
            # Formata os segundos em minutos e segundos (ex: 04:59)
            minutos = self.tempo_restante // 60
            segundos = self.tempo_restante % 60
            tempo_formatado = f"{minutos:02d}:{segundos:02d}"

            msg = (
                f"🟢 Chamada ABERTA!\n"
                f"Turma: {turma} | Disciplina: {disciplina}\n"
                f"Código: {codigo}\n"
                f"⏱️ Tempo restante para check-in: {tempo_formatado}"
            )
            self.lbl_status_chamada.config(text=msg, fg="#16a34a", font=("Arial", 10, "bold"))
            
            # Decrementa 1 segundo e agenda a próxima chamada daqui a 1000 milissegundos (1s)
            self.tempo_restante -= 1
            self.timer_id = self.master.after(1000, lambda: self.atualizar_contador(turma, disciplina, codigo))
        else:
            # Quando o tempo esgota
            msg = f"🔴 Chamada ENCERRADA!\nO prazo de 5 minutos para a turma {turma} expirou."
            self.lbl_status_chamada.config(text=msg, fg="#dc2626", font=("Arial", 10, "bold"))

    def montar_aba_alunos(self):
        # Topo com Título e Barra de Pesquisa
        topo_frame = tk.Frame(self.aba_alunos, bg="#f4f6f9")
        topo_frame.pack(fill=tk.X, padx=20, pady=10)

        lbl = tk.Label(topo_frame, text="Gerenciamento de Alunos", font=("Arial", 12, "bold"), bg="#f4f6f9", fg="#1e293b")
        lbl.pack(side=tk.LEFT)

        lbl_busca = tk.Label(topo_frame, text="🔍 Buscar:", font=("Arial", 9, "bold"), bg="#f4f6f9")
        lbl_busca.pack(side=tk.LEFT, padx=(20, 5))
        
        self.entry_busca = tk.Entry(topo_frame, font=("Arial", 9), width=20)
        self.entry_busca.pack(side=tk.LEFT, padx=5)
        self.entry_busca.bind("<KeyRelease>", self.filtrar_alunos)

        # Tabela (Treeview) para listagem
        columns = ("ID", "Nome", "CPF", "E-mail")
        self.tree = ttk.Treeview(self.aba_alunos, columns=columns, show="headings", height=6)
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=175)

        self.tree.pack(padx=20, pady=2, fill=tk.BOTH, expand=False)

        # Botão de Excluir Aluno Selecionado
        btn_excluir = tk.Button(
            self.aba_alunos, 
            text="🗑️ Excluir Aluno Selecionado", 
            bg="#dc2626", 
            fg="white", 
            font=("Arial", 9, "bold"),
            command=self.excluir_aluno
        )
        btn_excluir.pack(anchor="w", padx=20, pady=5)

        # Formulário de Cadastro de Novo Aluno
        frame_cad = tk.LabelFrame(self.aba_alunos, text=" Cadastrar Novo Aluno ", font=("Arial", 10, "bold"), bg="#f4f6f9", fg="#2563eb", padx=12, pady=6)
        frame_cad.pack(padx=20, pady=5, fill=tk.X)

        tk.Label(frame_cad, text="Nome:", font=("Arial", 9, "bold"), bg="#f4f6f9").grid(row=0, column=0, sticky="w", pady=2)
        self.entry_nome_aluno = tk.Entry(frame_cad, font=("Arial", 9), width=28)
        self.entry_nome_aluno.grid(row=0, column=1, sticky="w", pady=2, padx=5)

        tk.Label(frame_cad, text="CPF:", font=("Arial", 9, "bold"), bg="#f4f6f9").grid(row=1, column=0, sticky="w", pady=2)
        self.entry_cpf_aluno = tk.Entry(frame_cad, font=("Arial", 9), width=18)
        self.entry_cpf_aluno.grid(row=1, column=1, sticky="w", pady=2, padx=5)

        tk.Label(frame_cad, text="E-mail:", font=("Arial", 9, "bold"), bg="#f4f6f9").grid(row=2, column=0, sticky="w", pady=2)
        self.entry_email_aluno = tk.Entry(frame_cad, font=("Arial", 9), width=28)
        self.entry_email_aluno.grid(row=2, column=1, sticky="w", pady=2, padx=5)

        btn_salvar = tk.Button(
            frame_cad, 
            text="💾 Salvar Aluno", 
            bg="#2563eb", 
            fg="white", 
            font=("Arial", 9, "bold"),
            padx=8,
            command=self.salvar_novo_aluno
        )
        btn_salvar.grid(row=3, column=1, sticky="w", pady=6, padx=5)

        self.carregar_alunos_bd()

    def carregar_alunos_bd(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Inicializa a lista de memória padrão se não existir
        if not hasattr(self, "lista_alunos_memoria"):
            self.lista_alunos_memoria = [
                ("1", "Emilly Alcântara", "111.222.333-44", "emilly@grautecnico.com"),
                ("2", "Alex Junio", "555.666.777-88", "alex@grautecnico.com"),
                ("3", "João Silva", "999.888.777-66", "joao@grautecnico.com")
            ]

        sucesso_conexao = False
        try:
            import mysql.connector
            conexao = mysql.connector.connect(
                host="localhost",
                database="db_spa_presenca",
                user="root",
                password=""
            )
            if conexao.is_connected():
                cursor = conexao.cursor()
                query = "SELECT id_usuario, nome, cpf, email FROM usuarios WHERE tipo_usuario = 'ALUNO'"
                cursor.execute(query)
                resultados = cursor.fetchall()
                if resultados:
                    self.lista_alunos_memoria = list(resultados)
                cursor.close()
                conexao.close()
                sucesso_conexao = True
        except Exception as e:
            print(f"Modo demonstração ativo (Banco offline): {e}")

        for row in self.lista_alunos_memoria:
            self.tree.insert("", tk.END, values=row)

    def filtrar_alunos(self, event=None):
        termo = self.entry_busca.get().lower()
        for item in self.tree.get_children():
            self.tree.delete(item)

        if not hasattr(self, "lista_alunos_memoria"):
            return

        for row in self.lista_alunos_memoria:
            if termo in str(row[1]).lower() or termo in str(row[2]).lower() or termo in str(row[3]).lower():
                self.tree.insert("", tk.END, values=row)

    def excluir_aluno(self):
        selecionado = self.tree.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione um aluno na tabela para excluir!")
            return

        item_id = selecionado[0]
        valores = self.tree.item(item_id, "values")
        id_aluno = valores[0]

        if messagebox.askyesno("Confirmar Exclusão", f"Deseja realmente excluir o aluno {valores[1]}?"):
            self.lista_alunos_memoria = [a for a in self.lista_alunos_memoria if str(a[0]) != str(id_aluno)]
            self.carregar_alunos_bd()
            messagebox.showinfo("Sucesso", "Aluno excluído com sucesso!")

    def salvar_novo_aluno(self):
        nome = self.entry_nome_aluno.get()
        cpf = self.entry_cpf_aluno.get()
        email = self.entry_email_aluno.get()

        if not nome or not cpf or not email:
            messagebox.showwarning("Aviso", "Por favor, preencha todos os campos do aluno!")
            return

        # Tenta salvar no banco de dados MySQL de verdade
        salvo_no_banco = False
        try:
            import mysql.connector
            conexao = mysql.connector.connect(
                host="localhost",
                database="db_spa_presenca",
                user="root",
                password=""
            )
            if conexao.is_connected():
                cursor = conexao.cursor()
                # Insere o aluno definindo a senha padrão "123" e o tipo_usuario como 'ALUNO'
                query = "INSERT INTO usuarios (nome, cpf, email, senha, tipo_usuario) VALUES (%s, %s, %s, '123', 'ALUNO')"
                cursor.execute(query, (nome, cpf, email))
                conexao.commit()
                cursor.close()
                conexao.close()
                salvo_no_banco = True
        except Exception as e:
            print(f"Banco offline, salvando apenas em memória temporária: {e}")

        # Atualiza a lista local em memória também para exibição imediata
        novo_id = str(len(self.lista_alunos_memoria) + 1)
        self.lista_alunos_memoria.append((novo_id, nome, cpf, email))
        self.carregar_alunos_bd()

        # Limpa os campos
        self.entry_nome_aluno.delete(0, tk.END)
        self.entry_cpf_aluno.delete(0, tk.END)
        self.entry_email_aluno.delete(0, tk.END)

        if salvo_no_banco:
            messagebox.showinfo("Sucesso", f"Aluno {nome} cadastrado e salvo no Banco de Dados com sucesso!")
        else:
            messagebox.showinfo("Sucesso", f"Aluno {nome} cadastrado com sucesso (Modo Demonstração)!")