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
    #Utilizando a função render_template do flask para renderizar paginas html dinamicas(Jinja2)
    return render_template('lista.html', titulo='Jogos', jogos=lista)


@app.route('/novo')
def novo():
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
    return render_template('login.html')

@app.route('/autenticar', methods=['POST'])
def autenticar():
    if 'mestra' == request.form['senha']:
        #criando uma sessão. Essa sessão não é uma sessão do lado do servidor e ela é armazenada no cookie no navegador
        session['usuario_logado'] = request.form['usuario']
        # O flash é um helper para exibir uma mensagem no html
        flash(f'{request.form["usuario"]} logou com sucesso')
        return redirect('/')
    else:
        flash('Não logado, tente novamente')
        return redirect('/login')

app.run(host='0.0.0.0', port=8080, debug=True)
