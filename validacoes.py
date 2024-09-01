# validacoes.py

import re
import bcrypt

def verificar_senha(senha_fornecida, hash_armazenado):
    return bcrypt.checkpw(senha_fornecida.encode('utf-8'), hash_armazenado.encode('utf-8'))



def validar_email(email):
    """
    Valida o formato do e-mail.
    """
    return re.match(r"[^@]+@[^@]+\.[^@]+", email) is not None

def validar_senha(senha):
    """
    Valida a senha.
    """
    # Exemplo de validação: senha deve ter pelo menos 6 caracteres
    return len(senha) >= 6
