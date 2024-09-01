import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from mysql.connector import Error
import json

def carregar_configuracoes():
    with open('config.json', 'r') as arquivo:
        configuracoes = json.load(arquivo)
    return configuracoes

config = carregar_configuracoes()

def criar_tela_visualizacao(root, usuario_id):
    visualizar_window = tk.Toplevel(root)
    visualizar_window.title("Visualizar Lançamentos")

    largura_janela = 800
    altura_janela = 600
    largura_tela = root.winfo_screenwidth()
    altura_tela = root.winfo_screenheight()
    x = (largura_tela // 2) - (largura_janela // 2)
    y = (altura_tela // 2) - (altura_janela // 2)

    visualizar_window.geometry(f"{largura_janela}x{altura_janela}+{x}+{y}")
    visualizar_window.resizable(True, True)

    frame_visualizar = tk.Frame(visualizar_window, bg="#e3f2fd", padx=20, pady=20)
    frame_visualizar.pack(fill="both", expand=True)

    tree = ttk.Treeview(frame_visualizar, columns=("Tipo", "Data", "Valor", "Descrição", "Vencimento"), show="headings")
    tree.heading("Tipo", text="Tipo")
    tree.heading("Data", text="Data")
    tree.heading("Valor", text="Valor")
    tree.heading("Descrição", text="Descrição")
    tree.heading("Vencimento", text="Vencimento")
    tree.pack(fill="both", expand=True)

    def carregar_lancamentos():
        try:
            conn = mysql.connector.connect(
                host=config['host'],
                database=config['database'],
                user=config['user'],
                password=config['password']
            )
            cursor = conn.cursor()
            cursor.execute("""
                SELECT tipo, data_lancamento, valor, descricao, data_vencimento
                FROM Lancamentos
                WHERE usuario_id = %s
                """, (usuario_id,))
            for row in cursor.fetchall():
                tree.insert("", "end", values=row)
        except Error as e:
            messagebox.showerror("Erro", f"Erro ao carregar lançamentos: {e}")
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

    carregar_lancamentos()

    def excluir_lancamento():
        selected_item = tree.selection()
        if selected_item:
            item_values = tree.item(selected_item[0], 'values')
            tipo, data, valor, descricao, vencimento = item_values
            try:
                conn = mysql.connector.connect(
                    host=config['host'],
                    database=config['database'],
                    user=config['user'],
                    password=config['password']
                )
                cursor = conn.cursor()
                cursor.execute("""
                    DELETE FROM Lancamentos
                    WHERE tipo = %s AND data_lancamento = %s AND valor = %s AND descricao = %s AND data_vencimento = %s AND usuario_id = %s
                """, (tipo, data, valor, descricao, vencimento, usuario_id))
                conn.commit()
                messagebox.showinfo("Info", "Lançamento excluído com sucesso!")
                tree.delete(selected_item[0])
            except Error as e:
                messagebox.showerror("Erro", f"Erro ao excluir lançamento: {e}")
            finally:
                if conn.is_connected():
                    cursor.close()
                    conn.close()
        else:
            messagebox.showwarning("Aviso", "Nenhum lançamento selecionado.")

    def editar_lancamento():
        selected_item = tree.selection()
        if selected_item:
            item_values = tree.item(selected_item[0], 'values')
            tipo, data, valor, descricao, vencimento = item_values
            editar_window = tk.Toplevel(visualizar_window)
            editar_window.title("Editar Lançamento")
            tk.Label(editar_window, text="Tipo do Lançamento").pack(padx=10, pady=5)
            tipo_var = tk.StringVar(value=tipo)
            tk.Radiobutton(editar_window, text="Entrada", variable=tipo_var, value="Entrada").pack(anchor="w", padx=10)
            tk.Radiobutton(editar_window, text="Saída", variable=tipo_var, value="Saída").pack(anchor="w", padx=10)

            tk.Label(editar_window, text="Data de Lançamento").pack(padx=10, pady=5)
            entrada_data_lancamento = tk.Entry(editar_window, width=20)
            entrada_data_lancamento.insert(0, data)
            entrada_data_lancamento.pack(pady=5, padx=10)

            tk.Label(editar_window, text="Valor do Lançamento (R$)").pack(padx=10, pady=5)
            entrada_valor = tk.Entry(editar_window, width=20)
            entrada_valor.insert(0, valor)
            entrada_valor.pack(pady=5, padx=10)

            tk.Label(editar_window, text="Descrição do Lançamento").pack(padx=10, pady=5)
            entrada_descricao = tk.Entry(editar_window, width=20)
            entrada_descricao.insert(0, descricao)
            entrada_descricao.pack(pady=5, padx=10)

            tk.Label(editar_window, text="Data de Vencimento").pack(padx=10, pady=5)
            entrada_data_vencimento = tk.Entry(editar_window, width=20)
            entrada_data_vencimento.insert(0, vencimento)
            entrada_data_vencimento.pack(pady=5, padx=10)

            def salvar_edicao():
                novo_tipo = tipo_var.get()
                nova_data = entrada_data_lancamento.get()
                novo_valor = entrada_valor.get()
                nova_descricao = entrada_descricao.get()
                nova_vencimento = entrada_data_vencimento.get()

                if not novo_valor or not nova_descricao:
                    messagebox.showwarning("Aviso", "Todos os campos devem ser preenchidos.")
                    return

                novo_valor = novo_valor.replace(',', '.')

                try:
                    novo_valor = float(novo_valor)
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
                    cursor.execute("""
                        UPDATE Lancamentos
                        SET tipo = %s, data_lancamento = %s, valor = %s, descricao = %s, data_vencimento = %s
                        WHERE tipo = %s AND data_lancamento = %s AND valor = %s AND descricao = %s AND data_vencimento = %s AND usuario_id = %s
                    """, (novo_tipo, nova_data, novo_valor, nova_descricao, nova_vencimento, tipo, data, valor, descricao, vencimento, usuario_id))
                    conn.commit()
                    messagebox.showinfo("Info", "Lançamento editado com sucesso!")
                    carregar_lancamentos()
                    editar_window.destroy()
                except Error as e:
                    messagebox.showerror("Erro", f"Erro ao editar lançamento: {e}")
                finally:
                    if conn.is_connected():
                        cursor.close()
                        conn.close()

            tk.Button(editar_window, text="Salvar", command=salvar_edicao).pack(pady=10)

    frame_botoes = tk.Frame(frame_visualizar, bg="#e3f2fd")
    frame_botoes.pack(pady=20)

    botao_excluir = tk.Button(frame_botoes, text="Excluir Lançamento", bg="#c62828", fg="#ffffff", font=("Arial", 14), relief="flat", command=excluir_lancamento)
    botao_excluir.pack(side="left", padx=5)

    botao_editar = tk.Button(frame_botoes, text="Editar Lançamento", bg="#039be5", fg="#ffffff", font=("Arial", 14), relief="flat", command=editar_lancamento)
    botao_editar.pack(side="left", padx=5)

    def voltar_para_usuario():
        visualizar_window.destroy()

    botao_voltar = tk.Button(frame_botoes, text="Voltar", bg="#0288d1", fg="#ffffff", font=("Arial", 14), relief="flat", command=voltar_para_usuario)
    botao_voltar.pack(side="left", padx=5)

    def on_closing():
        visualizar_window.destroy()

    visualizar_window.protocol("WM_DELETE_WINDOW", on_closing)
