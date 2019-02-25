from flask import Flask, render_template, request, redirect, session, flash

app = Flask(__name__)
# chave secreta da aplicação. É usada para criptografar dados padrões utilizado pelo flask
app.secret_key = 'flask-app'


class Jogo:
    def __init__(self, nome, categoria, console):
        self.nome = nome
        self.categoria = categoria
        self.console = console


pokemon = Jogo('Pokemon', 'Ação', 'Windows/Mac/Linux')
supermario = Jogo('Super Mario', 'Ação', 'Super Nintendo')
lista = [pokemon, supermario]


# definindo uma rota, por padrão GET
@app.route('/')
def inicio():
    # Utilizando a função render_template do flask para renderizar paginas html dinamicas(Jinja2)
    return render_template('lista.html', titulo='Jogos', jogos=lista)


@app.route('/novo')
def novo():
    # validação se o usuario esta logado na sessão
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        return redirect('/login?proxima=novo')
    return render_template('novo.html', titulo='Novo Jogo')


# Criando uma rota POST
@app.route('/criar', methods=['POST'])
def criar():
    # Recuperando os dados da requisição
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']
    jogo = Jogo(nome, categoria, console)
    lista.append(jogo)
    return redirect('/')


@app.route('/login')
def login():
    # capturando uma query string ?proxima=VALOR
    proxima = request.args.get('proxima')
    # passando para o template para onde vamos ir depois de autenticar
    return render_template('login.html', proxima=proxima)


@app.route('/autenticar', methods=['POST'])
def autenticar():
    if 'mestra' == request.form['senha']:
        # criando uma sessão. Essa sessão não é uma sessão do lado do servidor e ela é armazenada no cookie no navegador
        session['usuario_logado'] = request.form['usuario']
        # O flash é um helper para exibir uma mensagem no html
        flash(f'{request.form["usuario"]} logou com sucesso')
        # Proxima pagina
        proxima_pagina = request.form['proxima']
        return redirect(f'/{proxima_pagina}')
    else:
        flash('Não logado, tente novamente')
        return redirect('/login')


@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Usuário deslogado com sucesso')
    return redirect('/')


app.run(host='0.0.0.0', port=5000, debug=True)
