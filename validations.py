import datetime
from decimal import Decimal, InvalidOperation
import re

# VALIDAR SE O VALOR É DECIMAL
def is_decimal(n):
    try:
        Decimal(n)
        return True
    except InvalidOperation:
        return False

# VALIDAR SE O VALOR É FORMATO DATA
def is_date(value):
    date_regex = re.compile(r'^\d{4}-\d{2}-\d{2}$')

    if date_regex.match(value):
        return True
    else:
        return False

# VALIDAR SE POSSUI n DÍGITOS
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
    
# VALIADR SE O VALOR EXISTE E ESTA EM FORMATO DE DATA
def validate_date(value):
    if value and is_date(value):
        return True
    else:
        return False

# VALIADR SE O VALOR EXISTE, POSSUI n DÍGITOS (virgula conta, por isso tem que ser um a mais) E É DECIMAL
def validate_price(value, n):
    if value and number_length(value, n) and is_decimal(value):
        return True
    else:
        return False
    
# VALIDAR SE O VALOR SE ENCONTRA DENTRO DE UMA LISTA
def is_in_list(value, list):
    if value and value in list:
        return True
    else:
        return False
    
# VALIDAR SE O VALOR É UM DÍGITO, SE EXISTE E SE É MAIOR QUE ZERO
def validate_id(value):
    if value and value.isdigit() and int(value) > 0:
        return True
    else:
        return False
    
# VALIDAR SE VALOR NUMÉRICO, SE EXISTE E SE POSSUI n DÍGITOS
def validate_patrimony(value, n):
    if value and number_length(value, n) and value.isnumeric():
        return True
    else:
        return False

