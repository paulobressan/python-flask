from flask import Flask, render_template, request, redirect, session, flash, url_for

app = Flask(__name__)
# chave secreta da aplicação. É usada para criptografar dados padrões utilizado pelo flask
app.secret_key = 'flask-app'


class Jogo:
    def __init__(self, id, nome, categoria, console):
        self.id = id
        self.nome = nome
        self.categoria = categoria
        self.console = console


class Usuario:
    def __init__(self, id, nome, senha):
        self.id = id
        self.nome = nome
        self.senha = senha


pokemon = Jogo('Pokemon', 'Ação', 'Windows/Mac/Linux')
supermario = Jogo('Super Mario', 'Ação', 'Super Nintendo')
lista = [pokemon, supermario]

paulo = Usuario('paulo', 'Paulo Bressan', '123')
bruna = Usuario('bruna', 'Bruna Carol', '7a1')
rita = Usuario('rita', 'Rita Bressan', 'rita')

usuarios = {paulo.id: paulo, bruna.id: bruna, rita.id: rita}

# definindo uma rota, por padrão GET
@app.route('/')
def index():
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
    lista.append(jogo)
    return redirect(url_for('index'))


@app.route('/login')
def login():
    # capturando uma query string ?proxima=VALOR
    proxima = request.args.get('proxima')
    # passando para o template para onde vamos ir depois de autenticar
    return render_template('login.html', proxima=proxima)


@app.route('/autenticar', methods=['POST'])
def autenticar():
    if request.form['usuario'] in usuarios:
        usuario = usuarios[request.form['usuario']]
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


app.run(host='0.0.0.0', port=5000, debug=True)
