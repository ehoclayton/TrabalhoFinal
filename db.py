import mysql.connector
import json
from validacoes import validar_email

def carregar_config():
    with open('config.json') as f:
        return json.load(f)

def conectar_banco():
    config = carregar_config()
    return mysql.connector.connect(
        host=config['host'],
        user=config['user'],
        password=config['password'],
        database=config['database']
    )

def verificar_login(email, senha, root):
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Usuarios WHERE email = %s AND senha = %s", (email, senha))
    resultado = cursor.fetchone()
    conn.close()
    if resultado:
        messagebox.showinfo("Login", "Login bem-sucedido!")
        # Adicione código para abrir a tela principal aqui
    else:
        messagebox.showerror("Login", "E-mail ou senha inválidos.")

def salvar_usuario(primeiro_nome, ultimo_nome, data_nascimento, sexo, email, senha, repetir_senha, tela_cadastro):
    from validacoes import validar_campos
    try:
        validar_campos(primeiro_nome, ultimo_nome, email, senha, repetir_senha)
        conn = conectar_banco()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Usuarios (primeiro_nome, ultimo_nome, data_nascimento, sexo, email, senha) VALUES (%s, %s, %s, %s, %s, %s)",
                       (primeiro_nome, ultimo_nome, data_nascimento, sexo, email, senha))
        conn.commit()
        conn.close()
        messagebox.showinfo("Cadastro", "Cadastro realizado com sucesso!")
        tela_cadastro.destroy()
    except ValueError as e:
        messagebox.showerror("Erro", str(e))
