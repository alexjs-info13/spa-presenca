from datetime import datetime
from math import radians, sin, cos, sqrt, atan2

class Usuario:
    def __init__(self, id_usuario: int, nome: str, cpf: str, senha: str, data_nascimento: str):
        self.id_usuario = id_usuario
        self.nome = nome
        self.cpf = cpf
        self.senha = senha
        self.data_nascimento = data_nascimento

    def login(self, cpf: str, senha: str) -> bool:
        return self.cpf == cpf and self.senha == senha


class Aluno(Usuario):
    def __init__(self, id_usuario: int, nome: str, cpf: str, senha: str, data_nascimento: str, matricula: str, foto_biometria: str, dados_responsavel: str = None):
        super().__init__(id_usuario, nome, cpf, senha, data_nascimento)
        self.matricula = matricula
        self.foto_biometria = foto_biometria
        self.dados_responsavel = dados_responsavel

    def registrar_presenca(self, chamada, lat_aluno, lon_aluno, foto_atual):
        # Validações das Regras de Negócio (RN02, RN03, RN04)
        if not chamada.validar_tempo():
            return "Erro: Código expirado ou fora da janela de tempo (RN02)."
        if not chamada.validar_geolocalizacao(lat_aluno, lon_aluno):
            return "Erro: Aluno fora do perímetro da sala de aula - Geofence (RN03)."
        
        # Simulação de correspondência biométrica (> 85%)
        similaridade_facial = 0.92 
        if similaridade_facial < 0.85:
            return "Erro: Verificação facial falhou (RN04)."
            
        return RegistroPresenca(chamada, self, datetime.now(), "Sucesso", "Sucesso")


class Professor(Usuario):
    def __init__(self, id_usuario: int, nome: str, cpf: str, senha: str, data_nascimento: str, departamento: str):
        super().__init__(id_usuario, nome, cpf, senha, data_nascimento)
        self.departamento = departamento

    def abrir_chamada(self, id_chamada: int, tempo_limite: int, geofence_coord: tuple):
        codigo = "XYZ123"
        return Chamada(id_chamada, self, datetime.now(), tempo_limite, codigo, geofence_coord)


class Chamada:
    def __init__(self, id_chamada: int, professor: Professor, data_hora_inicio: datetime, tempo_limite: int, codigo_acesso: str, geofence_coord: tuple):
        self.id_chamada = id_chamada
        self.professor = professor
        self.data_hora_inicio = data_hora_inicio
        self.tempo_limite = tempo_limite
        self.codigo_acesso = codigo_acesso
        self.geofence_coord = geofence_coord

    def validar_tempo(self) -> bool:
        tempo_decorrido = (datetime.now() - self.data_hora_inicio).total_seconds() / 60
        return tempo_decorrido <= self.tempo_limite

    def validar_geolocalizacao(self, lat_aluno: float, lon_aluno: float) -> bool:
        R = 6371000 # Raio da Terra em metros
        lat1, lon1, lat2, lon2 = map(radians, [self.geofence_coord[0], self.geofence_coord[1], lat_aluno, lon_aluno])
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        distancia = R * c
        return distancia <= 20.0 # Raio tolerado de 20 metros


class RegistroPresenca:
    def __init__(self, chamada: Chamada, aluno: Aluno, data_hora: datetime, status_biometria: str, status_gps: str):
        self.id_registro = f"{chamada.id_chamada}-{aluno.matricula}"
        self.chamada = chamada
        self.aluno = aluno
        self.data_hora = data_hora
        self.status_biometria = status_biometria
        self.status_gps = status_gps


# --- Bloco de Teste Prático ---
if __name__ == "__main__":
    prof = Professor(1, "Carlos Silva", "11122233344", "senha123", "1980-05-10", "Tecnologia")
    aluno = Aluno(2, "Mariana Souza", "22233344455", "senha456", "2005-08-15", "2026001", "foto_hash.jpg")
    
    coordenada_sala = (-19.9167, -43.9345)
    chamada_atual = prof.abrir_chamada(id_chamada=101, tempo_limite=10, geofence_coord=coordenada_sala)
    
    print(f"Chamada aberta com o código: {chamada_atual.codigo_acesso}")
    
    resultado = aluno.registrar_presenca(
        chamada=chamada_atual, 
        lat_aluno=-19.916701, 
        lon_aluno=-43.934502, 
        foto_atual="foto_atual.jpg"
    )
    
    if isinstance(resultado, RegistroPresenca):
        print(f"Presença confirmada para {resultado.aluno.nome} às {resultado.data_hora.strftime('%H:%M:%S')}!")
    else:
        print(resultado)