# app.py

from flask import Flask, render_template, request, redirect, url_for, flash, session
import bcrypt
from db import (
    verificar_login,
    salvar_usuario,
    obter_usuario_por_id,
    obter_lancamentos,
    salvar_lancamento,
    atualizar_lancamento,
    excluir_lancamento
)
from validacoes import validar_email, validar_senha
import json

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta_aqui'  # Substitua por uma chave secreta real e segura

# Carregar configurações
def carregar_configuracao():
    try:
        with open("config.json") as config_file:
            config = json.load(config_file)
            return config
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Erro ao carregar configuração: {e}")
        return None

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        
        usuario = verificar_login(email, senha)
        if usuario:
            session['user_id'] = usuario['id']
            session['primeiro_nome'] = usuario['primeiro_nome']
            flash('Login bem-sucedido!', 'success')
            return redirect(url_for('perfil'))
        else:
            flash('E-mail ou senha incorretos.', 'danger')
    
    return render_template('login.html')

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        primeiro_nome = request.form['primeiro_nome']
        ultimo_nome = request.form['ultimo_nome']
        email = request.form['email']
        senha = request.form['senha']
        repetir_senha = request.form['repetir_senha']
        data_nascimento = request.form['data_nascimento']
        
        # Validações
        if not primeiro_nome or not ultimo_nome or not email or not senha or not repetir_senha or not data_nascimento:
            flash('Todos os campos são obrigatórios.', 'danger')
            return redirect(url_for('cadastro'))
        
        if not validar_email(email):
            flash('E-mail inválido.', 'danger')
            return redirect(url_for('cadastro'))
        
        if not validar_senha(senha):
            flash('A senha deve ter pelo menos 6 caracteres.', 'danger')
            return redirect(url_for('cadastro'))
        
        if senha != repetir_senha:
            flash('As senhas não coincidem.', 'danger')
            return redirect(url_for('cadastro'))
        
        # Criptografar a senha
        hash_senha = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        try:
            salvar_usuario(primeiro_nome, ultimo_nome, data_nascimento, email, hash_senha)
            flash('Cadastro realizado com sucesso! Faça login.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            flash(f'Erro ao cadastrar usuário: {e}', 'danger')
            return redirect(url_for('cadastro'))
    
    return render_template('cadastro.html')

@app.route('/perfil')
def perfil():
    if 'user_id' not in session:
        flash('Por favor, faça login primeiro.', 'warning')
        return redirect(url_for('login'))
    
    user = obter_usuario_por_id(session['user_id'])
    lancamentos = obter_lancamentos(session['user_id'])
    return render_template('perfil.html', user=user, lancamentos=lancamentos)

@app.route('/lancamentos', methods=['GET', 'POST'])
def lancamentos():
    if 'user_id' not in session:
        flash('Por favor, faça login primeiro.', 'warning')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        descricao = request.form['descricao']
        valor = request.form['valor']
        data = request.form['data']
        
        if not descricao or not valor or not data:
            flash('Todos os campos são obrigatórios.', 'danger')
            return redirect(url_for('lancamentos'))
        
        try:
            valor = float(valor)
        except ValueError:
            flash('Valor inválido.', 'danger')
            return redirect(url_for('lancamentos'))
        
        try:
            salvar_lancamento(session['user_id'], descricao, valor, data)
            flash('Lançamento salvo com sucesso!', 'success')
            return redirect(url_for('perfil'))
        except Exception as e:
            flash(f'Erro ao salvar lançamento: {e}', 'danger')
            return redirect(url_for('lancamentos'))
    
    return render_template('lancamentos.html')

@app.route('/editar_lancamento/<int:lancamento_id>', methods=['GET', 'POST'])
def editar_lancamento(lancamento_id):
    if 'user_id' not in session:
        flash('Por favor, faça login primeiro.', 'warning')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        descricao = request.form['descricao']
        valor = request.form['valor']
        data = request.form['data']
        
        if not descricao or not valor or not data:
            flash('Todos os campos são obrigatórios.', 'danger')
            return redirect(url_for('editar_lancamento', lancamento_id=lancamento_id))
        
        try:
            valor = float(valor)
        except ValueError:
            flash('Valor inválido.', 'danger')
            return redirect(url_for('editar_lancamento', lancamento_id=lancamento_id))
        
        try:
            atualizar_lancamento(lancamento_id, descricao, valor, data)
            flash('Lançamento atualizado com sucesso!', 'success')
            return redirect(url_for('perfil'))
        except Exception as e:
            flash(f'Erro ao atualizar lançamento: {e}', 'danger')
            return redirect(url_for('editar_lancamento', lancamento_id=lancamento_id))
    
    # Obter detalhes do lançamento para exibir no formulário
    lancamentos = obter_lancamentos(session['user_id'])
    lancamento = next((l for l in lancamentos if l['id'] == lancamento_id), None)
    
    if not lancamento:
        flash('Lançamento não encontrado.', 'danger')
        return redirect(url_for('perfil'))
    
    return render_template('editar_lancamento.html', lancamento=lancamento)

@app.route('/excluir_lancamento/<int:lancamento_id>', methods=['POST'])
def excluir_lancamento_route(lancamento_id):
    if 'user_id' not in session:
        flash('Por favor, faça login primeiro.', 'warning')
        return redirect(url_for('login'))
    
    try:
        excluir_lancamento(lancamento_id)
        flash('Lançamento excluído com sucesso!', 'success')
    except Exception as e:
        flash(f'Erro ao excluir lançamento: {e}', 'danger')
    
    return redirect(url_for('perfil'))

@app.route('/logout')
def logout():
    session.clear()
    flash('Você foi deslogado com sucesso.', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
