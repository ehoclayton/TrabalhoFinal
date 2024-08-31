import tkinter as tk
from tkinter import ttk

def aplicar_estilos_login(root):
    root.configure(bg="#f0f0f0")

    title_font = ('Arial', 16, 'bold')
    label_font = ('Arial', 12)
    button_font = ('Arial', 10, 'bold')

    tk.Label(root, text="Usuário", bg="#f0f0f0", font=label_font).grid(row=0, column=0, padx=10, pady=5, sticky='e')
    tk.Label(root, text="Senha", bg="#f0f0f0", font=label_font).grid(row=1, column=0, padx=10, pady=5, sticky='e')

    # Não criar botões aqui, apenas aplicar estilos
    # Botões serão criados no código da tela de login



def aplicar_estilos_cadastro(root):
    root.configure(bg="#f0f0f0")

    label_font = ('Arial', 12)
    button_font = ('Arial', 10, 'bold')

    tk.Label(root, text="Nome", bg="#f0f0f0", font=label_font).grid(row=0, column=0, padx=10, pady=5, sticky='e')
    tk.Label(root, text="Email", bg="#f0f0f0", font=label_font).grid(row=1, column=0, padx=10, pady=5, sticky='e')
    tk.Label(root, text="Senha", bg="#f0f0f0", font=label_font).grid(row=2, column=0, padx=10, pady=5, sticky='e')

    tk.Button(root, text="Cadastrar", font=button_font, bg="#4CAF50", fg="white", relief="raised").grid(row=3, column=0, columnspan=2, padx=10, pady=10)


def aplicar_estilos_ambiente(root):
    root.configure(bg="#f0f0f0")

    label_font = ('Arial', 12)
    button_font = ('Arial', 10, 'bold')

    tk.Label(root, text="Valor", bg="#f0f0f0", font=label_font).grid(row=0, column=0, padx=10, pady=5, sticky='e')
    tk.Label(root, text="Tipo", bg="#f0f0f0", font=label_font).grid(row=1, column=0, padx=10, pady=5, sticky='e')
    tk.Label(root, text="Data de Lançamento", bg="#f0f0f0", font=label_font).grid(row=2, column=0, padx=10, pady=5, sticky='e')
    tk.Label(root, text="Data de Vencimento", bg="#f0f0f0", font=label_font).grid(row=3, column=0, padx=10, pady=5, sticky='e')
    tk.Label(root, text="Descrição", bg="#f0f0f0", font=label_font).grid(row=4, column=0, padx=10, pady=5, sticky='e')

    tk.Button(root, text="Salvar Lançamento", font=button_font, bg="#4CAF50", fg="white", relief="raised").grid(row=5, column=0, columnspan=2, padx=10, pady=10)

    tree = ttk.Treeview(root, columns=("Valor", "Tipo", "Data de Lançamento", "Data de Vencimento", "Descrição"), show="headings")
    for col in tree["columns"]:
        tree.heading(col, text=col, anchor='w')
        tree.column(col, anchor='w', width=100)
    tree.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

