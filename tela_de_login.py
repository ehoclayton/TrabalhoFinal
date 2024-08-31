import tkinter as tk
from tkinter import messagebox
import mysql.connector
import bcrypt
import json

def carregar_configuracoes():
    """Carrega configurações do banco de dados a partir de um arquivo JSON."""
    with open('config.json', 'r') as f:
        return json.load(f)

def conectar():
    """Cria e retorna uma conexão com o banco de dados."""
    config = carregar_configuracoes()
    try:
        conexao = mysql.connector.connect(
            host=config['host'],
            user=config['user'],
            password=config['password'],
            database=config['database']
        )
        return conexao
    except mysql.connector.Error as err:
        messagebox.showerror("Erro", f"Erro ao conectar ao banco de dados: {err}")
        return None

def validar_login(email, senha):
    """Valida o login do usuário com base no e-mail e senha fornecidos."""
    conexao = conectar()
    if conexao:
        try:
            cursor = conexao.cursor()
            cursor.execute("SELECT senha FROM Usuarios WHERE email = %s", (email,))
            result = cursor.fetchone()
            
            if result:
                hashed_senha = result[0]
                if bcrypt.checkpw(senha.encode('utf-8'), hashed_senha.encode('utf-8')):
                    return True
                else:
                    return False
            else:
                return False
        finally:
            cursor.close()
            conexao.close()
    return False

def tela_de_login():
    # Criar a janela principal
    root = tk.Tk()
    root.title("Login")
    
    # Centralizar a janela no monitor
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    window_width = 400
    window_height = 300
    x = (screen_width - window_width) / 2
    y = (screen_height - window_height) / 2
    root.geometry(f'{window_width}x{window_height}+{int(x)}+{int(y)}')
    
    # Criar o frame principal
    main_frame = tk.Frame(root, bg='#f0f0f0')
    main_frame.pack(fill=tk.BOTH, expand=True)
    
    # Adicionar título
    title_label = tk.Label(
        main_frame, 
        text="Login", 
        font=('Arial', 24, 'bold'), 
        bg='#f0f0f0', 
        fg='#2196F3'
    )
    title_label.pack(pady=10)
    
    # Adicionar campos de entrada
    tk.Label(main_frame, text="E-mail:", bg='#f0f0f0').pack(pady=5)
    email_entry = tk.Entry(main_frame, font=('Arial', 12))
    email_entry.pack(pady=5, padx=10, fill=tk.X)
    
    tk.Label(main_frame, text="Senha:", bg='#f0f0f0').pack(pady=5)
    senha_entry = tk.Entry(main_frame, show='*', font=('Arial', 12))
    senha_entry.pack(pady=5, padx=10, fill=tk.X)
    
    def logar():
        email = email_entry.get()
        senha = senha_entry.get()

        if validar_login(email, senha):
            root.destroy()  # Fecha a tela de login
            import tela_de_lancamentos
            tela_de_lancamentos.tela_de_lancamentos()  # Abre a tela de lançamentos
        else:
            messagebox.showerror("Erro", "E-mail ou senha incorretos.")
    
    def cadastrar():
        # Abre a tela de cadastro e fecha a tela de login atual
        root.destroy()
        import tela_de_cadastro
        tela_de_cadastro.tela_de_cadastro()
    
    # Adicionar botões no rodapé
    footer_frame = tk.Frame(root, bg='#f0f0f0')
    footer_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10)
    
    login_button = tk.Button(
        footer_frame, 
        text="Logar", 
        font=('Arial', 12, 'bold'), 
        bg='#2196F3', 
        fg='white', 
        command=logar
    )
    login_button.pack(side=tk.RIGHT, padx=10)
    
    cadastrar_button = tk.Button(
        footer_frame, 
        text="Cadastrar", 
        font=('Arial', 12, 'bold'), 
        bg='#4CAF50', 
        fg='white', 
        command=cadastrar
    )
    cadastrar_button.pack(side=tk.LEFT, padx=10)
    
    root.mainloop()

if __name__ == "__main__":
    tela_de_login()
