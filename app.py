from flask import Flask, request, render_template, redirect, flash, url_for
from decimal import Decimal, InvalidOperation
import re
from init_db import conectarBD
import datetime

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

def money_format(value):
    return f"R${value:,.2f}"


def convert_to_date(value):
    date_format = '%Y-%m-%d'
    date = datetime.datetime.strptime(value, date_format)
    return date.date()

app.jinja_env.filters["money_format"] = money_format

DEPARTMENTS_LIST = [
    "Atendimento ao Cliente",
    "Contabilidade",
    "Finanças",
    "Marketing",
    "Obsoleto",
    "Relações Empresariais",
    "Recursos Humanos",
    "Reserva",
    "Sala de Reuniões",
    "TI",
    "Vendas"
]

REVISOES_HARDWARE = [
    'Manutenção',
    'Limpeza',
    'Movimentação',
    'Mudança de departamento',
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
        description = request.form.get("description").capitalize().strip()
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
        cursor = connection.cursor() 

        #Realizando um select para mostrar todas as linhas e colunas da tabela
        cursor.execute("SELECT patrimonio FROM hardwares") #Executa o comando SQL
        all_patrimonies = cursor.fetchall() #Obtendo todas as linhas geradas pelo select
        cursor.close() #Fecha o cursor
        connection.close() #Fecha a conexão com o banco

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
        if not price or not number_length(price, 8) or not is_decimal(price):
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
    
# HARDWARES
@app.route("/all_hardwares")
def all_hardwares():
    # consultar todos os hardwares
    connection = conectarBD("localhost", "root", "root", "empresa")
    cursor = connection.cursor() 

    cursor.execute("SELECT * FROM hardwares ORDER BY patrimonio") 
    results = cursor.fetchall() 

    cursor.close()     
    connection.close() 

    # converter a lista de tuplas em uma lista de listas
    all_hardwares = list(map(list, results))


    # consultar todas as revisões dos hardwares
    connection = conectarBD("localhost", "root", "root", "empresa")
    cursor = connection.cursor()

    cursor.execute("SELECT hardwares_id, SUM(valor) FROM revisoes_hardware GROUP BY hardwares_id")
    sum_revisoes = cursor.fetchall()
    cursor.close()     
    connection.close() 


    for hardware in all_hardwares:
        hardware[5] = float(hardware[5])

    # INSERIR NA LISTA DE LISTAS DOS HARDWARES O CUSTO TOTAL DE REVISÕES DELE
    for hardware in all_hardwares:
        for sum_rev in sum_revisoes:
            if int(sum_rev[0]) == int(hardware[0]):
                hardware.append(float(sum_rev[1]))

    return render_template("all_hardwares.html", all_hardwares=all_hardwares, sum_revisoes=sum_revisoes)


@app.route("/delete_hardware", methods=["POST"])
def delete_hardware():
    hardware_id = request.form.get("hardware_id")

    # validar se o hardware_id existe, se é um digito e se é maior que 0
    if not hardware_id or not hardware_id.isdigit() or int(hardware_id) <= 0:
        flash("1 Hardware não encontrado!", "danger")
        return redirect("/all_hardwares")
    
    # validar se o hardware escolhido está no banco de dados

    connection = conectarBD("localhost", "root", "root", "empresa")
    cursor = connection.cursor() 
    cursor.execute("SELECT id FROM hardwares WHERE id = %s", (hardware_id,))
    results = cursor.fetchall()
    cursor.close()
    connection.close()


    # validar se a quantidade de tuplas de resultado da busca no banco de dados é maior que 1, ou seja, se o dado existe
    if len(results) != 1:
        flash("2 Hardware não encontrado!", "danger")
        return redirect("/all_hardwares")

    else:
        connection = conectarBD("localhost", "root", "root", "empresa")
        cursor = connection.cursor() 
        cursor.execute("DELETE FROM hardwares WHERE id = %s", (hardware_id,))
        results = cursor.fetchall()
        connection.commit()
        cursor.close()
        connection.close()

        flash("Hardware deletado", "warning")
        return redirect('/all_hardwares') 
     

@app.route("/edit_hardware", methods=["POST", "GET"])
def edit_hardware():
    if request.method == 'POST':
        hardware_id = request.form.get("hardware_id")
        description = request.form.get("description").capitalize().strip()
        dt_buy = request.form.get("dt_buy")
        dt_pr_rev = request.form.get("dt_pr_rev")
        price = request.form.get("price")
        department = request.form.get("department")

        # VALIDAR SE o ID EXISTE
        if not hardware_id or int(hardware_id) < 1:
            flash("3 Hardware não encontrado 1!", "danger")
            return redirect("/all_hardwares")
        
        
        connection = conectarBD("localhost", "root", "root", "empresa")
        cursor = connection.cursor() 

        #Realizando um select para mostrar todas as linhas e colunas da tabela
        cursor.execute("SELECT * FROM hardwares WHERE id = %s", (hardware_id,)) 
        results = cursor.fetchall() 

        counter = 0
        
        # VALIDAR SE DT_BUY EXISTE E ESTÁ EM FORMATO DATE
        if dt_buy and not is_date(dt_buy):
            cursor.close() 
            connection.close()
            flash("Data de compra inválida, ela deve ser em formato de data!", "warning")
            return redirect("/all_hardwares")

        # VALIDAR SE A DATA DE COMPRA NOVA É ANTERIOR A DATA DE REVISÃO SALVA
        elif dt_buy and convert_to_date(dt_buy) > results[0][4]:
            cursor.close() 
            connection.close()
            flash("Data de compra inválida, ela deve ser anterior a data de revisão!", "warning")
            return redirect("/all_hardwares")

        # VALIDAR SE DT_PR_REV EXISTE E ESTÁ EM FORMATO DATE
        elif dt_pr_rev and not is_date(dt_pr_rev):
            cursor.close() 
            connection.close()
            flash("Data da próxima revisão inválida, ela deve ser em formato de data!", "warning")
            return redirect("/all_hardwares")

        #  VALIDAR SE A DATA DA PRÓXIMA REVISÃO É POSTERIOR A DATA DE COMPRA SALVA
        elif dt_pr_rev and convert_to_date(dt_pr_rev) < results[0][3]:
            dt_pr_rev = convert_to_date(dt_pr_rev)
            flash("Data da próxima revisão inválida, ela deve ser posterior a data de compra!", "warning")
            return redirect("/all_hardwares")
        
        # validar se a data de compra nova existe e é anterior a data de previsão nova
        elif dt_buy and dt_buy < dt_pr_rev:
            flash("Data da próxima revisão inválida, ela deve ser posterior a data de compra!", "warning")
            return redirect("/all_hardwares")

        # validar se o valor inicital do ativo é possui 7 dígitos numéricos
        elif price and not number_length(price, 8):
            flash("Preço inicial do ativo deve ser um número decimal positivo com no máximo 7 dígitos!", "warning")
            return redirect("/all_hardwares")
        
        #  VALIDAR SE O department ESTA DENTRO DA LISTA DE DEPARTAMENTOS DEFINIDA
        elif department not in DEPARTMENTS_LIST or not department:
            flash("Departamento não encontrado", "danger")
            return redirect("/add_hardware")
        
        # SE PASSAR DE TODAS AS VALIDAÇÕES 
        else:               
            # ver se a descricao escrita é diferente da que esta no banco de dados, caso seja, então alterar e somar no contador de edições
            if description and description != results[0][2]:
                cursor.execute("UPDATE hardwares SET descricao = %s WHERE id = %s", (description, hardware_id,)) 
                counter += 1

            #  validar se a data de compra nova é diferente da salva
            if dt_buy:
                cursor.execute("UPDATE hardwares SET dt_compra = %s WHERE id = %s", (dt_buy, hardware_id,)) 
                counter += 1

            # se dt_pr_rev existe, alterar
            if dt_pr_rev:
                cursor.execute("UPDATE hardwares SET dt_pr_rev = %s WHERE id = %s", (dt_pr_rev, hardware_id,)) 
                counter += 1

            # se price existe, alterar
            if price:
                cursor.execute("UPDATE hardwares SET valor_inicial = %s WHERE id = %s", (price, hardware_id,)) 
                counter += 1

            # VALIDAÇÃO PARA VER SE DEPARTAMENTO ESTÁ NA LISTA DE DEPARTAMENTOS PADRÃO 
            if department and department != results[0][6]:
                cursor.execute("UPDATE hardwares SET departamento = %s WHERE id = %s", (department, hardware_id,)) 
                counter += 1

            connection.commit()
            cursor.close() 
            connection.close()

            if counter > 0:
                flash("Hardware editado!", "success")
                return redirect("/all_hardwares")
            else:
                flash("Nenhuma edição foi feita!", "success")
                return redirect("/all_hardwares")
        

    else: #GET
        hardware_id = request.args.get("hardware_id")

        # validar se o hardware_id existe, se é um digito e se é maior que 0
        if not hardware_id or not hardware_id.isdigit() or int(hardware_id) <= 0:
            flash("4 Hardware não encontrado!", "danger")
            return redirect("/all_hardwares")
        
        else:
        
            # validar se o hardware escolhido está no banco de dados
            connection = conectarBD("localhost", "root", "root", "empresa")
            cursor = connection.cursor() 
            cursor.execute("SELECT * FROM hardwares WHERE id = %s", (hardware_id,))
            hardware = cursor.fetchall()
            cursor.close()
            connection.close()


            # validar se a quantidade de tuplas de resultado da busca no banco de dados é maior que 1, ou seja, se o dado existe
            if len(hardware) != 1:
                flash("5 Hardware não encontrado!", "danger")
                return redirect("/all_hardwares")
            

            return render_template("edit_hardware.html", hardware=hardware, departments=DEPARTMENTS_LIST)


@app.route('/add_rev_hardware', methods=["POST","GET"])
def add_rev_hardware():
    if request.method == "POST":
        hardware_id = request.form.get("hardware_id")
        type_rev = request.form.get("type_rev")
        dt_rev = request.form.get("dt_rev")
        price = request.form.get("price")
        infos = request.form.get("infos").capitalize()
        department = request.form.get("department")  
        

        connection = conectarBD("localhost", "root", "root", "empresa")
        cursor = connection.cursor() 
        cursor.execute("SELECT * FROM hardwares WHERE id = %s", (hardware_id,)) 
        hardware = cursor.fetchall() 
        cursor.close() 
        connection.close()

        if type_rev:
            type_rev = type_rev.strip().capitalize()

        if not price:
            price = 0
        
        if not infos:
            infos = ''

        # validar se o hardware_id existe, se é um digito e se é maior que 0, e se ele existe no bando de dados
        if not hardware_id or not hardware_id.isdigit() or int(hardware_id) <= 0 or not hardware:
            flash("6 Hardware não encontrado!", "danger")
            return redirect('/all_hardwares')

        # validar se o tipo de rev está dentro da lista
        elif type_rev not in REVISOES_HARDWARE or not type_rev:
            flash("Tipo de revisão não encontrada!", "danger")
            return redirect('/all_hardwares')

        # VALIDAR SE A dt_buy EXISTE E SE ESTÁ NO FORMATO DE DATA
        elif not dt_rev or not is_date(dt_rev):
            flash("Informe a data da revisão!", "warning")
            return redirect('/all_hardwares')
        
        # verificar se dt_rev é posterior a data de compra salva no banco de dados
        elif dt_rev and convert_to_date(dt_rev) < hardware[0][3]:
            dt_rev = convert_to_date(dt_rev)
            flash("Data da revisão inválida, ela deve ser posterior a data de compra!", "warning")
            return redirect("/all_hardwares")
        
        #  VALIDAR SE O price POSSUI 7 DIGITOS NUMERICOS, SE É UM float E SE EXISTE
        elif not number_length(price, 8) or not is_decimal(price):
        # elif not price or not number_length(price, 8):
            flash("Preço da revisão deve ser um número decimal positivo com no máximo 7 dígitos!", "warning")
            return redirect('/all_hardwares')

        # validar se o tipo de rev escolhido for 'mudandça de departamento', tem que ter um valor no department
        elif type_rev == 'Mudança de departamento' and not department:
            flash("Para Mudar de departamento, é necessário informar o novo departamento!", "warning")
            return redirect('/all_hardwares')
        
        
        else:
            # inserir no banco de dados
            connection = conectarBD("localhost", "root", "root", "empresa")
            cursor = connection.cursor() 
            sql = "INSERT INTO revisoes_hardware (data, valor, tipo_revisao, infos_adicionais, hardwares_id) VALUES (%s, %s, %s, %s, %s)"
            data = (dt_rev, price, type_rev, infos, hardware_id)
            cursor.execute(sql,data) 
            connection.commit()
            cursor.close() 
            connection.close()
            
            flash(f"Ativo adicionada!", "success")
            return redirect("/all_hardwares")



    else: #GET
        hardware_id = request.args.get("hardware_id")
        
        # validar se o hardware_id existe, se é um digito e se é maior que 0
        if not hardware_id or not hardware_id.isdigit() or int(hardware_id) <= 0:
            flash("7 Hardware não encontrado!", "danger")
            return redirect("/add_rev_hardware")
        
        else:
            # validar se o hardware escolhido está no banco de dados
            connection = conectarBD("localhost", "root", "root", "empresa")
            cursor = connection.cursor() 
            cursor.execute("SELECT * FROM hardwares WHERE id = %s", (hardware_id,))
            hardware = cursor.fetchall()
            cursor.close()
            connection.close()


            # validar se a quantidade de tuplas de resultado da busca no banco de dados é maior que 1, ou seja, se o dado existe
            if len(hardware) != 1:
                flash("8 Hardware não encontrado!", "danger")
                return redirect("/add_rev_hardware")
            

            return render_template("add_rev_hardware.html", hardware=hardware,  type_revs=REVISOES_HARDWARE, departments=DEPARTMENTS_LIST)


@app.route("/all_rev_hardware")
def all_rev_hardware():
    hardware_id = request.args.get("hardware_id")
    patrimony = request.args.get("patrimony")

    # consultar todos as as revisões do hardware
    connection = conectarBD("localhost", "root", "root", "empresa")
    cursor = connection.cursor() 
    cursor.execute("SELECT * FROM revisoes_hardware WHERE hardwares_id = %s", (hardware_id,)) 
    results = cursor.fetchall()
    cursor.close()
    connection.close()

    all_revs = results

    # converter a lista de tuplas em uma lista de listas
    all_revs = list(map(list, results))

    sum_revs = 0
    for rev in all_revs:
        sum_revs += rev[2]

    return render_template("all_rev_hardware.html", all_revs=all_revs, patrimony=patrimony, type_revs=REVISOES_HARDWARE, sum_revs=sum_revs)



# SOFTWARES
# TODO
@app.route("/add_software", methods=["POST","GET"])
def add_software():
    if request.method == "POST":
        key = request.form.get("key").strip()
        name = request.form.get("name").title().strip()
        description = request.form.get("description").capitalize().strip()
        dt_buy = request.form.get("dt_buy")
        dt_pr_rev = request.form.get("dt_pr_rev")
        price = request.form.get("price")
        hardware_id = request.form.get("hardware_id")

        if not key:
            flash("Digite a chave de lincença!", "warning")
            return render_template("add_software.html", departments=DEPARTMENTS_LIST)
        
        if not name:
            flash("Digite o nome do software!", "warning")
            return render_template("add_software.html", departments=DEPARTMENTS_LIST)
        
        if not description:
            flash("Digite uma breve descrição do software!", "warning")
            return render_template("add_software.html", departments=DEPARTMENTS_LIST)
        
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


@app.route("/all_softwares", methods=["POST","GET"])
def all_softwares():
    if request.method == "POST":
        pass

    else: #GET
        connection = conectarBD("localhost", "root", "root", "empresa")
        cursor = connection.cursor() 

        cursor.execute("SELECT * FROM softwares") 
        all_softwares = cursor.fetchall() 
        cursor.close()     
        connection.close() 
        return render_template("all_softwares.html", all_softwares=all_softwares)
    

if __name__ =='__main__':
    app.run()