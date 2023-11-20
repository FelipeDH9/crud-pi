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


# FUNÇÃO PARA CONECTAR AO BANCO DE DADOS
def conectarBD(host, usuario, senha, DB):
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
        ON DELETE CASCADE
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
            ON DELETE CASCADE
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
            ON DELETE CASCADE
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
        