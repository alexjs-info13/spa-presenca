class Usuario:

  def __init__(self, id_usuario, nome, cpf, email, tipo_usuario):
    self.id_usuario = id_usuario
    self.nome = nome
    self.cpf = cpf
    self.email = email
    self.tipo_usuario = tipo_usuario

  def __str__(self):
    return (
        f"Usuário: {self.nome} ({self.tipo_usuario}) - CPF: {self.cpf}"
    )