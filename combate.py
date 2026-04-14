import random


def gerar_pergunta(is_boss=False):
    if is_boss:
        operacoes = ['+', '-']
        num1 = random.randint(20, 100)
        num2 = random.randint(1, 50)
    else:
        operacoes = ['+', '-', '/']
        num1 = random.choice([random.randint(1, 10), random.randint(20, 50)])
        num2 = random.choice([random.randint(1, 10), random.randint(20, 50)])
        if random.random() < 0.3:  # 30% chance of division
            operacoes = ['/']
            num1 = num2 * random.randint(1, 10)

    operador = random.choice(operacoes)

    if operador == '-' and num2 > num1:
        num1, num2 = num2, num1

    pergunta_texto = f"{num1} {operador} {num2}"

    resultado = 0
    if operador == '+':
        resultado = num1 + num2
    elif operador == '-':
        resultado = num1 - num2
    elif operador == '*':
        resultado = num1 * num2
    elif operador == '/':
        resultado = num1 // num2

    return pergunta_texto, str(resultado)


def gerar_pergunta_super():
    # Conta mais elaborada com pelo menos 2 dígitos
    num1 = random.randint(20, 99)
    num2 = random.randint(20, 99)
    num3 = random.randint(10, 50)

    # Sorteia variações
    tipo = random.choice(['+++', '++-', '+-+', '++*'])
    if tipo == '+++':
        resultado = num1 + num2 + num3
        pergunta_texto = f"{num1} + {num2} + {num3}"
    elif tipo == '++-':
        resultado = num1 + num2 - num3
        pergunta_texto = f"{num1} + {num2} - {num3}"
    elif tipo == '+-+':
        resultado = num1 - num2 + num3
        pergunta_texto = f"{num1} - {num2} + {num3}"
    elif tipo == '++*':
        resultado = num1 + num2 * num3
        pergunta_texto = f"{num1} + {num2} * {num3}"

    return pergunta_texto, str(resultado)