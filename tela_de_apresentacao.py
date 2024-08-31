import tkinter as tk
from tkinter import ttk
from tela_de_login import tela_de_login  # Importar a função tela_de_login

def configurar_janela(root, titulo, largura, altura):
    """Configura a janela principal e centraliza na tela."""
    root.title(titulo)
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - largura) / 2
    y = (screen_height - altura) / 2
    root.geometry(f'{largura}x{altura}+{int(x)}+{int(y)}')

def criar_descricao(main_frame):
    """Cria e adiciona a área de texto com a descrição ao frame principal."""
    descricao = (
        "Este App foi desenvolvido para apresentação do trabalho final do curso de graduação de Análise e Desenvolvimento de Sistemas.\n\n"
        "O objetivo aqui é apresentar funcionalidades bem estruturadas desenvolvidas em Python com conexão ao banco de dados MySQL, "
        "onde vocês poderão visualizar a validação de usuário login e senha, o cadastro de informações, exclusão de informações e "
        "extração de relatórios simulando um controle financeiro que pode ser usado por pessoas físicas e jurídicas.\n\n"
        "Os direitos estão reservados ao desenvolvedor Clayton F. Oliveira, que aplicou os conhecimentos aprendidos durante o curso, "
        "junto com a sua experiência na área e também com o auxílio de IAs para otimização do tempo e aperfeiçoamento da clareza do código."
    )
    
    descricao_label = tk.Label(
        main_frame,
        text=descricao,
        wraplength=550,  # Ajustar largura da linha para melhor visualização
        font=('Arial', 12),
        bg='#ffffff',
        fg='#000000',
        padx=10,
        pady=10
    )
    descricao_label.pack(fill=tk.BOTH, expand=True)

def criar_botao(feedback, texto, cor, comando, lado, frame):
    """Cria um botão e adiciona ao frame especificado."""
    botao = tk.Button(
        frame,
        text=texto,
        font=('Arial', 12, 'bold'),
        bg=cor,
        fg='white',
        command=comando
    )
    botao.pack(side=lado, padx=10)
    return botao

def tela_de_apresentacao():
    # Criar a janela principal
    root = tk.Tk()
    
    # Configurar janela
    configurar_janela(root, "Registros de Fluxo de Caixa", 600, 400)
    
    # Criar o frame principal
    main_frame = tk.Frame(root, bg='#f0f0f0')
    main_frame.pack(fill=tk.BOTH, expand=True)
    
    # Adicionar título
    title_label = tk.Label(
        main_frame,
        text="FLUXO DE CAIXA - IMPACTA",
        font=('Arial', 24, 'bold'),
        bg='#f0f0f0',
        fg='#2196F3'
    )
    title_label.pack(pady=10)
    
    # Adicionar descrição
    criar_descricao(main_frame)

    # Adicionar botões no rodapé
    footer_frame = tk.Frame(root, bg='#f0f0f0')
    footer_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10)
    
    criar_botao("Fechar o Aplicativo", "Fechar o Aplicativo", '#f44336', root.quit, tk.LEFT, footer_frame)
    criar_botao("Fazer Login", "Fazer Login", '#2196F3', lambda: (root.destroy(), tela_de_login()), tk.RIGHT, footer_frame)
    
    root.mainloop()

if __name__ == "__main__":
    tela_de_apresentacao()
