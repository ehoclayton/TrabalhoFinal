import pandas as pd
from io import BytesIO
from flask import Flask, render_template, request, redirect, url_for, flash, session, send_file
from db import (
    verificar_login,
    salvar_usuario,
    obter_usuario_por_id,
    obter_lancamentos,
    salvar_lancamento,
    atualizar_lancamento,
    excluir_lancamento,
    obter_lancamento_por_id,  # Função já definida para buscar o lançamento por ID
    exportar_lancamentos_excel
)
from validacoes import validar_email, validar_senha
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Chave secreta para a sessão

@app.route('/perfil')
def perfil():
    if 'user_id' not in session:
        flash('Por favor, faça login primeiro.', 'warning')
        return redirect(url_for('login'))
    
    user = obter_usuario_por_id(session['user_id'])
    lancamentos = obter_lancamentos(session['user_id'])
    return render_template('perfil.html', user=user, lancamentos=lancamentos)

@app.route('/exportar_relatorio_excel', methods=['POST'])
def exportar_relatorio_excel_route():
    # Obtenha o user_id da sessão (se disponível)
    user_id = session.get('user_id')
    if not user_id:
        flash("Você precisa estar logado para exportar o relatório.", "danger")
        return redirect(url_for('login'))  # Substitua 'login' pela rota de login da sua aplicação
    
    # Obtenha os lançamentos do usuário
    lancamentos = obter_lancamentos(user_id)  # Use sua função para pegar os lançamentos do usuário

    # Converta os lançamentos em um DataFrame
    df = pd.DataFrame(lancamentos)

    # Verifique as colunas do DataFrame para entender sua estrutura
    print(f"Colunas do DataFrame: {df.columns.tolist()}")  # Exibe as colunas para depuração

    # Aqui, se seu DataFrame tem 5 colunas, ajuste os nomes para 5 colunas
    if len(df.columns) == 5:
        df.columns = ['id', 'usuario_id', 'descricao', 'valor', 'data_lancamento']
    elif len(df.columns) == 4:  # Caso o DataFrame tenha 4 colunas
        df.columns = ['descricao', 'valor', 'data_lancamento', 'tipo']
    else:
        flash("O número de colunas no DataFrame está incorreto.", "danger")
        return redirect(url_for('home'))  # Redirecionar para uma página de erro ou outra página de sua escolha

    # Renomeando para a estrutura de Excel (ajuste conforme necessário)
    df = df.rename(columns={
        'descricao': 'Descrição',
        'valor': 'Valor',
        'data_lancamento': 'Data',
        'tipo': 'Tipo'
    })

    # Crie o arquivo Excel em memória
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:       
        df.to_excel(writer, index=False, sheet_name='Lançamentos')

    output.seek(0)

    # Retorne o arquivo Excel como resposta para download
    return send_file(output, as_attachment=True, download_name="relatorio_lancamentos.xlsx", mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

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

@app.route('/lancamentos', methods=['GET', 'POST'])
def lancamentos():
    if 'user_id' not in session:
        flash('Por favor, faça login primeiro.', 'warning')
        return redirect(url_for('login'))
    
    user = obter_usuario_por_id(session['user_id'])  # Obter as informações do usuário
    if request.method == 'POST':
        descricao = request.form['descricao']
        valor = request.form['valor']
        data_lancamento = request.form['data_lancamento']
        tipo = request.form['tipo']
        
        if not descricao or not valor or not data_lancamento or not tipo:
            flash('Todos os campos são obrigatórios.', 'danger')
            return redirect(url_for('lancamentos'))
        
        try:
            valor = float(valor)
        except ValueError:
            flash('Valor inválido.', 'danger')
            return redirect(url_for('lancamentos'))
        
        try:
            salvar_lancamento(session['user_id'], descricao, valor, data_lancamento, tipo)
            flash('Lançamento salvo com sucesso!', 'success')
            return redirect(url_for('perfil'))
        except Exception as e:
            flash(f'Erro ao salvar lançamento: {e}', 'danger')
            return redirect(url_for('lancamentos'))
    
    return render_template('lancamentos.html', user=user)  # Passar 'user' para o template

@app.route('/editar_lancamento/<int:id>', methods=['GET', 'POST'])
def editar_lancamento(id):
    if 'user_id' not in session:
        flash('Por favor, faça login primeiro.', 'warning')
        return redirect(url_for('login'))
    
    user = obter_usuario_por_id(session['user_id'])
    lancamento = obter_lancamento_por_id(id)
    
    if request.method == 'POST':
        descricao = request.form['descricao']
        valor = request.form['valor']
        data_lancamento = request.form['data_lancamento']
        tipo = request.form['tipo']
        
        if not descricao or not valor or not data_lancamento or not tipo:
            flash('Todos os campos são obrigatórios.', 'danger')
            return redirect(url_for('editar_lancamento', id=id))
        
        try:
            valor = float(valor)
        except ValueError:
            flash('Valor inválido.', 'danger')
            return redirect(url_for('editar_lancamento', id=id))
        
        try:
            atualizar_lancamento(id, descricao, valor, data_lancamento, tipo)
            flash('Lançamento atualizado com sucesso!', 'success')
            return redirect(url_for('perfil'))
        except Exception as e:
            flash(f'Erro ao atualizar lançamento: {e}', 'danger')
            return redirect(url_for('editar_lancamento', id=id))
    
    return render_template('editar_lancamento.html', lancamento=lancamento, user=user)

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
    flash('Você foi desconectado.', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
