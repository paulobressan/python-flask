from flask import Flask, render_template, request, redirect

app = Flask(__name__)


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


app.run(host='0.0.0.0', port=8080, debug=True)
