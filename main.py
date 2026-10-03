import mysql.connector
from mysql.connector import Error

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
                user="root",        # Altere se o seu usuário do MySQL for diferente
                password=""         # Insira sua senha do MySQL se houver
            )
            if conexao.is_connected():
                print("Conexão bem-sucedida com o Banco de Dados MySQL!")
                return conexao
        except Error as e:
            print(f"Erro ao conectar ao banco de dados: {e}")
            return None

# ==========================================
# ESTRUTURA DE CLASSES (POO)
# ==========================================
class Usuario:
    def __init__(self, id_usuario, nome, cpf, email, tipo_usuario):
        self.id_usuario = id_usuario
        self.nome = nome
        self.cpf = cpf
        self.email = email
        self.tipo_usuario = tipo_usuario

    def exibir_dados(self):
        return f"[{self.tipo_usuario}] {self.nome} (CPF: {self.cpf})"

class Aluno(Usuario):
    def __init__(self, id_usuario, nome, cpf, email, matricula):
        super().__init__(id_usuario, nome, cpf, email, "ALUNO")
        self.matricula = matricula

class Professor(Usuario):
    def __init__(self, id_usuario, nome, cpf, email, departamento):
        super().__init__(id_usuario, nome, cpf, email, "PROFESSOR")
        self.departamento = departamento

# ==========================================
# TESTE INICIAL DO SISTEMA
# ==========================================
if __name__ == "__main__":
    print("--- Inicializando Sistema de Presença Acadêmica (SPA) ---")
    
    # Testando a conexão com o banco
    conexao = ConexaoBD.conectar()
    if conexao:
        conexao.close()
        print("Conexão fechada com segurança.")
        
    # Testando a criação de objetos em POO
    aluno_teste = Aluno(1, "Alex Silva", "123.456.789-00", "alex@email.com", "2026001")
    print(aluno_teste.exibir_dados())