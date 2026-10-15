import sqlite3


class BancoDeDados:
  DB_NAME = "db_spa_presenca.db"

  @staticmethod
  def conectar():
    """Retorna uma conexão com o SQLite."""
    try:
      conexao = sqlite3.connect(BancoDeDados.DB_NAME)
      conexao.row_factory = sqlite3.Row
      return conexao
    except Exception as e:
      print(f"Erro ao conectar ao SQLite: {e}")
      return None

  @staticmethod
  def inicializar_banco():
    """Cria a tabela de usuários e insere dados padrão se estiver vazia."""
    conexao = BancoDeDados.conectar()
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

        # Insere dados padrão se estiver vazio
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
      """Retorna todos os registros do tipo ALUNO em formato de tupla."""
      conexao = BancoDeDados.conectar()
      resultados = []
      if conexao:
        try:
          cursor = conexao.cursor()
          cursor.execute(
              "SELECT id_usuario, nome, cpf, email FROM usuarios WHERE"
              " tipo_usuario = 'ALUNO'"
          )
          # Converte explicitamente cada linha do Row para tupla padrão do Python
          linhas = cursor.fetchall()
          resultados = [(row[0], row[1], row[2], row[3]) for row in linhas]

          cursor.close()
          conexao.close()
        except Exception as e:
          print(f"Erro ao listar alunos: {e}")
      return resultados

  @staticmethod
  def excluir_usuario(id_usuario):
    """Exclui um usuário pelo ID."""
    conexao = BancoDeDados.conectar()
    if conexao:
      try:
        cursor = conexao.cursor()
        cursor.execute(
            "DELETE FROM usuarios WHERE id_usuario = ?", (id_usuario,)
        )
        conexao.commit()
        cursor.close()
        conexao.close()
        return True
      except Exception as e:
        print(f"Erro ao excluir usuário: {e}")
    return False