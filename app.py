from flask import Flask, request, render_template, redirect, flash, url_for
from decimal import Decimal, InvalidOperation
import re
from init_db import conectarBD

app = Flask(__name__)

app.config['SECRET_KEY'] = 'fuabsnfouasbf0384h230br23082308328rftb32i230trg32t3gb20tg23tb'


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
    number_length = len(number_str)
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
        if not price or not number_length(price, 8):
            flash("Preço inicial do ativo deve ser um número decimal positivo com no máximo 7 dígitos!", "warning")
            return render_template("add_hardware.html", departments=DEPARTMENTS_LIST)


        #  VALIDAR SE O department ESTA DENTRO DA LISTA DE DEPARTAMENTOS DEFINIDA
        if department not in DEPARTMENTS_LIST or not department:
            flash("Departamento não encontrado", "danger")
            return redirect("/add_hardware")
    
        # COMO TODAS AS VALIDAÇÕES FORAM FEITAS E O ATIVO ESTÁ APTO, BASTA INSERIR NO BANCO DE DADOS
        connection = conectarBD("localhost", "root", "root", "empresa")
        cursor = connection.cursor() 
        sql = "INSERT INTO hardwares (patrimonio, descricao, dt_compra, dt_pr_rev, valor_inicial, departamento) VALUES (%s, %s, %s, %s, %s, %s)"
        data = (patrimony, description, dt_buy, dt_pr_rev, price, department)
        cursor.execute(sql,data) 
        connection.commit() 
        cursor.close() 
        connection.close()
        
        flash(f"Ativo {patrimony} adicionado!", "success")
        return redirect("/add_hardware")

    else: #GET
        return render_template("add_hardware.html", departments=DEPARTMENTS_LIST)
    
# TODO
@app.route("/add_software", methods=["POST","GET"])
def add_software():
    if request.method == "POST":
        key = request.form.get("key").strip()
        name = request.form.get("name").title().strip()
        description = request.form.get("description").title().strip()
        dt_buy = request.form.get("dt_buy")
        dt_pr_rev = request.form.get("dt_pr_rev")
        price = request.form.get("price")
        hardware_id = request.form.get("hardware_id")

        if not key:
            flash("Digite a chave de lincença!", "warning")
            return redirect("/add_software")
        
        if not name:
            flash("Digite o nome do software!", "warning")
            return redirect("/add_software")
        
        if not description:
            flash("Digite uma breve descrição do software!", "warning")
            return redirect("/add_software")
        
        # VALIDAR SE A dt_buy EXISTE E SE ESTÁ NO FORMATO DE DATA
        if not dt_buy or not is_date(dt_buy):
            flash("Informe a data de compra do ativo!", "warning")
            return render_template("add_software.html", departments=DEPARTMENTS_LIST)

        # VALIDAR SE A dt_pr_rev EXISTE E SE ESTÁ NO FORMATO DE DATA
        elif not dt_pr_rev or not is_date(dt_pr_rev):
            flash("Informe a próxima data de revisão do ativo!", "warning")
            return render_template("add_software.html", departments=DEPARTMENTS_LIST)
        
        # VALIDAR SE dt_buy É DIFERENTE DE dt_pr_rev
        elif dt_buy == dt_pr_rev:
            flash("As datas de compra e revisão devem ser diferentes!", "warning")
            return render_template("add_software.html", departments=DEPARTMENTS_LIST)

        # VALIDAR SE dt_buy É MENOR QUE dt_pr_rev
        elif dt_buy > dt_pr_rev:
            flash("A data da próxima revisão deve ser maior que a data de compra do ativo!", "warning")
            return render_template("add_software.html", departments=DEPARTMENTS_LIST)
        
        #  VALIDAR SE O price POSSUI 7 DIGITOS NUMERICOS, SE É UM float E SE EXISTE
        if not price or not number_length(price, 8):
            flash("Preço inicial do ativo deve ser um número decimal positivo com no máximo 7 dígitos!", "warning")
            return render_template("add_hardware.html", departments=DEPARTMENTS_LIST)


        # VALIDAR SE O hardware ESCOLHIDO EXISTE NO DB
        connection = conectarBD("localhost", "root", "root", "empresa")
        cursor = connection.cursor() 
        cursor.execute("SELECT id, patrimonio FROM hardwares ORDER BY patrimonio") 
        results = cursor.fetchall() 
        cursor.close() 
        connection.close()
    
        hardware_id_list = []

        for result in results:
            hardware_id_list.append(result[0])

        if not hardware_id or int(hardware_id) not in hardware_id_list:
            return render_template("mes.html", mes='nao encontrado')

    
        # INSERIR O SOFTWARE NO DB, JÁ QUE ELE PASSOU EM TODAS AS VALIDAÇÕES
        connection = conectarBD("localhost", "root", "root", "empresa")
        cursor = connection.cursor()
        sql = "INSERT INTO softwares (nome, chave_licenca, descricao, dt_compra, dt_pr_rev, valor_inicial, hardwares_id) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        data = (name, key, description, dt_buy, dt_pr_rev, price, hardware_id)
        cursor.execute(sql,data)
        connection.commit()
        cursor.close() 
        connection.close() 

        flash(f"Software {name} adicionado!", "success")
        return redirect("/add_software")

    else: #GET
        # ler DB e achar todos os patrimonios, e enviar essa lista para a página de adicionar softwares
        connection = conectarBD("localhost", "root", "root", "empresa")
        cursor = connection.cursor() 

        cursor.execute("SELECT id, patrimonio FROM hardwares ORDER BY patrimonio") 
        hardwares = cursor.fetchall() 
        cursor.close()     
        connection.close() 
        return render_template("add_software.html", hardwares=hardwares)


if __name__ =='__main__':
    app.run()