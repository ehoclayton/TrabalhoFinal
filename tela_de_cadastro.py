# tela_de_cadastro.py

import tkinter as tk
from tkinter import messagebox
from tkcalendar import DateEntry
import mysql.connector
import bcrypt
from validacoes import validar_email, validar_senha


def criar_tela_cadastro(root):
    def salvar_usuario():
        primeiro_nome = entrada_primeiro_nome.get()
        ultimo_nome = entrada_ultimo_nome.get()
        email = entrada_email.get()
        senha = entrada_senha.get()
        repetir_senha = entrada_repetir_senha.get()
        data_nascimento = entrada_data_nascimento.get_date().strftime('%Y-%m-%d')
        nome_usuario = primeiro_nome
        
        if not validar_email(email):
            messagebox.showwarning("Aviso", "E-mail inválido.")
            return
        
        if not validar_senha(senha):
            messagebox.showwarning("Aviso", "A senha deve ter pelo menos 6 caracteres.")
            return
        
        if senha != repetir_senha:
            messagebox.showwarning("Aviso", "As senhas não coincidem.")
            return
        
        hash_senha = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        try:
            conn = mysql.connector.connect(host='localhost', database='CadastroUsuarios', user='root', password='123456789')
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO Usuarios (primeiro_nome, ultimo_nome, data_nascimento, email, senha)
                VALUES (%s, %s, %s, %s, %s)
            """, (primeiro_nome, ultimo_nome, data_nascimento, email, hash_senha))
            conn.commit()
            messagebox.showinfo("Info", "Cadastro realizado com sucesso!")
        except mysql.connector.Error as e:
            messagebox.showerror("Erro", f"Erro ao cadastrar usuário: {e}")
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

    cadastro_window = tk.Toplevel(root)
    cadastro_window.title("Tela de Cadastro")
    
    largura_janela = 400
    altura_janela = 600
    largura_tela = root.winfo_screenwidth()
    altura_tela = root.winfo_screenheight()
    x = (largura_tela // 2) - (largura_janela // 2)
    y = (altura_tela // 2) - (altura_janela // 2)
    
    cadastro_window.geometry(f"{largura_janela}x{altura_janela}+{x}+{y}")
    cadastro_window.resizable(False, False)

    # Evita o fechamento do aplicativo principal
    cadastro_window.protocol("WM_DELETE_WINDOW", lambda: [cadastro_window.destroy(), root.deiconify()])

    frame_cadastro = tk.Frame(cadastro_window, bg="#e3f2fd", padx=20, pady=20)
    frame_cadastro.pack(fill="both", expand=True)
    
    tk.Label(frame_cadastro, text="Primeiro Nome", font=("Arial", 14), bg="#e3f2fd").pack(anchor="w", padx=10, pady=5)
    entrada_primeiro_nome = tk.Entry(frame_cadastro, font=("Arial", 14), bd=2, relief="solid")
    entrada_primeiro_nome.pack(pady=5, padx=10, fill="x")
    
    tk.Label(frame_cadastro, text="Último Nome", font=("Arial", 14), bg="#e3f2fd").pack(anchor="w", padx=10, pady=5)
    entrada_ultimo_nome = tk.Entry(frame_cadastro, font=("Arial", 14), bd=2, relief="solid")
    entrada_ultimo_nome.pack(pady=5, padx=10, fill="x")
    
    tk.Label(frame_cadastro, text="E-mail", font=("Arial", 14), bg="#e3f2fd").pack(anchor="w", padx=10, pady=5)
    entrada_email = tk.Entry(frame_cadastro, font=("Arial", 14), bd=2, relief="solid")
    entrada_email.pack(pady=5, padx=10, fill="x")
    
    tk.Label(frame_cadastro, text="Senha", font=("Arial", 14), bg="#e3f2fd").pack(anchor="w", padx=10, pady=5)
    entrada_senha = tk.Entry(frame_cadastro, show="*", font=("Arial", 14), bd=2, relief="solid")
    entrada_senha.pack(pady=5, padx=10, fill="x")
    
    tk.Label(frame_cadastro, text="Repetir Senha", font=("Arial", 14), bg="#e3f2fd").pack(anchor="w", padx=10, pady=5)
    entrada_repetir_senha = tk.Entry(frame_cadastro, show="*", font=("Arial", 14), bd=2, relief="solid")
    entrada_repetir_senha.pack(pady=5, padx=10, fill="x")
    
    tk.Label(frame_cadastro, text="Data de Nascimento", font=("Arial", 14), bg="#e3f2fd").pack(anchor="w", padx=10, pady=5)
    entrada_data_nascimento = DateEntry(frame_cadastro, font=("Arial", 14), bd=2, relief="solid")
    entrada_data_nascimento.pack(pady=5, padx=10, fill="x")
    
    # Frame para os botões lado a lado
    frame_botoes = tk.Frame(frame_cadastro, bg="#e3f2fd")
    frame_botoes.pack(pady=20)
    
    botao_salvar = tk.Button(frame_botoes, text="Salvar Cadastro", bg="#039be5", fg="#ffffff", font=("Arial", 14), relief="flat", command=salvar_usuario)
    botao_salvar.pack(side="left", padx=10)
    
    botao_voltar = tk.Button(frame_botoes, text="Voltar", bg="#0288d1", fg="#ffffff", font=("Arial", 14), relief="flat", command=lambda: [cadastro_window.destroy(), root.deiconify()])
    botao_voltar.pack(side="left", padx=10)

