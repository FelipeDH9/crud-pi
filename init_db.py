import mysql.connector #Importa o conector mySQL para o python
from mysql.connector import Error #Importa o módulo de erro do mySQL


def criarBD(host, usuario, senha, DB):
    # verificando se o banco de dados já existe
    try:
        connection=mysql.connector.connect( #Informando dados de conexão
            host = host, #ip do servidor do banco de dados
            user = usuario, #usuário cadastrado no MySQL
            password = senha, #Senha do usuário cadastrado no MySQL
            database = DB #Nome do database utilizado
        )
        return True
    except Error as err:
        pass
    connection=mysql.connector.connect( #Informando dados de conexão
            host = host, #ip do servidor do banco de dados
            user = usuario, #usuário cadastrado no MySQL
            password = senha, #Senha do usuário cadastrado no MySQL
        )
    cursor = connection.cursor() #Cursor para comunicação com o banco
    cursor.execute("CREATE DATABASE "+ DB) #Executa o comando SQL
    cursor.close() #Fecha o cursor
    connection.close() #Fecha a conexão
    return False




def conectarBD (host, usuario, senha, DB):
    try:
        connection=mysql.connector.connect( #Informando dados de conexão
            host = host, #ip do servidor do banco de dados
            user = usuario, #usuário cadastrado no MySQL
            password = senha, #Senha do usuário cadastrado no MySQL
            database = DB #Nome do database utilizado
        )
        return connection
    except Error:
        pass


# def read_BD(conn):
#     connection = conn #Recebe a conexão estabelecida com o banco
#     cursor = connection.cursor() #Cursor para comunicação com o banco

#     #Realizando um select para mostrar todas as linhas e colunas da tabela
#     cursor.execute("SELECT * FROM CLIENTE") #Executa o comando SQL
#     results = cursor.fetchall() #Obtendo todas as linhas geradas pelo select
#     cursor.close() #Fecha o cursor
#     connection.close() #Fecha a conexão com o banco

#     for result in results: #Percorrer a lista com as linhas geradas pelo SELECT
#         print(result) #Imprime cada linha gerada pelo SELECT

#  INSERIR DADOS NO BANCO DE DADOS
# def insertBD(nome, rg, cpf, endereco,cidade,uf,conn):
#     connection = conn #Recebe a conexão estabelecida com o banco
#     cursor = connection.cursor() #Cursor para comunicação com o banco

#     sql = "INSERT INTO CLIENTE (nome, rg,cpf,endereco,cidade,uf) VALUES(%s,%s,%s,%s,%s,%s)"
#     data = (
#         nome,
#         rg,
#         cpf,
#         endereco,
#         cidade,
#         uf
#     )
#     cursor.execute(sql,data) #Executa o comando SQL
#     connection.commit() #Efetua as modificações na tabela

#     cliente_id = cursor.lastrowid #Obter o último ID cadastrado
#     cursor.close() #Fecha o cursor
#     connection.close() #Fecha a conexão
#     print("Foi cadastrado o novo cliente de ID ",cliente_id)


# FUNÇÃO BASE QUE CRIA A TABELA DE ACORDO COM O ARGUMENTO PASSADO
def criarTabela(host, usuario, senha, DB, tabela):
    connection=conectarBD (host, usuario, senha, DB)
    cursor = connection.cursor() #Cursor para comunicação com o banco
    
    if tabela == 'hardwares':
        cursor.execute(f'''CREATE TABLE IF NOT EXISTS {tabela} (
            id INT auto_increment primary key,
            patrimonio varchar(6) NOT NULL,
            descricao varchar(45) NOT NULL,
            dt_compra DATE NOT NULL, 
            dt_pr_rev DATE NOT NULL, 
            valor_inicial DECIMAL(7,2) NOT NULL, 
            departamento varchar(45) NOT NULL
            )
            ''')
        
    elif tabela == 'softwares':
        cursor.execute(f'''CREATE TABLE IF NOT EXISTS {tabela} (
            id INT auto_increment primary key,
            nome varchar(45) NOT NULL,
            chave_licenca varchar(45) NOT NULL,
            descricao varchar(45) NOT NULL,
            dt_compra DATE NOT NULL, 
            dt_pr_rev DATE NOT NULL, 
            valor_inicial DECIMAL(7,2) NOT NULL, 
            hardwares_id INT NOT NULL,
            FOREIGN KEY (hardwares_id) REFERENCES hardwares (id)
            )
            ''')
        
    elif tabela == 'revisoes_hardware':
        cursor.execute(f'''CREATE TABLE IF NOT EXISTS {tabela} (
                id INT auto_increment primary key,
                data DATE NOT NULL, 
                valor DECIMAL(7,2) NOT NULL, 
                tipo_revisao VARCHAR(45) NOT NULL,
                infos_adicionais VARCHAR(45),
                hardwares_id INT NOT NULL,
                FOREIGN KEY (hardwares_id) REFERENCES hardwares (id)
                )
                ''')
        
        
    elif tabela == 'revisoes_software':
        cursor.execute(f'''CREATE TABLE IF NOT EXISTS {tabela} (
                id INT auto_increment primary key,
                data DATE NOT NULL, 
                valor DECIMAL(7,2) NOT NULL, 
                tipo_revisao VARCHAR(45) NOT NULL,
                infos_adicionais VARCHAR(45),
                softwares_id INT NOT NULL,
                FOREIGN KEY (softwares_id) REFERENCES softwares (id)
                )
                ''')

    else:
        pass
    cursor.close() #Fecha o cursor
    connection.close() #Fecha a conexão
    print(f"Tabela {tabela} com sucesso!")



def main():
    # se a db não estiver criada, é criada e entra no if para criar todas as tabelas
    if not criarBD("localhost","root", "root", "empresa"):
        criarTabela("localhost", "root", "root", "empresa", "hardwares")
        criarTabela("localhost", "root", "root", "empresa", "softwares")
        criarTabela("localhost", "root", "root", "empresa", "revisoes_hardware")
        criarTabela("localhost", "root", "root", "empresa", "revisoes_software")

    else:
        print("DB e todas as tabelas já existem!")

main()
        