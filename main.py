import tkinter as tk
from banco import BancoDeDados
from tela_login import TelaLogin

if __name__ == "__main__":
    # 1. Garante que o banco de dados e todas as tabelas relacionais existam antes de ligar o app
    BancoDeDados.inicializar_banco()

    # 2. Inicializa a janela base do Tkinter
    root = tk.Tk()
    
    # 3. Passa o controle da janela para a classe especializada de Login
    app = TelaLogin(root)
    
    # 4. Mantém o programa rodando
    root.mainloop()
