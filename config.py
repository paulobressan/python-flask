import os


# chave secreta da aplicação. É usada para criptografar dados padrões utilizado pelo flask
SECRET_KEY = 'flask-app'
# Guardando variaveis de configurações no flask
MYSQL_HOST = "0.0.0.0"
MYSQL_USER = "root"
MYSQL_PASSWORD = "root"
MYSQL_DB = "jogoteca"
MYSQL_PORT = 3306
# Caminho da pasta onde sera realizado os upload da aplicação
UPLOAD_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
