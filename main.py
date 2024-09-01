import tkinter as tk
import sys
import os
from tela_de_login import criar_tela_login

# Adicione o diretório atual ao caminho do módulo
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def main():
    root = tk.Tk()
    root.title("FLUXER")
    
    largura_tela = root.winfo_screenwidth()
    altura_tela = root.winfo_screenheight()
    largura_janela = 900
    altura_janela = 600
    x = (largura_tela // 2) - (largura_janela // 2)
    y = (altura_tela // 2) - (altura_janela // 2)
    
    root.geometry(f"{largura_janela}x{altura_janela}+{x}+{y}")
    root.resizable(False, False)

    criar_tela_login(root)

    root.mainloop()

if __name__ == "__main__":
    main()
