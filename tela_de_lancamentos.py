import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
import mysql.connector
from tkinter import messagebox
import json
import pandas as pd

def carregar_configuracoes():
    with open('config.json') as f:
        return json.load(f)

def criar_conexao():
    config = carregar_configuracoes()
    return mysql.connector.connect(
        host=config['host'],
        user=config['user'],
        password=config['password'],
        database=config['database']
    )

def fechar_conexao(conexao):
    conexao.close()

def salvar_lancamento_no_db(data_lancamento, data_vencimento, valor, tipo, descricao):
    try:
        conexao = criar_conexao()
        cursor = conexao.cursor()
        cursor.execute("""
            INSERT INTO Lançamentos (valor, tipo, data_lancamento, data_vencimento, descricao) 
            VALUES (%s, %s, %s, %s, %s)
        """, (valor, tipo, data_lancamento, data_vencimento, descricao))
        conexao.commit()
        cursor.close()
        fechar_conexao(conexao)
        messagebox.showinfo("Sucesso", "Lançamento salvo com sucesso.")
    except mysql.connector.Error as err:
        messagebox.showerror("Erro", f"Erro ao salvar lançamento: {err}")

def exportar_para_excel():
    try:
        conexao = criar_conexao()
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM Lançamentos")
        registros = cursor.fetchall()
        colunas = [i[0] for i in cursor.description]
        cursor.close()
        fechar_conexao(conexao)

        df = pd.DataFrame(registros, columns=colunas)
        df.to_excel('lancamentos.xlsx', index=False, engine='openpyxl')
        messagebox.showinfo("Sucesso", "Dados exportados para Excel com sucesso.")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao exportar dados: {e}")

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

    button_frame = tk.Frame(visualizacao)
    button_frame.pack(fill=tk.X, pady=10)

    atualizar_button = tk.Button(button_frame, text="Atualizar", command=lambda: atualizar_lancamento(tree.selection()[0]))
    atualizar_button.pack(side=tk.LEFT, padx=10)

    excluir_button = tk.Button(button_frame, text="Excluir", command=lambda: excluir_lancamento(tree.selection()[0]))
    excluir_button.pack(side=tk.LEFT, padx=10)
    
    exportar_button = tk.Button(button_frame, text="Exportar para Excel", command=exportar_para_excel)
    exportar_button.pack(side=tk.RIGHT, padx=10)

def tela_de_lancamentos():
    root = tk.Tk()
    root.title("Lançamentos")
    
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    window_width = 600
    window_height = 500
    x = (screen_width - window_width) / 2
    y = (screen_height - window_height) / 2
    root.geometry(f'{window_width}x{window_height}+{int(x)}+{int(y)}')

    main_frame = tk.Frame(root, bg='#f0f0f0')
    main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    title_label = tk.Label(main_frame, text="Lançamentos", font=('Arial', 24, 'bold'), bg='#f0f0f0', fg='#2196F3')
    title_label.pack(pady=10)

    tk.Label(main_frame, text="Data de Lançamento:", bg='#f0f0f0').pack(pady=5)
    data_lancamento_entry = DateEntry(main_frame, width=15, background='darkblue', foreground='white', borderwidth=2)
    data_lancamento_entry.pack(pady=5, padx=10)
    
    tk.Label(main_frame, text="Data de Vencimento (Opcional):", bg='#f0f0f0').pack(pady=5)
    data_vencimento_entry = DateEntry(main_frame, width=15, background='darkblue', foreground='white', borderwidth=2)
    data_vencimento_entry.pack(pady=5, padx=10)
    
    tk.Label(main_frame, text="Valor:", bg='#f0f0f0').pack(pady=5)
    valor_entry = tk.Entry(main_frame, font=('Arial', 12))
    valor_entry.pack(pady=5, padx=10, fill=tk.X)
    
    tk.Label(main_frame, text="Tipo de Registro:", bg='#f0f0f0').pack(pady=5)
    tipo_var = tk.StringVar()
    tipo_entry = ttk.Combobox(main_frame, textvariable=tipo_var, values=['Entrada', 'Saída'], state='readonly')
    tipo_entry.pack(pady=5, padx=10, fill=tk.X)
    
    tk.Label(main_frame, text="Descrição do Lançamento:", bg='#f0f0f0').pack(pady=5)
    descricao_entry = tk.Entry(main_frame, font=('Arial', 12))
    descricao_entry.pack(pady=5, padx=10, fill=tk.X)
    
    def limpar_campos():
        data_lancamento_entry.set_date(None)
        data_vencimento_entry.set_date(None)
        valor_entry.delete(0, tk.END)
        tipo_entry.set('')
        descricao_entry.delete(0, tk.END)
    
    def processar_salvar_lancamento():
        data_lancamento = data_lancamento_entry.get_date()
        data_vencimento = data_vencimento_entry.get_date() if data_vencimento_entry.get_date() else None
        valor = valor_entry.get().replace(',', '.')
        tipo = tipo_var.get()
        descricao = descricao_entry.get()
        salvar_lancamento_no_db(data_lancamento, data_vencimento, valor, tipo, descricao)
        limpar_campos()

    footer_frame = tk.Frame(root, bg='#f0f0f0')
    footer_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10)
    
    visualizar_button = tk.Button(
        footer_frame, text="Visualizar", font=('Arial', 12, 'bold'), bg='#2196F3', fg='white', command=lambda: visualizar_lancamentos(root)
    )
    visualizar_button.pack(side=tk.LEFT, padx=10)
    
    salvar_button = tk.Button(
        footer_frame, text="Salvar", font=('Arial', 12, 'bold'), bg='#4CAF50', fg='white', command=processar_salvar_lancamento
    )
    salvar_button.pack(side=tk.RIGHT, padx=10)
    
    cancelar_button = tk.Button(
        footer_frame, text="Cancelar", font=('Arial', 12, 'bold'), bg='#f44336', fg='white', command=root.destroy
    )
    cancelar_button.pack(side=tk.LEFT, padx=10)
    
    root.mainloop()

if __name__ == "__main__":
    tela_de_lancamentos()
