import tkinter as tk
from tkinter import messagebox
import mysql.connector
import bcrypt
import re

def validar_email(email):
    """Valida o formato do e-mail."""
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def validar_senha(senha):
    """Valida a força da senha."""
    return len(senha) >= 6

def criar_campo(frame, rotulo_texto, tipo='text', mostrar='*'):
    """Cria um campo de entrada com rótulo."""
    tk.Label(frame, text=rotulo_texto, bg='#f0f0f0').pack(pady=5)
    if tipo == 'text':
        return tk.Entry(frame, font=('Arial', 12))
    elif tipo == 'password':
        return tk.Entry(frame, show=mostrar, font=('Arial', 12))

def cadastrar(nome_entry, email_entry, senha_entry, repetir_senha_entry):
    """Função para realizar o cadastro do usuário."""
    nome = nome_entry.get()
    email = email_entry.get()
    senha = senha_entry.get()
    repetir_senha = repetir_senha_entry.get()
    
    if not validar_email(email):
        messagebox.showerror("Erro", "O e-mail fornecido é inválido.")
        return
    
    if not validar_senha(senha):
        messagebox.showerror("Erro", "A senha deve ter pelo menos 6 caracteres.")
        return

    if senha != repetir_senha:
        messagebox.showerror("Erro", "As senhas não coincidem.")
        return
    
    # Hash da senha
    hashed_senha = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt())
    
    try:
        conexao = mysql.connector.connect(
            host='localhost',
            user='root',
            password='20@Fev91',
            database='CadastroUsuarios'
        )
        cursor = conexao.cursor()
        cursor.execute("""
            INSERT INTO Usuarios (nome, email, senha) 
            VALUES (%s, %s, %s)
        """, (nome, email, hashed_senha))
        conexao.commit()
        cursor.close()
        conexao.close()
        
        messagebox.showinfo("Sucesso", "Cadastro realizado com sucesso.")
        
        root.destroy()  # Fecha a tela de cadastro
        import tela_de_login
        tela_de_login.tela_de_login()  # Reabre a tela de login
        
    except mysql.connector.Error as err:
        messagebox.showerror("Erro", f"Erro ao cadastrar: {err}")

def tela_de_cadastro():
    """Cria e exibe a tela de cadastro."""
    root = tk.Tk()
    root.title("Cadastro")
    
    # Centralizar a janela no monitor
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    window_width = 400
    window_height = 400
    x = (screen_width - window_width) / 2
    y = (screen_height - window_height) / 2
    root.geometry(f'{window_width}x{window_height}+{int(x)}+{int(y)}')
    
    # Criar o frame principal
    main_frame = tk.Frame(root, bg='#f0f0f0')
    main_frame.pack(fill=tk.BOTH, expand=True)
    
    # Adicionar título
    title_label = tk.Label(
        main_frame, 
        text="Cadastro", 
        font=('Arial', 24, 'bold'), 
        bg='#f0f0f0', 
        fg='#2196F3'
    )
    title_label.pack(pady=10)
    
    # Adicionar campos de entrada
    nome_entry = criar_campo(main_frame, "Nome:")
    nome_entry.pack(pady=5, padx=10, fill=tk.X)
    
    email_entry = criar_campo(main_frame, "E-mail:")
    email_entry.pack(pady=5, padx=10, fill=tk.X)
    
    senha_entry = criar_campo(main_frame, "Senha:", tipo='password')
    senha_entry.pack(pady=5, padx=10, fill=tk.X)
    
    repetir_senha_entry = criar_campo(main_frame, "Repetir Senha:", tipo='password')
    repetir_senha_entry.pack(pady=5, padx=10, fill=tk.X)
    
    # Adicionar botões no rodapé
    footer_frame = tk.Frame(root, bg='#f0f0f0')
    footer_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10)
    
    cadastrar_button = tk.Button(
        footer_frame, 
        text="Cadastrar", 
        font=('Arial', 12, 'bold'), 
        bg='#4CAF50', 
        fg='white', 
        command=lambda: cadastrar(nome_entry, email_entry, senha_entry, repetir_senha_entry)
    )
    cadastrar_button.pack(side=tk.RIGHT, padx=10)
    
    cancelar_button = tk.Button(
        footer_frame, 
        text="Cancelar", 
        font=('Arial', 12, 'bold'), 
        bg='#f44336', 
        fg='white', 
        command=root.destroy
    )
    cancelar_button.pack(side=tk.LEFT, padx=10)
    
    root.mainloop()

if __name__ == "__main__":
    tela_de_cadastro()
