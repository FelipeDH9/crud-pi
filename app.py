from flask import Flask, request, render_template, redirect, flash, url_for
from decimal import Decimal, InvalidOperation
import re
from init_db import conectarBD

app = Flask(__name__)

app.config['SECRET_KEY'] = 'fuabsnfouasbf0384h230br23082308328rftb32i230trg32t3gb20tg23tb'

# lista de departamentos da empresa
# DEPARTMENTS = [
#     {"codigo": "AC", "nome": "Atendimento ao Cliente"},
#     {"codigo": "CT", "nome": "Contabilidade"},
#     {"codigo": "FN", "nome": "Finanças"},
#     {"codigo": "MK", "nome": "Marketing"},
#     {"codigo": "RE", "nome": "Relações Empresariais"},
#     {"codigo": "RH", "nome": "Recursos Humanos"},
#     {"codigo": "RS", "nome": "Reserva"},
#     {"codigo": "SR", "nome": "Sala de Reuniões"},
#     {"codigo": "TI", "nome": "TI da empresa"},
#     {"codigo": "VN", "nome": "Vendas"},
# ]

# DEPARTMENTS = [
#     {"id": "1", "nome": "Atendimento ao Cliente"},
#     {"id": "2", "nome": "Contabilidade"},
#     {"id": "3", "nome": "Finanças"},
#     {"id": "4", "nome": "Marketing"},
#     {"id": "5", "nome": "Relações Empresariais"},
#     {"id": "6", "nome": "Recursos Humanos"},
#     {"id": "7", "nome": "Reserva"},
#     {"id": "8", "nome": "Sala de Reuniões"},
#     {"id": "9", "nome": "TI da empresa"},
#     {"id": "10", "nome": "Vendas"},
# ]

def is_decimal(n):
    try:
        Decimal(n)
        return True
    except InvalidOperation:
        return False


def is_date(value):
    date_regex = re.compile(r'^\d{4}-\d{2}-\d{2}$')

    if date_regex.match(value):
        return True
    else:
        return False


def number_length(number, n):
    # converte o numero em string
    number_str = str(number)
    # encontra o tamanho da string e subtrai 1 para desconsiderar o ponto decimal
    number_length = len(number_str) - 1
    # se o tamanho for maior que n ou menor ou igual que 0, então retorna false
    if number_length > n or number_length <= 0:
        return False
    else:
        return True 


DEPARTMENTS_LIST = [
    "Atendimento ao Cliente",
    "Contabilidade",
    "Finanças",
    "Marketing",
    "Relações Empresariais",
    "Recursos Humanos",
    "Reserva",
    "Sala de Reuniões",
    "TI",
    "Vendas",
]

REVISOES_HARDWARE = [
    'Manutenção',
    'Limpeza',
    'Movimentação',
    'Obsolescência'
]

REVISOES_SOFTWARE = [
    'Controle de Licença',
    'Migração para outra máquina'
]


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/add_hardware", methods=["POST","GET"])
def add_hardware():
    if request.method == "POST":
        patrimony = request.form.get("patrimony").strip()
        description = request.form.get("description").title().strip()
        dt_buy = request.form.get("dt_buy")
        dt_pr_rev = request.form.get("dt_pr_rev")
        price = request.form.get("price")
        department = request.form.get("department")
        

        # VALIDAR SE patrimony EXISTE, POSSUI 6 DIGITOS NUMERICOS
        if not patrimony or not number_length(patrimony, 6):
            flash("Patrimonio deve conter seis dígitos numéricos!", "warning")
            return render_template("add_hardware.html", departments=DEPARTMENTS_LIST)
        

        # checar se o patrimonio já existe no banco de dados
        # ir no banco de dados e retonar todos os patrimonios cadastrados
        connection = conectarBD("localhost", "root", "root", "empresa")
        cursor = connection.cursor() #Cursor para comunicação com o banco

        #Realizando um select para mostrar todas as linhas e colunas da tabela
        cursor.execute("SELECT patrimonio FROM hardwares") #Executa o comando SQL
        all_patrimonies = cursor.fetchall() #Obtendo todas as linhas geradas pelo select
        cursor.close() #Fecha o cursor
        connection.close() #Fecha a conexão com o banco

        # patrimony_list = []
        for result in all_patrimonies:
            if patrimony == result[0]:                
                flash("Patrimonio já cadastrado!", "danger")
                return render_template("add_hardware.html", departments=DEPARTMENTS_LIST)
    
        # VALIDAR SE description EXISTE
        if not description:
            flash("Informe uma breve descrição sobre o ativo!", "warning")
            return render_template("add_hardware.html", departments=DEPARTMENTS_LIST)
            

        # VALIDAR SE A dt_buy EXISTE E SE ESTÁ NO FORMATO DE DATA
        if not dt_buy or not is_date(dt_buy):
        # if not dt_buy:
            flash("Informe a data de compra do ativo!", "warning")
            return render_template("add_hardware.html", departments=DEPARTMENTS_LIST)

        # VALIDAR SE A dt_pr_rev EXISTE E SE ESTÁ NO FORMATO DE DATA
        elif not dt_pr_rev or not is_date(dt_pr_rev):
            flash("Informe a próxima data de revisão do ativo!", "warning")
            return render_template("add_hardware.html", departments=DEPARTMENTS_LIST)
        
        # VALIDAR SE dt_buy É DIFERENTE DE dt_pr_rev
        elif dt_buy == dt_pr_rev:
            flash("As datas de compra e revisão devem ser diferentes!", "warning")
            return render_template("add_hardware.html", departments=DEPARTMENTS_LIST)

        # VALIDAR SE dt_buy É MENOR QUE dt_pr_rev
        elif dt_buy > dt_pr_rev:
            flash("A data da próxima revisão deve ser maior que a data de compra do ativo!", "warning")
            return render_template("add_hardware.html", departments=DEPARTMENTS_LIST)


        #  VALIDAR SE O price POSSUI 7 DIGITOS NUMERICOS, SE É UM float E SE EXISTE
        if not price or not number_length(price, 7):
            flash("Preço inicial do ativo deve ser um número decimal positivo com no máximo 7 dígitos!", "warning")
            return render_template("add_hardware.html", departments=DEPARTMENTS_LIST)


        #  VALIDAR SE O department ESTA DENTRO DA LISTA DE DEPARTAMENTOS DEFINIDA
        if department not in DEPARTMENTS_LIST or not department:
            flash("Departamento não encontrado", "danger")
            return redirect("/add_hardware")
    
        # COMO TODAS AS VALIDAÇÕES FORAM FEITAS E O ATIVO ESTÁ APTO, BASTA INSERIR NO BANCO DE DADOS
        connection = conectarBD("localhost", "root", "root", "empresa")
        cursor = connection.cursor() #Cursor para comunicação com o banco
        sql = "INSERT INTO hardwares (patrimonio, descricao, dt_compra, dt_pr_rev, valor_inicial, departamento) VALUES (%s, %s, %s, %s, %s, %s)"
        data = (patrimony, description, dt_buy, dt_pr_rev, price, department)
        cursor.execute(sql,data) #Executa o comando SQL
        
        connection.commit() #Efetua as modificações na tabela

        cursor.close() #Fecha o cursor
        connection.close() #Fecha a conexão
        
        
        # return render_template("mes.html", mes=f'{patrimony} foi added')
        flash(f"Ativo {patrimony} adicionado!", "success")
        return redirect("/add_hardware")

    else: #GET
        return render_template("add_hardware.html", departments=DEPARTMENTS_LIST)
    

@app.route("/add_software", methods=["POST","GET"])
def add_software():
    if request.method == "POST":
        key = request.form.get("key").title().strip()
        description = request.form.get("description").title().strip()
        dt_buy = request.form.get("dt-buy")
        dt_pr_rev = request.form.get("dt-rev")
        price = request.form.get("price")


        departamento = request.form.get("department")

        # if departamento not in DEPARTMENTS or not departamento:
        #     flash("Departamento não encontrado", "danger")
        #     return redirect("/add")
        # return render_template("mes.html", mes=f'{departamento} foi escolhido')
        # pass

    else: #GET
        return render_template("add_software.html")


if __name__ =='__main__':
    app.run()