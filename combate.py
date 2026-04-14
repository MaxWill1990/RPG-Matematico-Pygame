import random


def gerar_pergunta(is_boss=False):
    if is_boss:
        operacoes = ['+', '-', '*']
        num1 = random.randint(10, 50)
        num2 = random.randint(5, 20)
    else:
        operacoes = ['+', '-']
        num1 = random.choice([random.randint(1, 10), random.randint(20, 50)])
        num2 = random.choice([random.randint(1, 10), random.randint(20, 50)])

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

    return pergunta_texto, str(resultado)


def gerar_pergunta_super():
    # A conta do Super Combo agora tem 3 números (Mais justa e divertida!)
    num1 = random.randint(10, 50)
    num2 = random.randint(10, 50)
    num3 = random.randint(10, 50)

    # Sorteia se vai ser tudo soma, ou soma e subtração
    if random.choice([True, False]):
        resultado = num1 + num2 + num3
        pergunta_texto = f"{num1} + {num2} + {num3}"
    else:
        resultado = num1 + num2 - num3
        pergunta_texto = f"{num1} + {num2} - {num3}"

    return pergunta_texto, str(resultado)