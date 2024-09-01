import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import mysql.connector
from mysql.connector import Error
from validacoes import verificar_senha  # Certifique-se de que o caminho está correto
import json
from tela_de_usuario import criar_tela_usuario


def verificar_login(email, senha_fornecida):
    try:
        conn = mysql.connector.connect(host='localhost', database='CadastroUsuarios', user='root', password='123456789')
        cursor = conn.cursor()
        cursor.execute("SELECT senha FROM Usuarios WHERE email = %s", (email,))
        resultado = cursor.fetchone()
        
        if resultado:
            hash_armazenado = resultado[0]
            return verificar_senha(senha_fornecida, hash_armazenado)
        else:
            return False
    except mysql.connector.Error as e:
        print(f"Erro ao verificar login: {e}")
        return False
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

def carregar_configuracao():
    try:
        with open("config.json") as config_file:
            config = json.load(config_file)
            return config
    except FileNotFoundError:
        raise FileNotFoundError("O arquivo de configuração 'config.json' não foi encontrado.")
    except json.JSONDecodeError:
        raise ValueError("Erro ao decodificar o arquivo de configuração 'config.json'.")

def criar_tela_login(root):
    root.title("Tela de Login")
    
    largura_tela = root.winfo_screenwidth()
    altura_tela = root.winfo_screenheight()
    largura_janela = 900
    altura_janela = 600
    x = (largura_tela // 2) - (largura_janela // 2)
    y = (altura_tela // 2) - (altura_janela // 2)
    
    root.geometry(f"{largura_janela}x{altura_janela}+{x}+{y}")
    root.resizable(False, False)
    
    # Criar um frame principal
    frame_principal = tk.Frame(root, bg="#e3f2fd")
    frame_principal.pack(fill="both", expand=True)
    
    # Frame para a imagem
    frame_imagem = tk.Frame(frame_principal, bg="#ffffff", padx=20, pady=20)
    frame_imagem.pack(side="left", fill="both", expand=True)
    
    # Carregar e exibir a imagem
    try:
        img = Image.open("ia.png")  # Certifique-se de que a imagem está no mesmo diretório
        img_tk = ImageTk.PhotoImage(img)
        panel = tk.Label(frame_imagem, image=img_tk, bg="#ffffff")
        panel.image = img_tk
        panel.pack(pady=(altura_janela - 250) // 2, padx=(largura_janela * 0.6 - 485) // 2)  # Centraliza a imagem no frame
    except FileNotFoundError:
        tk.Label(frame_imagem, text="Imagem não encontrada", bg="#ffffff").pack(pady=20)
    
    # Frame para o formulário de login
    frame_login = tk.Frame(frame_principal, width=largura_janela * 0.4, height=altura_janela, bg="#ffffff", padx=20, pady=20)
    frame_login.pack(side="right", fill="both", expand=True)
    
    # Título do formulário
    tk.Label(frame_login, text="Login", font=("Arial", 30, "bold"), bg="#ffffff", fg="#0288d1").pack(pady=20)
    
    # Frame para os campos de entrada
    frame_campos = tk.Frame(frame_login, bg="#ffffff")
    frame_campos.pack(pady=20, fill="x", expand=True)
    
    # Campos de entrada com estilo
    tk.Label(frame_campos, text="E-mail", bg="#ffffff", font=("Arial", 14)).pack(anchor="w", padx=10)
    entrada_email = tk.Entry(frame_campos, font=("Arial", 14), bd=2, relief="solid")
    entrada_email.pack(pady=10, padx=10, fill="x", expand=True)
    
    tk.Label(frame_campos, text="Senha", bg="#ffffff", font=("Arial", 14)).pack(anchor="w", padx=10)
    entrada_senha = tk.Entry(frame_campos, show="*", font=("Arial", 14), bd=2, relief="solid")
    entrada_senha.pack(pady=10, padx=10, fill="x", expand=True)
    
    # Função para lidar com o login
    def realizar_login():
        email = entrada_email.get()
        senha = entrada_senha.get()
        try:
            logar_usuario(root, email, senha)  # Passa `root` como argumento
        except Exception as e:
            messagebox.showerror("Erro", str(e))
    
    # Botões
    frame_botoes = tk.Frame(frame_login, bg="#ffffff")
    frame_botoes.pack(pady=20, fill="x")
    
    botao_cadastrar = tk.Button(frame_botoes, text="Cadastrar", bg="#039be5", fg="#ffffff", font=("Arial", 14), relief="flat", command=lambda: abrir_tela_cadastro(root))
    botao_cadastrar.pack(pady=10, fill="x", padx=10)
    
    botao_login = tk.Button(frame_botoes, text="Login", bg="#0288d1", fg="#ffffff", font=("Arial", 14), relief="flat", command=realizar_login)
    botao_login.pack(pady=10, fill="x", padx=10)

def abrir_tela_cadastro(root):
    root.withdraw()  # Oculta a tela de login
    import tela_de_cadastro
    tela_de_cadastro.criar_tela_cadastro(root)

def logar_usuario(root, email, senha):
    config = carregar_configuracao()
    db_config = {
        'host': config.get('host'),
        'database': config.get('database'),
        'user': config.get('user'),
        'password': config.get('password')
    }
    
    try:
        conn = mysql.connector.connect(
            host=db_config['host'],
            database=db_config['database'],
            user=db_config['user'],
            password=db_config['password']
        )
        cursor = conn.cursor()

        cursor.execute("SELECT id, primeiro_nome, senha FROM Usuarios WHERE email = %s", (email,))
        usuario = cursor.fetchone()
        
        if usuario:
            usuario_id, primeiro_nome, hash_armazenado = usuario
            if verificar_senha(senha, hash_armazenado):
                print(f"Login bem-sucedido para o usuário com ID: {usuario_id}")
                root.withdraw()  # Oculta a tela de login
                criar_tela_usuario(root, usuario_id, primeiro_nome)  # Passa o primeiro_nome como nome_usuario
            else:
                messagebox.showerror("Erro", "E-mail ou senha incorretos.")
        else:
            messagebox.showerror("Erro", "E-mail ou senha incorretos.")
    except Error as e:
        messagebox.showerror("Erro", f"Erro ao fazer login: {e}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

