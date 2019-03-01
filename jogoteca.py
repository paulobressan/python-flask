import os
import time

import mysql.connector
from flask import (Flask, flash, redirect, render_template, request,
                   send_from_directory, session, url_for)

from dao import JogoDao, UsuarioDao
from models import Jogo, Usuario

app = Flask(__name__)
# chave secreta da aplicação. É usada para criptografar dados padrões utilizado pelo flask
app.secret_key = 'flask-app'
# Guardando variaveis de configurações no flask
app.config['MYSQL_HOST'] = "0.0.0.0"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = "root"
app.config['MYSQL_DB'] = "jogoteca"
app.config['MYSQL_PORT'] = 3306
# Caminho da pasta onde sera realizado os upload da aplicação
app.config['UPLOAD_PATH'] = \
    f'{os.path.dirname(os.path.abspath(__file__))}/uploads'

conn = mysql.connector.connect(user=app.config.get('MYSQL_USER'), passwd=app.config.get(
    'MYSQL_PASSWORD'), host=app.config.get('MYSQL_HOST'), port=app.config.get('MYSQL_PORT'), database=app.config.get('MYSQL_DB'))

jogo_dao = JogoDao(conn)
usuario_dao = UsuarioDao(conn)

# definindo uma rota, por padrão GET
@app.route('/')
def index():
    lista = jogo_dao.listar()
    # Utilizando a função render_template do flask para renderizar paginas html dinamicas(Jinja2)
    return render_template('lista.html', titulo='Jogos', jogos=lista)


@app.route('/novo')
def novo():
    # validação se o usuario esta logado na sessão
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        # utilizando o url_for para montar urls dinamicamente de acordo com o metodo
        return redirect(url_for('login', proxima=url_for('novo')))
    return render_template('novo.html', titulo='Novo Jogo')


# Criando uma rota POST
@app.route('/criar', methods=['POST'])
def criar():
    # Recuperando os dados da requisição
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']
    jogo = Jogo(nome, categoria, console)
    jogo = jogo_dao.salvar(jogo)
    # capturando uma imagem do request e salvando em uma pasta
    arquivo = request.files['arquivo']
    timestamp = time.time()
    arquivo.save(f"{app.config['UPLOAD_PATH']}/capa-{jogo.id}-{timestamp}.jpg")
    flash(f'Produto {nome} salvo com sucesso')
    return redirect(url_for('index'))

# essa rota espera um parametro inteiro
@app.route('/editar/<int:id>')
def editar(id):
    # validação se o usuario esta logado na sessão
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        # utilizando o url_for para montar urls dinamicamente de acordo com o metodo
        return redirect(url_for('login', proxima=url_for('editar')))
    jogo = jogo_dao.busca_por_id(id)
    nome_imagem = recupera_imagem(jogo.id)
    return render_template('editar.html', titulo='Editar Jogo', jogo=jogo, capa_jogo=nome_imagem)


@app.route('/atualizar', methods=['POST'])
def atualizar():
    # Recuperando os dados da requisição
    id = request.form['id']
    id = int(id) if not None else id
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']
    jogo = Jogo(nome, categoria, console, id)
    jogo = jogo_dao.salvar(jogo)
    # capturando uma imagem do request e salvando em uma pasta
    arquivo = request.files['arquivo']
    timestamp = time.time()
    # deleta arquivo existente
    deleta_arquivo(jogo.id)
    arquivo.save(f"{app.config['UPLOAD_PATH']}/capa-{jogo.id}-{timestamp}.jpg")
    flash(f'Produto {nome} atualizado com sucesso')
    return redirect(url_for('index'))


@app.route('/deletar/<int:id>')
def deletar(id):
    jogo_dao.deletar(id)
    deleta_arquivo(id)
    flash('O jogo foi removido com sucesso!')
    return redirect(url_for('index'))


@app.route('/login')
def login():
    # capturando uma query string ?proxima=VALOR
    proxima = request.args.get('proxima')
    # passando para o template para onde vamos ir depois de autenticar
    return render_template('login.html', proxima=proxima)


@app.route('/autenticar', methods=['POST'])
def autenticar():
    usuario = usuario_dao.buscar_por_id(request.form['usuario'])
    if usuario:
        if usuario.senha == request.form['senha']:
            # criando uma sessão. Essa sessão não é uma sessão do lado do servidor e ela é armazenada no cookie no navegador
            session['usuario_logado'] = usuario.id
            # O flash é um helper para exibir uma mensagem no html
            flash(f'{usuario.nome} logou com sucesso!')
            # Proxima pagina
            proxima_pagina = request.form['proxima']
            return redirect(proxima_pagina)
        else:
            flash('Usuário ou senha invalidos')
            return redirect(url_for('login'))
    else:
        flash('Não logado, tente novamente')
        return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Usuário deslogado com sucesso')
    return redirect(url_for('index'))


@app.route('/uploads/<nome_arquivo>')
def imagem(nome_arquivo):
    return send_from_directory('uploads', nome_arquivo)


def recupera_imagem(id):
    for nome_arquivo in os.listdir(app.config['UPLOAD_PATH']):
        if f'capa-{id}' in nome_arquivo:
            return nome_arquivo


def deleta_arquivo(id):
    arquivo = recupera_imagem(id)
    os.remove(os.path.join(app.config['UPLOAD_PATH'], arquivo))


# Para debugar com vscode tem que remover o debug do run
app.run(host='0.0.0.0', port=5000, debug=True)
#app.run(host='0.0.0.0', port=5000)
