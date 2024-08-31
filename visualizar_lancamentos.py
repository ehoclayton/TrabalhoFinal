import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
import mysql.connector
from tkinter import messagebox

def criar_conexao():
    # Defina a função para criar a conexão com o banco de dados
    # Substitua os parâmetros com suas configurações
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='20@Fev91',
        database='CadastroUsuarios'
    )

def fechar_conexao(conexao):
    conexao.close()

def atualizar_lancamento(tree, data_lancamento_entry, data_vencimento_entry, valor_entry, tipo_entry, descricao_entry):
    try:
        selected_item = tree.selection()[0]
        values = tree.item(selected_item, 'values')
        id_lancamento = values[0]
        
        data_lancamento = data_lancamento_entry.get_date()
        data_vencimento = data_vencimento_entry.get_date() if data_vencimento_entry.get_date() else None
        valor = valor_entry.get().replace(',', '.')
        tipo = tipo_entry.get()
        descricao = descricao_entry.get()
        
        conexao = criar_conexao()
        cursor = conexao.cursor()
        cursor.execute("""
            UPDATE Lançamentos
            SET data_lancamento = %s, data_vencimento = %s, valor = %s, tipo = %s, descricao = %s
            WHERE id = %s
        """, (data_lancamento, data_vencimento, valor, tipo, descricao, id_lancamento))
        conexao.commit()
        cursor.close()
        fechar_conexao(conexao)
        messagebox.showinfo("Sucesso", "Lançamento atualizado com sucesso.")
    except mysql.connector.Error as err:
        messagebox.showerror("Erro", f"Erro ao atualizar lançamento: {err}")

def visualizar_lancamentos(root):
    visualizacao = tk.Toplevel(root)
    visualizacao.title("Visualizar Lançamentos")
    
    screen_width = visualizacao.winfo_screenwidth()
    screen_height = visualizacao.winfo_screenheight()
    window_width = 800
    window_height = 500
    x = (screen_width - window_width) / 2
    y = (screen_height - window_height) / 2
    visualizacao.geometry(f'{window_width}x{window_height}+{int(x)}+{int(y)}')

    table_frame = tk.Frame(visualizacao)
    table_frame.pack(fill=tk.BOTH, expand=True)

    columns = ('id', 'data_lancamento', 'data_vencimento', 'valor', 'tipo', 'descricao')
    tree = ttk.Treeview(table_frame, columns=columns, show='headings')
    tree.pack(fill=tk.BOTH, expand=True)

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=100, anchor='center')

    def preencher_tabela():
        try:
            conexao = criar_conexao()
            cursor = conexao.cursor()
            cursor.execute("SELECT * FROM Lançamentos")
            registros = cursor.fetchall()
            cursor.close()
            fechar_conexao(conexao)

            for item in tree.get_children():
                tree.delete(item)

            for registro in registros:
                tree.insert("", tk.END, values=registro)
        except mysql.connector.Error as err:
            messagebox.showerror("Erro", f"Erro ao carregar lançamentos: {err}")

    preencher_tabela()

    # Frames para edição
    edit_frame = tk.Frame(visualizacao)
    edit_frame.pack(fill=tk.BOTH, pady=10)

    tk.Label(edit_frame, text="Data de Lançamento:").pack(pady=5)
    data_lancamento_entry = DateEntry(edit_frame, width=15, background='darkblue', foreground='white', borderwidth=2)
    data_lancamento_entry.pack(pady=5, padx=10)

    tk.Label(edit_frame, text="Data de Vencimento (Opcional):").pack(pady=5)
    data_vencimento_entry = DateEntry(edit_frame, width=15, background='darkblue', foreground='white', borderwidth=2)
    data_vencimento_entry.pack(pady=5, padx=10)

    tk.Label(edit_frame, text="Valor:").pack(pady=5)
    valor_entry = tk.Entry(edit_frame, font=('Arial', 12))
    valor_entry.pack(pady=5, padx=10, fill=tk.X)

    tk.Label(edit_frame, text="Tipo de Registro:").pack(pady=5)
    tipo_var = tk.StringVar()
    tipo_entry = ttk.Combobox(edit_frame, textvariable=tipo_var, values=['Entrada', 'Saída'], state='readonly')
    tipo_entry.pack(pady=5, padx=10, fill=tk.X)

    tk.Label(edit_frame, text="Descrição do Lançamento:").pack(pady=5)
    descricao_entry = tk.Entry(edit_frame, font=('Arial', 12))
    descricao_entry.pack(pady=5, padx=10, fill=tk.X)

    button_frame = tk.Frame(visualizacao)
    button_frame.pack(fill=tk.X, pady=10)

    atualizar_button = tk.Button(button_frame, text="Atualizar", command=lambda: atualizar_lancamento(tree, data_lancamento_entry, data_vencimento_entry, valor_entry, tipo_entry, descricao_entry))
    atualizar_button.pack(side=tk.LEFT, padx=10)

    excluir_button = tk.Button(button_frame, text="Excluir", command=lambda: excluir_lancamento(tree.selection()[0]))
    excluir_button.pack(side=tk.LEFT, padx=10)

def excluir_lancamento(id_lancamento):
    try:
        conexao = criar_conexao()
        cursor = conexao.cursor()
        cursor.execute("DELETE FROM Lançamentos WHERE id = %s", (id_lancamento,))
        conexao.commit()
        cursor.close()
        fechar_conexao(conexao)
        messagebox.showinfo("Sucesso", "Lançamento excluído com sucesso.")
    except mysql.connector.Error as err:
        messagebox.showerror("Erro", f"Erro ao excluir lançamento: {err}")

if __name__ == "__main__":
    # Função para rodar a tela principal para teste
    import tela_de_lancamentos
    tela_de_lancamentos.tela_de_lancamentos()
