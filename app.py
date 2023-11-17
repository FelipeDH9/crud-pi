from flask import Flask, request, render_template, redirect, flash

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

DEPARTMENTS = [
    {"id": "1", "nome": "Atendimento ao Cliente"},
    {"id": "2", "nome": "Contabilidade"},
    {"id": "3", "nome": "Finanças"},
    {"id": "4", "nome": "Marketing"},
    {"id": "5", "nome": "Relações Empresariais"},
    {"id": "6", "nome": "Recursos Humanos"},
    {"id": "7", "nome": "Reserva"},
    {"id": "8", "nome": "Sala de Reuniões"},
    {"id": "9", "nome": "TI da empresa"},
    {"id": "10", "nome": "Vendas"},
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
        codigo = request.form.get("codigo").title().strip()
        descricao = request.form.get("description").title().strip()
        data_compra = request.form.get("dt-buy")
        data_rev = request.form.get("dt-rev"),
        preco = request.form.get("price")


        departamento = request.form.get("department")

        if departamento not in DEPARTMENTS or not departamento:
            flash("Departamento não encontrado", "danger")
            return redirect("/add")
        return render_template("mes.html", mes=f'{departamento} foi escolhido')
        # pass

    else: #GET
        return render_template("add_hardware.html", departments=DEPARTMENTS)
    

@app.route("/add_software", methods=["POST","GET"])
def add_software():
    if request.method == "POST":
        key = request.form.get("key").title().strip()
        description = request.form.get("description").title().strip()
        dt_buy = request.form.get("dt-buy")
        dt_rev = request.form.get("dt-rev")
        price = request.form.get("price")


        departamento = request.form.get("department")

        if departamento not in DEPARTMENTS or not departamento:
            flash("Departamento não encontrado", "danger")
            return redirect("/add")
        return render_template("mes.html", mes=f'{departamento} foi escolhido')
        # pass

    else: #GET
        return render_template("add_software.html", departments=DEPARTMENTS)


if __name__ =='__main__':
    app.run()