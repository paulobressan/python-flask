import os

import mysql.connector
from flask import Flask

app = Flask(__name__)
# Importando arquivo de configuração
app.config.from_pyfile('config.py')
# Configuração do banco
conn = mysql.connector.connect(user=app.config.get('MYSQL_USER'), passwd=app.config.get(
    'MYSQL_PASSWORD'), host=app.config.get('MYSQL_HOST'), port=app.config.get('MYSQL_PORT'), database=app.config.get('MYSQL_DB'))

# Inserindo contexto de views antes de rodar o servidor
from views import *
# O servidor vai ser executado somente na execução do arquivo jogoteca
if __name__ == '__main__':
    # Para debugar com vscode tem que remover o debug do run
    app.run(host='0.0.0.0', port=5000, debug=True)
    #app.run(host='0.0.0.0', port=5000)
