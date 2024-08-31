import mysql.connector
import json
from contextlib import contextmanager

def carregar_configuracoes():
    """Carrega configurações do banco de dados a partir de um arquivo JSON."""
    with open('config.json', 'r') as f:
        return json.load(f)

@contextmanager
def conectar():
    """Cria e retorna uma conexão com o banco de dados."""
    config = carregar_configuracoes()
    try:
        conexao = mysql.connector.connect(
            host=config['host'],
            user=config['user'],
            password=config['password'],
            database=config['database']
        )
        yield conexao
    except mysql.connector.Error as err:
        print(f"Erro ao conectar ao banco de dados: {err}")
        raise
    finally:
        conexao.close()

def criar_tabela_usuarios():
    """Cria a tabela de usuários no banco de dados, se ainda não existir."""
    try:
        with conectar() as conexao:
            cursor = conexao.cursor()
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS Usuarios (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nome VARCHAR(100) NOT NULL,
                email VARCHAR(100) NOT NULL UNIQUE,
                senha VARCHAR(255) NOT NULL
            )
            """)
            conexao.commit()
    except mysql.connector.Error as err:
        print(f"Erro ao criar tabela de usuários: {err}")

def criar_tabela_lancamentos():
    """Cria a tabela de lançamentos no banco de dados, se ainda não existir."""
    try:
        with conectar() as conexao:
            cursor = conexao.cursor()
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS Lancamentos (
                id INT AUTO_INCREMENT PRIMARY KEY,
                valor DECIMAL(10, 2) NOT NULL,
                tipo ENUM('Entrada', 'Saída') NOT NULL,
                data_lancamento DATE NOT NULL,
                data_vencimento DATE,
                descricao TEXT NOT NULL
            )
            """)
            conexao.commit()
    except mysql.connector.Error as err:
        print(f"Erro ao criar tabela de lançamentos: {err}")

if __name__ == "__main__":
    criar_tabela_usuarios()
    criar_tabela_lancamentos()
