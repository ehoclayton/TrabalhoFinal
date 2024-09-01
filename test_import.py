# test_import.py
import sys
import os

# Adicione o diretório atual ao caminho do módulo
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    import tela_de_login
    print("Módulo 'tela_de_login' importado com sucesso!")
except ModuleNotFoundError as e:
    print(f"Erro ao importar o módulo 'tela_de_login': {e}")
