# db.py

import mysql.connector
import json
from validacoes import verificar_senha
from openpyxl import Workbook

def exportar_lancamentos_excel(user_id):
    lancamentos = obter_lancamentos(user_id)
    
    # Criando um novo workbook e a planilha
    wb = Workbook()
    ws = wb.active
    ws.title = "Lançamentos"

    # Definir os cabeçalhos da planilha
    ws.append(["Descrição", "Valor", "Data", "Tipo"])

    # Preencher os dados da planilha com os lançamentos
    for lancamento in lancamentos:
        ws.append([lancamento['descricao'], lancamento['valor'], lancamento['data_lancamento'], lancamento['tipo']])

    # Salvar o arquivo Excel
    file_path = f"lancamentos_usuario_{user_id}.xlsx"
    wb.save(file_path)
    
    return file_path



def carregar_config():
    with open('config.json') as f:
        return json.load(f)

def conectar_banco():
    config = carregar_config()
    return mysql.connector.connect(
        host=config['host'],
        user=config['user'],
        password=config['password'],
        database=config['database']
    )

def verificar_login(email, senha_fornecida):
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute("SELECT id, primeiro_nome, senha FROM Usuarios WHERE email = %s", (email,))
    resultado = cursor.fetchone()
    conn.close()
    if resultado:
        user_id, primeiro_nome, hash_armazenado = resultado
        if verificar_senha(senha_fornecida, hash_armazenado):
            return {'id': user_id, 'primeiro_nome': primeiro_nome, 'email': email}
    return None

def salvar_usuario(primeiro_nome, ultimo_nome, data_nascimento, email, senha):
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Usuarios (primeiro_nome, ultimo_nome, data_nascimento, email, senha)
        VALUES (%s, %s, %s, %s, %s)
    """, (primeiro_nome, ultimo_nome, data_nascimento, email, senha))
    conn.commit()
    conn.close()

def obter_usuario_por_id(user_id):
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute("SELECT id, primeiro_nome, ultimo_nome, email FROM Usuarios WHERE id = %s", (user_id,))
    resultado = cursor.fetchone()
    conn.close()
    if resultado:
        return {
            'id': resultado[0],
            'primeiro_nome': resultado[1],
            'ultimo_nome': resultado[2],
            'email': resultado[3]
        }
    return None

def obter_lancamentos(user_id):
    conn = conectar_banco()
    cursor = conn.cursor()
    # Atualizamos a consulta para usar 'data_lancamento' e 'tipo', e corrigimos 'usuario_id'
    cursor.execute("""
        SELECT id, descricao, valor, data_lancamento, tipo 
        FROM Lancamentos 
        WHERE usuario_id = %s
    """, (user_id,))
    resultados = cursor.fetchall()
    conn.close()
    lancamentos = []
    for row in resultados:
        lancamentos.append({
            'id': row[0],
            'descricao': row[1],
            'valor': row[2],
            'data_lancamento': row[3].strftime('%Y-%m-%d') if row[3] else None,
            'tipo': row[4]
        })
    return lancamentos

def salvar_lancamento(user_id, descricao, valor, data_lancamento, tipo):
    conn = conectar_banco()
    cursor = conn.cursor()
    # Atualizamos a inserção para incluir 'tipo' e usar 'data_lancamento'
    cursor.execute("""
        INSERT INTO Lancamentos (usuario_id, descricao, valor, data_lancamento, tipo)
        VALUES (%s, %s, %s, %s, %s)
    """, (user_id, descricao, valor, data_lancamento, tipo))
    conn.commit()
    conn.close()

def atualizar_lancamento(lancamento_id, descricao, valor, data_lancamento, tipo):
    conn = conectar_banco()
    cursor = conn.cursor()
    # Atualizamos a consulta para incluir 'data_lancamento' e 'tipo'
    cursor.execute("""
        UPDATE Lancamentos
        SET descricao = %s, valor = %s, data_lancamento = %s, tipo = %s
        WHERE id = %s
    """, (descricao, valor, data_lancamento, tipo, lancamento_id))
    conn.commit()
    conn.close()

def excluir_lancamento(lancamento_id):
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Lancamentos WHERE id = %s", (lancamento_id,))
    conn.commit()
    conn.close()

# Função para obter um lançamento específico por ID
def obter_lancamento_por_id(lancamento_id):
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, descricao, valor, data_lancamento, tipo 
        FROM Lancamentos 
        WHERE id = %s
    """, (lancamento_id,))
    resultado = cursor.fetchone()
    conn.close()
    
    if resultado:
        return {
            'id': resultado[0],
            'descricao': resultado[1],
            'valor': resultado[2],
            'data_lancamento': resultado[3].strftime('%Y-%m-%d') if resultado[3] else None,
            'tipo': resultado[4]
        }
    return None
