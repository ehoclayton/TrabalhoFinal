import tkinter as tk
from tkinter import messagebox
from tkcalendar import DateEntry
import mysql.connector
from mysql.connector import Error
import json
import visualizar_lancamentos

def carregar_configuracoes():
    with open('config.json', 'r') as arquivo:
        configuracoes = json.load(arquivo)
    return configuracoes

# Carregar configurações
config = carregar_configuracoes()

def criar_tela_usuario(root, usuario_id, nome_usuario):
    usuario_window = tk.Toplevel(root)
    usuario_window.title("Tela de Lançamento")

    largura_janela = 800
    altura_janela = 700
    largura_tela = root.winfo_screenwidth()
    altura_tela = root.winfo_screenheight()
    x = (largura_tela // 2) - (largura_janela // 2)
    y = (altura_tela // 2) - (altura_janela // 2)

    usuario_window.geometry(f"{largura_janela}x{altura_janela}+{x}+{y}")
    usuario_window.resizable(True, True)

    frame_usuario = tk.Frame(usuario_window, bg="#e3f2fd", padx=20, pady=20)
    frame_usuario.pack(fill="both", expand=True)

    tk.Label(frame_usuario, text=f"Bem-vindo, {nome_usuario}", font=("Arial", 16), bg="#e3f2fd").pack(anchor="w", padx=10, pady=10)
    tk.Label(frame_usuario, text="Nome do Usuário", font=("Arial", 14), bg="#e3f2fd").pack(anchor="w", padx=10, pady=5)
    tk.Label(frame_usuario, text=nome_usuario, font=("Arial", 14), bg="#e3f2fd").pack(anchor="w", padx=10, pady=5)

    tk.Label(frame_usuario, text="Tipo do Lançamento", font=("Arial", 14), bg="#e3f2fd").pack(anchor="w", padx=10, pady=5)
    tipo_var = tk.StringVar(value="Entrada")
    tk.Radiobutton(frame_usuario, text="Entrada", variable=tipo_var, value="Entrada", font=("Arial", 14), bg="#e3f2fd").pack(anchor="w", padx=10)
    tk.Radiobutton(frame_usuario, text="Saída", variable=tipo_var, value="Saída", font=("Arial", 14), bg="#e3f2fd").pack(anchor="w", padx=10)

    tk.Label(frame_usuario, text="Data de Lançamento", font=("Arial", 14), bg="#e3f2fd").pack(anchor="w", padx=10, pady=5)
    entrada_data_lancamento = DateEntry(frame_usuario, font=("Arial", 14), bd=2, relief="solid")
    entrada_data_lancamento.pack(pady=5, padx=10, fill="x")

    tk.Label(frame_usuario, text="Valor do Lançamento (R$)", font=("Arial", 14), bg="#e3f2fd").pack(anchor="w", padx=10, pady=5)
    entrada_valor = tk.Entry(frame_usuario, font=("Arial", 14), bd=2, relief="solid")
    entrada_valor.pack(pady=5, padx=10, fill="x")

    tk.Label(frame_usuario, text="Descrição do Lançamento", font=("Arial", 14), bg="#e3f2fd").pack(anchor="w", padx=10, pady=5)
    entrada_descricao = tk.Entry(frame_usuario, font=("Arial", 14), bd=2, relief="solid")
    entrada_descricao.pack(pady=5, padx=10, fill="x")

    tk.Label(frame_usuario, text="Data de Vencimento (Opcional)", font=("Arial", 14), bg="#e3f2fd").pack(anchor="w", padx=10, pady=5)
    entrada_data_vencimento = DateEntry(frame_usuario, font=("Arial", 14), bd=2, relief="solid")
    entrada_data_vencimento.pack(pady=5, padx=10, fill="x")

    def salvar_lancamento():
        tipo = tipo_var.get()
        data_lancamento = entrada_data_lancamento.get_date()
        valor = entrada_valor.get()
        descricao = entrada_descricao.get()
        data_vencimento = entrada_data_vencimento.get_date() if entrada_data_vencimento.get_date() else None

        if not valor or not descricao:
            messagebox.showwarning("Aviso", "Todos os campos devem ser preenchidos.")
            return

        valor = valor.replace(',', '.')

        try:
            valor = float(valor)
        except ValueError:
            messagebox.showwarning("Aviso", "Valor inválido.")
            return

        try:
            conn = mysql.connector.connect(
                host=config['host'],
                database=config['database'],
                user=config['user'],
                password=config['password']
            )
            cursor = conn.cursor()
            cursor.execute("INSERT INTO Lancamentos (usuario_id, tipo, data_lancamento, valor, descricao, data_vencimento) VALUES (%s, %s, %s, %s, %s, %s)",
                           (usuario_id, tipo, data_lancamento, valor, descricao, data_vencimento))
            conn.commit()
            messagebox.showinfo("Info", "Lançamento salvo com sucesso!")
        except Error as e:
            messagebox.showerror("Erro", f"Erro ao salvar lançamento: {e}")
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

    def visualizar_lancamentos():
        usuario_window.withdraw()  # Oculta a janela atual
        visualizar_lancamentos.criar_tela_visualizacao(usuario_window, usuario_id, nome_usuario)  # Chama a nova tela de visualização

    def voltar_para_login():
        usuario_window.destroy()
        root.deiconify()

    frame_botoes = tk.Frame(frame_usuario, bg="#e3f2fd")
    frame_botoes.pack(pady=20)

    botao_salvar = tk.Button(frame_botoes, text="Salvar Lançamento", bg="#039be5", fg="#ffffff", font=("Arial", 14), relief="flat", command=salvar_lancamento)
    botao_salvar.pack(side="left", padx=5)

    botao_visualizar = tk.Button(frame_botoes, text="Visualizar Lançamentos", bg="#0288d1", fg="#ffffff", font=("Arial", 14), relief="flat", command=visualizar_lancamentos)
    botao_visualizar.pack(side="left", padx=5)

    botao_voltar = tk.Button(frame_botoes, text="Voltar", bg="#0288d1", fg="#ffffff", font=("Arial", 14), relief="flat", command=voltar_para_login)
    botao_voltar.pack(side="left", padx=5)

    def atualizar_saldo():
        try:
            conn = mysql.connector.connect(
                host=config['host'],
                database=config['database'],
                user=config['user'],
                password=config['password']
            )
            cursor = conn.cursor()

            cursor.execute("""
                SELECT SUM(valor) FROM Lancamentos
                WHERE tipo = 'Entrada' AND data_lancamento <= CURDATE() AND usuario_id = %s
            """, (usuario_id,))
            total_entradas = cursor.fetchone()[0] or 0

            cursor.execute("""
                SELECT SUM(valor) FROM Lancamentos
                WHERE tipo = 'Saída' AND data_lancamento <= CURDATE() AND usuario_id = %s
            """, (usuario_id,))
            total_saidas = cursor.fetchone()[0] or 0

            saldo_atual = total_entradas - total_saidas

            tk.Label(frame_usuario, text=f"Saldo Atual: R${saldo_atual:.2f}", font=("Arial", 14), bg="#e3f2fd").pack(anchor="w", padx=10, pady=10)
            tk.Label(frame_usuario, text=f"Total de Entradas: R${total_entradas:.2f}", font=("Arial", 14), bg="#e3f2fd").pack(anchor="w", padx=10, pady=5)
            tk.Label(frame_usuario, text=f"Total de Saídas: R${total_saidas:.2f}", font=("Arial", 14), bg="#e3f2fd").pack(anchor="w", padx=10, pady=5)
        except Error as e:
            messagebox.showerror("Erro", f"Erro ao atualizar saldo: {e}")
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

    atualizar_saldo()

    def on_closing():
        usuario_window.destroy()
        root.deiconify()

    usuario_window.protocol("WM_DELETE_WINDOW", on_closing)
