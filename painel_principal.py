import csv
import os
import sqlite3
import tkinter as tk
from tkinter import filedialog, messagebox, ttk


class PainelPrincipal:

  def __init__(self, master, usuario_logado="Administrador"):
    self.master = master
    self.master.title(
        "Sistema de Presença Acadêmica (SPA) - Painel Principal"
    )
    self.master.geometry("900x630")
    self.master.config(bg="#f4f6f9")

    self.usuario_logado = usuario_logado

    # Garante que a base de dados e a tabela de alunos existem no SQLite local
    self.inicializar_banco()

    # --- CARREGAMENTO DA LOGO COM CAMINHO SEGURO ---
    self.logo_mini = None
    try:
      diretorio_atual = os.path.dirname(os.path.abspath(__file__))
      caminho_logo = os.path.join(diretorio_atual, "Imagens", "Logo_SPA.png")
      if os.path.exists(caminho_logo):
        self.logo_img = tk.PhotoImage(file=caminho_logo)
        self.logo_mini = self.logo_img.subsample(5, 5)
    except Exception as e:
      print(f"Aviso ao carregar logo: {e}")

    self.criar_cabecalho()
    self.criar_conteudo()

  def conectar_bd(self):
    """Retorna uma conexão ativa com a base de dados SQLite local"""
    try:
      conexao = sqlite3.connect("db_spa_presenca.db")
      return conexao
    except Exception as e:
      print(f"Erro ao conectar ao SQLite: {e}")
      return None

  def inicializar_banco(self):
    """Cria a tabela de utilizadores no SQLite e insere dados iniciais se estiver vazia"""
    conexao = self.conectar_bd()
    if conexao:
      try:
        cursor = conexao.cursor()
        cursor.execute("""
                    CREATE TABLE IF NOT EXISTS usuarios (
                        id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
                        nome TEXT NOT NULL,
                        cpf TEXT NOT NULL UNIQUE,
                        email TEXT NOT NULL UNIQUE,
                        senha TEXT NOT NULL,
                        tipo_usuario TEXT NOT NULL
                    )
                """)
        # Verifica se há registos para inserir os alunos padrão iniciais
        cursor.execute("SELECT COUNT(*) FROM usuarios")
        if cursor.fetchone()[0] == 0:
          alunos_iniciais = [
              (
                  "Emilly Alcântara",
                  "111.222.333-44",
                  "emilly@grautecnico.com",
                  "123",
                  "ALUNO",
              ),
              (
                  "Alex Junio",
                  "555.666.777-88",
                  "alex@grautecnico.com",
                  "123",
                  "ALUNO",
              ),
              (
                  "João Silva",
                  "999.888.777-66",
                  "joao@grautecnico.com",
                  "123",
                  "ALUNO",
              ),
          ]
          cursor.executemany(
              """
                        INSERT OR IGNORE INTO usuarios (nome, cpf, email, senha, tipo_usuario)
                        VALUES (?, ?, ?, ?, ?)
                    """,
              alunos_iniciais,
          )
          conexao.commit()
        cursor.close()
        conexao.close()
      except Exception as e:
        print(f"Erro ao inicializar base de dados SQLite: {e}")

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
        fg="white",
    )
    titulo_app.pack(side=tk.LEFT, pady=20)

    lbl_usuario = tk.Label(
        header_frame,
        text=f"Usuário: {self.usuario_logado}",
        font=("Arial", 11),
        bg="#1e293b",
        fg="#94a3b8",
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

    # Aba 4: Relatórios
    self.aba_relatorios = ttk.Frame(self.notebook)
    self.notebook.add(self.aba_relatorios, text=" Relatórios ")
    self.montar_aba_relatorios()

  def montar_aba_inicio(self):
    lbl_bem_vindo = tk.Label(
        self.aba_inicio,
        text=f"Bem-vindo ao Painel de Controle, {self.usuario_logado}!",
        font=("Arial", 14, "bold"),
        bg="#f4f6f9",
        fg="#334155",
    )
    lbl_bem_vindo.pack(pady=30, padx=20, anchor="w")

    card_frame = tk.Frame(self.aba_inicio, bg="#f4f6f9")
    card_frame.pack(fill=tk.X, padx=20)

    self.criar_card(card_frame, "Turmas Ativas", "6", "#3b82f6")
    self.criar_card(card_frame, "Alunos Matriculados", "142", "#10b981")
    self.criar_card(card_frame, "Chamadas Hoje", "3", "#f59e0b")

  def criar_card(self, parent, titulo, valor, cor):
    card = tk.Frame(
        parent, bg="white", bd=1, relief=tk.SOLID, width=200, height=100
    )
    card.pack(side=tk.LEFT, padx=10, ipadx=20, ipady=10)
    card.pack_propagate(False)

    lbl_tit = tk.Label(
        card,
        text=titulo,
        font=("Arial", 10, "bold"),
        bg="white",
        fg="#64748b",
    )
    lbl_tit.pack(anchor="w", pady=5)

    lbl_val = tk.Label(
        card, text=valor, font=("Arial", 22, "bold"), bg="white", fg=cor
    )
    lbl_val.pack(anchor="w")

  def montar_aba_chamada(self):
    lbl_titulo = tk.Label(
        self.aba_chamada,
        text="Painel de Controle de Chamadas",
        font=("Arial", 14, "bold"),
        bg="#f4f6f9",
        fg="#1e293b",
    )
    lbl_titulo.pack(pady=15, padx=20, anchor="w")

    frame_form = tk.LabelFrame(
        self.aba_chamada,
        text=" Abrir Nova Chamada de Aula ",
        font=("Arial", 10, "bold"),
        bg="#f4f6f9",
        fg="#2563eb",
        padx=15,
        pady=15,
    )
    frame_form.pack(padx=20, pady=10, fill=tk.X)

    lbl_turma = tk.Label(
        frame_form, text="Turma:", font=("Arial", 9, "bold"), bg="#f4f6f9"
    )
    lbl_turma.grid(row=0, column=0, sticky="w", pady=5)

    self.combo_turma = ttk.Combobox(
        frame_form,
        values=[
            "Técnico em TI - Módulo 2",
            "Técnico em TI - Módulo 1",
        ],
        width=35,
        state="readonly",
    )
    self.combo_turma.grid(row=0, column=1, sticky="w", pady=5, padx=10)
    self.combo_turma.current(0)

    lbl_disc = tk.Label(
        frame_form, text="Disciplina:", font=("Arial", 9, "bold"), bg="#f4f6f9"
    )
    lbl_disc.grid(row=1, column=0, sticky="w", pady=5)

    self.combo_disc = ttk.Combobox(
        frame_form,
        values=[
            "Banco de Dados",
            "Programação em Python",
            "Análise de Sistemas",
        ],
        width=35,
        state="readonly",
    )
    self.combo_disc.grid(row=1, column=1, sticky="w", pady=5, padx=10)
    self.combo_disc.current(0)

    lbl_codigo = tk.Label(
        frame_form,
        text="Código (6 dígitos):",
        font=("Arial", 9, "bold"),
        bg="#f4f6f9",
    )
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
        command=self.acao_abrir_chamada,
    )
    btn_iniciar.grid(row=3, column=1, sticky="w", pady=15, padx=10)

    self.lbl_status_chamada = tk.Label(
        self.aba_chamada,
        text="Status: Nenhuma chamada ativa no momento.",
        font=("Arial", 10, "italic"),
        bg="#f4f6f9",
        fg="#64748b",
    )
    self.lbl_status_chamada.pack(padx=20, pady=15, anchor="w")

  def acao_abrir_chamada(self):
    turma = self.combo_turma.get()
    disciplina = self.combo_disc.get()
    codigo = self.entry_codigo.get()

    if not codigo:
      messagebox.showwarning("Aviso", "Insira um código de verificação!")
      return

    self.tempo_restante = 300
    self.atualizar_contador(turma, disciplina, codigo)

  def atualizar_contador(self, turma, disciplina, codigo):
    if self.tempo_restante > 0:
      minutos = self.tempo_restante // 60
      segundos = self.tempo_restante % 60
      tempo_formatado = f"{minutos:02d}:{segundos:02d}"

      msg = (
          f"🟢 Chamada ABERTA!\nTurma: {turma} | Disciplina:"
          f" {disciplina}\nCódigo: {codigo}\n⏱️ Tempo restante para check-in:"
          f" {tempo_formatado}"
      )
      self.lbl_status_chamada.config(
          text=msg, fg="#16a34a", font=("Arial", 10, "bold")
      )

      self.tempo_restante -= 1
      self.master.after(
          1000, lambda: self.atualizar_contador(turma, disciplina, codigo)
      )
    else:
      msg = (
          f"🔴 Chamada ENCERRADA!\nO prazo de 5 minutos para a turma {turma}"
          " expirou."
      )
      self.lbl_status_chamada.config(
          text=msg, fg="#dc2626", font=("Arial", 10, "bold")
      )

  def montar_aba_alunos(self):
    topo_frame = tk.Frame(self.aba_alunos, bg="#f4f6f9")
    topo_frame.pack(fill=tk.X, padx=20, pady=10)

    lbl = tk.Label(
        topo_frame,
        text="Gerenciamento de Alunos",
        font=("Arial", 12, "bold"),
        bg="#f4f6f9",
        fg="#1e293b",
    )
    lbl.pack(side=tk.LEFT)

    lbl_busca = tk.Label(
        topo_frame, text="🔍 Buscar:", font=("Arial", 9, "bold"), bg="#f4f6f9"
    )
    lbl_busca.pack(side=tk.LEFT, padx=(20, 5))

    self.entry_busca = tk.Entry(topo_frame, font=("Arial", 9), width=20)
    self.entry_busca.pack(side=tk.LEFT, padx=5)
    self.entry_busca.bind("<KeyRelease>", self.filtrar_alunos)

    columns = ("ID", "Nome", "CPF", "E-mail")
    self.tree = ttk.Treeview(
        self.aba_alunos, columns=columns, show="headings", height=6
    )

    for col in columns:
      self.tree.heading(col, text=col)
      self.tree.column(col, width=175)

    self.tree.pack(padx=20, pady=2, fill=tk.BOTH, expand=False)

    btn_excluir = tk.Button(
        self.aba_alunos,
        text="🗑️ Excluir Aluno Selecionado",
        bg="#dc2626",
        fg="white",
        font=("Arial", 9, "bold"),
        command=self.excluir_aluno,
    )
    btn_excluir.pack(anchor="w", padx=20, pady=5)

    frame_cad = tk.LabelFrame(
        self.aba_alunos,
        text=" Cadastrar Novo Aluno ",
        font=("Arial", 10, "bold"),
        bg="#f4f6f9",
        fg="#2563eb",
        padx=12,
        pady=6,
    )
    frame_cad.pack(padx=20, pady=5, fill=tk.X)

    tk.Label(
        frame_cad, text="Nome:", font=("Arial", 9, "bold"), bg="#f4f6f9"
    ).grid(row=0, column=0, sticky="w", pady=2)
    self.entry_nome_aluno = tk.Entry(frame_cad, font=("Arial", 9), width=28)
    self.entry_nome_aluno.grid(row=0, column=1, sticky="w", pady=2, padx=5)

    tk.Label(frame_cad, text="CPF:", font=("Arial", 9, "bold"), bg="#f4f6f9").grid(
        row=1, column=0, sticky="w", pady=2
    )
    self.entry_cpf_aluno = tk.Entry(frame_cad, font=("Arial", 9), width=18)
    self.entry_cpf_aluno.grid(row=1, column=1, sticky="w", pady=2, padx=5)

    tk.Label(
        frame_cad, text="E-mail:", font=("Arial", 9, "bold"), bg="#f4f6f9"
    ).grid(row=2, column=0, sticky="w", pady=2)
    self.entry_email_aluno = tk.Entry(frame_cad, font=("Arial", 9), width=28)
    self.entry_email_aluno.grid(row=2, column=1, sticky="w", pady=2, padx=5)

    btn_salvar = tk.Button(
        frame_cad,
        text="💾 Salvar Aluno",
        bg="#2563eb",
        fg="white",
        font=("Arial", 9, "bold"),
        padx=8,
        command=self.salvar_novo_aluno,
    )
    btn_salvar.grid(row=3, column=1, sticky="w", pady=6, padx=5)

    self.carregar_alunos_bd()

  def carregar_alunos_bd(self):
    """Carrega os alunos diretamente do SQLite de forma permanente"""
    for item in self.tree.get_children():
      self.tree.delete(item)

    conexao = self.conectar_bd()
    if conexao:
      try:
        cursor = conexao.cursor()
        cursor.execute(
            "SELECT id_usuario, nome, cpf, email FROM usuarios WHERE"
            " tipo_usuario = 'ALUNO'"
        )
        resultados = cursor.fetchall()
        for row in resultados:
          self.tree.insert("", tk.END, values=row)
        cursor.close()
        conexao.close()
      except Exception as e:
        print(f"Erro ao carregar alunos do SQLite: {e}")

  def filtrar_alunos(self, event=None):
    """Filtra os alunos exibidos na Treeview com base na pesquisa"""
    termo = self.entry_busca.get().lower()
    for item in self.tree.get_children():
      self.tree.delete(item)

    conexao = self.conectar_bd()
    if conexao:
      try:
        cursor = conexao.cursor()
        cursor.execute(
            "SELECT id_usuario, nome, cpf, email FROM usuarios WHERE"
            " tipo_usuario = 'ALUNO'"
        )
        resultados = cursor.fetchall()
        for row in resultados:
          # row = (id, nome, cpf, email)
          if (
              termo in str(row[1]).lower()
              or termo in str(row[2]).lower()
              or termo in str(row[3]).lower()
          ):
            self.tree.insert("", tk.END, values=row)
        cursor.close()
        conexao.close()
      except Exception as e:
        print(f"Erro ao filtrar alunos: {e}")

  def excluir_aluno(self):
    """Exclui o aluno selecionado permanentemente da base de dados SQLite"""
    selecionado = self.tree.selection()
    if not selecionado:
      messagebox.showwarning(
          "Aviso", "Selecione um aluno na tabela para excluir!"
      )
      return

    item_id = selecionado[0]
    valores = self.tree.item(item_id, "values")
    id_aluno = valores[0]
    nome_aluno = valores[1]

    if messagebox.askyesno(
        "Confirmar Exclusão", f"Deseja realmente excluir o aluno {nome_aluno}?"
    ):
      conexao = self.conectar_bd()
      if conexao:
        try:
          cursor = conexao.cursor()
          cursor.execute("DELETE FROM usuarios WHERE id_usuario = ?", (id_aluno,))
          conexao.commit()
          cursor.close()
          conexao.close()
          self.carregar_alunos_bd()
          messagebox.showinfo(
              "Sucesso", "Aluno excluído com sucesso do banco local!"
          )
        except Exception as e:
          messagebox.showerror("Erro", f"Erro ao excluir aluno: {e}")

  def salvar_novo_aluno(self):
    """Guarda um novo aluno permanentemente no SQLite"""
    nome = self.entry_nome_aluno.get().strip()
    cpf = self.entry_cpf_aluno.get().strip()
    email = self.entry_email_aluno.get().strip()

    if not nome or not cpf or not email:
      messagebox.showwarning(
          "Aviso", "Por favor, preencha todos os campos do aluno!"
      )
      return

    conexao = self.conectar_bd()
    if conexao:
      try:
        cursor = conexao.cursor()
        cursor.execute(
            """
                    INSERT INTO usuarios (nome, cpf, email, senha, tipo_usuario)
                    VALUES (?, ?, ?, '123', 'ALUNO')
                """,
            (nome, cpf, email),
        )
        conexao.commit()
        cursor.close()
        conexao.close()

        # Limpa os campos do formulário
        self.entry_nome_aluno.delete(0, tk.END)
        self.entry_cpf_aluno.delete(0, tk.END)
        self.entry_email_aluno.delete(0, tk.END)

        self.carregar_alunos_bd()
        messagebox.showinfo(
            "Sucesso", f"Aluno {nome} cadastrado e gravado no SQLite!"
        )
      except sqlite3.IntegrityError:
        messagebox.showerror(
            "Erro", "CPF ou E-mail já cadastrados no sistema!"
        )
      except Exception as e:
        messagebox.showerror("Erro", f"Erro ao salvar aluno: {e}")

  def montar_aba_relatorios(self):
    """Monta a interface da Aba de Relatórios de Frequência"""
    frame_conteudo = ttk.Frame(self.aba_relatorios, padding=15)
    frame_conteudo.pack(fill="both", expand=True)

    # 1. Painel de Filtros
    frame_filtros = ttk.LabelFrame(
        frame_conteudo, text=" Filtros de Consulta ", padding=10
    )
    frame_filtros.pack(fill="x", pady=(0, 10))

    ttk.Label(frame_filtros, text="Turma:").grid(
        row=0, column=0, padx=5, pady=5, sticky="w"
    )
    self.combo_rel_turma = ttk.Combobox(
        frame_filtros,
        values=[
            "Todas",
            "Técnico em TI - Módulo 2",
            "Técnico em TI - Módulo 1",
        ],
        state="readonly",
        width=25,
    )
    self.combo_rel_turma.current(0)
    self.combo_rel_turma.grid(row=0, column=1, padx=5, pady=5)

    ttk.Label(frame_filtros, text="Status:").grid(
        row=0, column=2, padx=5, pady=5, sticky="w"
    )
    self.combo_rel_status = ttk.Combobox(
        frame_filtros,
        values=["Todos", "Presente", "Ausente"],
        state="readonly",
        width=15,
    )
    self.combo_rel_status.current(0)
    self.combo_rel_status.grid(row=0, column=3, padx=5, pady=5)

    btn_filtrar = ttk.Button(
        frame_filtros,
        text="🔍 Gerar Relatório",
        command=self.carregar_dados_relatorio,
    )
    btn_filtrar.grid(row=0, column=4, padx=15, pady=5)

    # 2. Tabela (Treeview) de Relatórios
    frame_tabela = ttk.Frame(frame_conteudo)
    frame_tabela.pack(fill="both", expand=True)

    colunas = (
        "id",
        "aluno",
        "cpf",
        "turma",
        "data_hora",
        "status_gps",
        "status_bio",
        "presenca",
    )
    self.tree_rel = ttk.Treeview(
        frame_tabela, columns=colunas, show="headings", height=10
    )

    self.tree_rel.heading("id", text="ID")
    self.tree_rel.heading("aluno", text="Nome do Aluno")
    self.tree_rel.heading("cpf", text="CPF")
    self.tree_rel.heading("turma", text="Turma")
    self.tree_rel.heading("data_hora", text="Data/Hora")
    self.tree_rel.heading("status_gps", text="GPS (Geofence)")
    self.tree_rel.heading("status_bio", text="Biometria")
    self.tree_rel.heading("presenca", text="Status")

    self.tree_rel.column("id", width=40, anchor="center")
    self.tree_rel.column("aluno", width=160, anchor="w")
    self.tree_rel.column("cpf", width=110, anchor="center")
    self.tree_rel.column("turma", width=150, anchor="w")
    self.tree_rel.column("data_hora", width=120, anchor="center")
    self.tree_rel.column("status_gps", width=100, anchor="center")
    self.tree_rel.column("status_bio", width=90, anchor="center")
    self.tree_rel.column("presenca", width=80, anchor="center")

    scrollbar = ttk.Scrollbar(
        frame_tabela, orient="vertical", command=self.tree_rel.yview
    )
    self.tree_rel.configure(yscrollcommand=scrollbar.set)

    self.tree_rel.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # 3. Rodapé com Ações e Resumo
    frame_rodape = ttk.Frame(frame_conteudo)
    frame_rodape.pack(fill="x", pady=(10, 0))

    self.lbl_total_rel = ttk.Label(
        frame_rodape, text="Total de Registros: 0", font=("Arial", 9, "bold")
    )
    self.lbl_total_rel.pack(side="left", padx=5)

    btn_exportar = ttk.Button(
        frame_rodape,
        text="📄 Exportar Relatório (CSV)",
        command=self.exportar_relatorio_csv,
    )
    btn_exportar.pack(side="right", padx=5)

    # Carrega os dados iniciais na tabela de relatórios
    self.carregar_dados_relatorio()

  def carregar_dados_relatorio(self):
    """Carrega dados simulados ou do banco de dados na tabela de relatórios"""
    for item in self.tree_rel.get_children():
      self.tree_rel.delete(item)

    dados_demo = [
        (
            "1",
            "Alex Junio",
            "555.666.777-88",
            "Técnico em TI - Módulo 2",
            "13/10/2026 19:00",
            "Validado (12m)",
            "Aprovado (92%)",
            "Presente",
        ),
        (
            "2",
            "Emilly Alcântara",
            "111.222.333-44",
            "Técnico em TI - Módulo 2",
            "13/10/2026 19:02",
            "Validado (8m)",
            "Aprovado (89%)",
            "Presente",
        ),
        (
            "3",
            "João Silva",
            "999.888.777-66",
            "Técnico em TI - Módulo 1",
            "13/10/2026 19:15",
            "Fora do Raio (45m)",
            "Pendente",
            "Ausente",
        ),
    ]

    for linha in dados_demo:
      self.tree_rel.insert("", tk.END, values=linha)

    self.lbl_total_rel.config(
        text=f"Total de Registros Encontrados: {len(dados_demo)}"
    )

  def exportar_relatorio_csv(self):
    """Exporta o conteúdo exibido na tabela de relatórios para um ficheiro CSV"""
    caminho = filedialog.asksaveasfilename(
        defaultextension=".csv",
        filetypes=[("Arquivo CSV", "*.csv"), ("Todos os Ficheiros", "*.*")],
        title="Salvar Relatório de Frequência",
    )
    if not caminho:
      return

    try:
      with open(caminho, mode="w", newline="", encoding="utf-8-sig") as arquivo:
        escritor = csv.writer(arquivo, delimiter=";")
        escritor.writerow([
            "ID",
            "Nome do Aluno",
            "CPF",
            "Turma",
            "Data/Hora",
            "Status GPS",
            "Status Biometria",
            "Status Final",
        ])

        for row_id in self.tree_rel.get_children():
          row = self.tree_rel.item(row_id)["values"]
          escritor.writerow(row)

      messagebox.showinfo(
          "Sucesso", f"Relatório exportado com sucesso!\nSalvo em: {caminho}"
      )
    except Exception as e:
      messagebox.showerror(
          "Erro", f"Não foi possível exportar o relatório: {e}"
      )