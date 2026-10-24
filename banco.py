import sqlite3
from datetime import datetime, timedelta

class BancoDeDados:
    DB_NAME = "db_spa_presenca.db"

    @staticmethod
    def conectar():
        """Retorna uma conexão com o SQLite configurada para Row Factory."""
        try:
            conexao = sqlite3.connect(BancoDeDados.DB_NAME)
            conexao.row_factory = sqlite3.Row
            # Ativa suporte a chaves estrangeiras no SQLite
            conexao.execute("PRAGMA foreign_keys = ON;")
            return conexao
        except Exception as e:
            print(f"Erro ao conectar ao SQLite: {e}")
            return None

    @staticmethod
    def inicializar_banco():
        """Cria todas as tabelas do ecossistema SPA baseadas no modelo relacional."""
        conexao = BancoDeDados.conectar()
        if conexao:
            try:
                cursor = conexao.cursor()
                
                # 1. TABELA DE USUÁRIOS
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS usuarios (
                        id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
                        nome TEXT NOT NULL,
                        cpf TEXT NOT NULL UNIQUE,
                        email TEXT NOT NULL UNIQUE,
                        senha TEXT NOT NULL,
                        tipo_usuario TEXT CHECK(tipo_usuario IN ('ALUNO', 'PROFESSOR', 'ADMIN')) NOT NULL,
                        data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)

                # 2. TABELA DE TURMAS
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS turmas (
                        id_turma INTEGER PRIMARY KEY AUTOINCREMENT,
                        nome_turma TEXT NOT NULL UNIQUE
                    )
                """)

                # 3. TABELA DE ASSOCIAÇÃO: ALUNOS E TURMAS
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS alunos_turmas (
                        id_aluno INTEGER NOT NULL,
                        id_turma INTEGER NOT NULL,
                        PRIMARY KEY (id_aluno, id_turma),
                        FOREIGN KEY (id_aluno) REFERENCES usuarios(id_usuario) ON DELETE CASCADE,
                        FOREIGN KEY (id_turma) REFERENCES turmas(id_turma) ON DELETE CASCADE
                    )
                """)

                # 4. TABELA DE DISCIPLINAS
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS disciplinas (
                        id_disciplina INTEGER PRIMARY KEY AUTOINCREMENT,
                        nome_disciplina TEXT NOT NULL UNIQUE,
                        carga_horaria INTEGER NOT NULL
                    )
                """)

                # 5. TABELA DE CHAMADAS
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS chamadas (
                        id_chamada INTEGER PRIMARY KEY AUTOINCREMENT,
                        id_professor INTEGER NOT NULL,
                        id_disciplina INTEGER NOT NULL,
                        id_turma INTEGER NOT NULL,
                        codigo_verificacao TEXT NOT NULL,
                        data_hora_inicio TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        status_chamada TEXT DEFAULT 'ABERTA' CHECK(status_chamada IN ('ABERTA', 'ENCERRADA')),
                        FOREIGN KEY (id_professor) REFERENCES usuarios(id_usuario),
                        FOREIGN KEY (id_disciplina) REFERENCES disciplinas(id_disciplina),
                        FOREIGN KEY (id_turma) REFERENCES turmas(id_turma)
                    )
                """)

                # 6. TABELA DE REGISTROS DE PRESENÇA
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS registros_presenca (
                        id_registro INTEGER PRIMARY KEY AUTOINCREMENT,
                        id_chamada INTEGER NOT NULL,
                        id_aluno INTEGER NOT NULL,
                        codigo_validado TEXT NOT NULL,
                        status_presenca TEXT NOT NULL CHECK(status_presenca IN ('PRESENTE', 'AUSENTE', 'JUSTIFICADO')),
                        data_hora_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (id_chamada) REFERENCES chamadas(id_chamada) ON DELETE CASCADE,
                        FOREIGN KEY (id_aluno) REFERENCES usuarios(id_usuario) ON DELETE CASCADE,
                        CONSTRAINT uc_aluno_chamada UNIQUE (id_aluno, id_chamada)
                    )
                """)

                # --- POPULAR DADOS INICIAIS CASO O BANCO ESTEJA VAZIO ---
                cursor.execute("SELECT COUNT(*) FROM usuarios")
                if cursor.fetchone()[0] == 0:
                    # Inserindo Turmas
                    cursor.executemany("INSERT OR IGNORE INTO turmas (nome_turma) VALUES (?)", 
                                     [("Técnico em TI - Módulo 1",), ("Técnico em TI - Módulo 2",)])
                    
                    # Inserindo Disciplinas
                    cursor.executemany("INSERT OR IGNORE INTO disciplinas (nome_disciplina, carga_horaria) VALUES (?, ?)", 
                                     [("Banco de Dados", 80), ("Programação em Python", 80), ("Análise de Sistemas", 60)])

                    # Inserindo Alunos e Professores padrão
                    usuarios_iniciais = [
                        ("Emilly Alcântara", "111.222.333-44", "emilly@grautecnico.com", "123", "ALUNO"),
                        ("Alex Junio", "555.666.777-88", "alex@grautecnico.com", "123", "ALUNO"),
                        ("João Silva", "999.888.777-66", "joao@grautecnico.com", "123", "ALUNO"),
                        ("Professor Mestre", "000.111.222-33", "professor@grautecnico.com", "123", "PROFESSOR"),
                    ]
                    cursor.executemany(
                        "INSERT OR IGNORE INTO usuarios (nome, cpf, email, senha, tipo_usuario) VALUES (?, ?, ?, ?, ?)",
                        usuarios_iniciais
                    )
                    conexao.commit()
                    
                    # Vinculando alunos às turmas (Exemplo: todos no Módulo 2)
                    cursor.execute("SELECT id_usuario FROM usuarios WHERE tipo_usuario = 'ALUNO'")
                    id_alunos = [row['id_usuario'] for row in cursor.fetchall()]
                    cursor.execute("SELECT id_turma FROM turmas WHERE nome_turma = 'Técnico em TI - Módulo 2'")
                    id_turma_m2 = cursor.fetchone()['id_turma']
                    
                    for id_aluno in id_alunos:
                        cursor.execute("INSERT OR IGNORE INTO alunos_turmas (id_aluno, id_turma) VALUES (?, ?)", (id_aluno, id_turma_m2))
                    
                    conexao.commit()

                cursor.close()
                conexao.close()
            except Exception as e:
                print(f"Erro ao inicializar base de dados SQLite: {e}")

    @staticmethod
    def validar_login(cpf_ou_email, senha):
        """Consulta o banco para autenticar o usuário."""
        conexao = BancoDeDados.conectar()
        if conexao:
            try:
                cursor = conexao.cursor()
                query = "SELECT * FROM usuarios WHERE (cpf = ? OR email = ?) AND senha = ?"
                cursor.execute(query, (cpf_ou_email, cpf_ou_email, senha))
                usuario = cursor.fetchone()
                cursor.close()
                conexao.close()
                return usuario
            except Exception as e:
                print(f"Erro ao validar login: {e}")
        return None

    @staticmethod
    def cadastrar_usuario(nome, cpf, email, senha, tipo_usuario):
        """Insere um novo usuário/aluno no banco."""
        conexao = BancoDeDados.conectar()
        if conexao:
            try:
                cursor = conexao.cursor()
                cursor.execute(
                    """
                    INSERT INTO usuarios (nome, cpf, email, senha, tipo_usuario)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (nome, cpf, email, senha, tipo_usuario),
                )
                id_novo_usuario = cursor.lastrowid
                
                # Se for aluno, vincula automaticamente à turma padrão do Módulo 2 para testes no painel
                if tipo_usuario == "ALUNO":
                    cursor.execute("SELECT id_turma FROM turmas WHERE nome_turma = 'Técnico em TI - Módulo 2'")
                    turma_row = cursor.fetchone()
                    if turma_row:
                        cursor.execute(
                            "INSERT INTO alunos_turmas (id_aluno, id_turma) VALUES (?, ?)",
                            (id_novo_usuario, turma_row['id_turma'])
                        )
                
                conexao.commit()
                cursor.close()
                conexao.close()
                return True
            except sqlite3.IntegrityError:
                return "duplicado"
            except Exception as e:
                print(f"Erro ao cadastrar usuário: {e}")
                return False
        return False

    @staticmethod
    def listar_alunos():
        """Retorna todos os registros do tipo ALUNO em formato de tupla para a Treeview."""
        conexao = BancoDeDados.conectar()
        resultados = []
        if conexao:
            try:
                cursor = conexao.cursor()
                cursor.execute(
                    "SELECT id_usuario, nome, cpf, email FROM usuarios WHERE tipo_usuario = 'ALUNO'"
                )
                linhas = cursor.fetchall()
                
                # CORREÇÃO AQUI: Mapeia corretamente cada coluna por sua chave/índice
                resultados = [(row['id_usuario'], row['nome'], row['cpf'], row['email']) for row in linhas]
                
                cursor.close()
                conexao.close()
            except Exception as e:
                print(f"Erro ao listar alunos: {e}")
        return resultados

    @staticmethod
    def excluir_usuario(id_usuario):
        """Exclui um usuário limpando primeiro as restrições relacionais."""
        conexao = BancoDeDados.conectar()
        if conexao:
            try:
                cursor = conexao.cursor()
                
                # 1. Remove primeiro o vínculo do aluno com a turma para liberar a chave estrangeira
                cursor.execute("DELETE FROM alunos_turmas WHERE id_aluno = ?", (int(id_usuario),))
                
                # 2. Agora o banco aceita apagar o registro do usuário na tabela principal sem travar
                cursor.execute("DELETE FROM usuarios WHERE id_usuario = ?", (int(id_usuario),))
                
                conexao.commit()
                cursor.close()
                conexao.close()
                return True
            except Exception as e:
                print(f"Erro ao excluir usuário no banco: {e}")
                return False
        return False
