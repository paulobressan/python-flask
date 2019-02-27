from models import Jogo, Usuario

SQL_DELETA_JOGO = 'delete from jogo where id = %s'
SQL_JOGO_POR_ID = 'SELECT id, nome, categoria, console from jogo where id = %s'
SQL_USUARIO_POR_ID = 'SELECT id, nome, senha from usuario where id = %s'
SQL_ATUALIZA_JOGO = 'UPDATE jogo SET nome=%s, categoria=%s, console=%s where id = %s'
SQL_BUSCA_JOGOS = 'SELECT id, nome, categoria, console from jogo'
SQL_CRIA_JOGO = 'INSERT into jogo (nome, categoria, console) values (%s, %s, %s)'


class JogoDao:
    def __init__(self, conn):
        self.__conn = conn

    def salvar(self, jogo):
        cursor = self.__conn.cursor()

        if (jogo.id):
            cursor.execute(SQL_ATUALIZA_JOGO, (jogo.nome,
                                               jogo.categoria, jogo.console, jogo.id))
        else:
            cursor.execute(SQL_CRIA_JOGO, (jogo.nome,
                                           jogo.categoria, jogo.console))
            jogo.id = cursor.lastrowid
        self.__conn.commit()
        return jogo

    def listar(self):
        cursor = self.__conn.cursor(dictionary=True)
        cursor.execute(SQL_BUSCA_JOGOS)

        jogos = traduz_jogos(cursor.fetchall())
        return jogos

    def busca_por_id(self, id):
        cursor = self.__conn.cursor()
        cursor.execute(SQL_JOGO_POR_ID, (id,))
        tupla = cursor.fetchone()
        return Jogo(tupla[1], tupla[2], tupla[3], id=tupla[0])

    def deletar(self, id):
        self.__conn.cursor().execute(SQL_DELETA_JOGO, (id, ))
        self.__conn.commit()


class UsuarioDao:
    def __init__(self, db):
        self.__conn = db

    def buscar_por_id(self, id):
        # listar os resultados como dicionario
        cursor = self.__conn.cursor(dictionary=True)
        cursor.execute(SQL_USUARIO_POR_ID, (id, ))
        dados = cursor.fetchone()
        usuario = traduz_usuario(dados) if dados else None
        return usuario


def traduz_jogos(rows):
    jogos = []
    for row in rows:
        jogos.append(Jogo(row['nome'].decode(), row['categoria'].decode(),
                          row['console'].decode(), row['id']))
    return jogos


def traduz_usuario(row):
    return Usuario(row['id'].decode(), row['nome'].decode(), row['senha'].decode())
