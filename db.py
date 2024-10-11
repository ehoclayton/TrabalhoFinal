# db.py

import mysql.connector
import json
from validacoes import verificar_senha

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
    cursor.execute("SELECT id, descricao, valor, data FROM Lancamentos WHERE user_id = %s", (user_id,))
    resultados = cursor.fetchall()
    conn.close()
    lancamentos = []
    for row in resultados:
        lancamentos.append({
            'id': row[0],
            'descricao': row[1],
            'valor': row[2],
            'data': row[3].strftime('%Y-%m-%d')
        })
    return lancamentos

def salvar_lancamento(user_id, descricao, valor, data):
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Lancamentos (user_id, descricao, valor, data)
        VALUES (%s, %s, %s, %s)
    """, (user_id, descricao, valor, data))
    conn.commit()
    conn.close()

def atualizar_lancamento(lancamento_id, descricao, valor, data):
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE Lancamentos
        SET descricao = %s, valor = %s, data = %s
        WHERE id = %s
    """, (descricao, valor, data, lancamento_id))
    conn.commit()
    conn.close()

def excluir_lancamento(lancamento_id):
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Lancamentos WHERE id = %s", (lancamento_id,))
    conn.commit()
    conn.close()
