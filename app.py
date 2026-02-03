from flask import Flask, render_template, request
import random

app = Flask(__name__)

def completar_com_luhn(prefixo_str="", tamanho=16):
    """Completa prefixo com aleatórios e calcula Luhn. Se prefixo vazio, gera do zero."""
    numero = list(prefixo_str) if prefixo_str else []
    
    if len(numero) >= tamanho:
        numero = numero[:tamanho - 1]
    
    while len(numero) < tamanho - 1:
        numero.append(str(random.randint(0, 9)))
    
    # Luhn
    soma = 0
    for i in range(len(numero)):
        digito = int(numero[-(i + 1)])
        if i % 2 == 0:
            digito *= 2
            if digito > 9:
                digito -= 9
        soma += digito
    
    verificador = (10 - (soma % 10)) % 10
    numero.append(str(verificador))
    
    numero_completo = ''.join(numero)
    formatado = ' '.join([numero_completo[i:i+4] for i in range(0, len(numero_completo), 4)])
    
    return formatado

def mes = random.randint(1, 12)
ano = random.randint(25, 30)
if 'mes' in request.form and request.form['mes'].strip():
    try:
        mes = int(request.form['mes'])
        if not 1 <= mes <= 12:
            mes = random.randint(1, 12)
    except:
        mes = random.randint(1, 12)
if 'ano' in request.form and request.form['ano'].strip():
    try:
        ano = int(request.form['ano'])
        if not 25 <= ano <= 99:
            ano = random.randint(25, 30)
    except:
        ano = random.randint(25, 30)
    }

@app.route('/', methods=['GET', 'POST'])
def home():
    cartoes = []
    bandeira_escolhida = "visa"
    prefixo_input = ""
    quantidade = 1
    
    if request.method == 'POST':
        bandeira_escolhida = request.form.get('bandeira', 'visa')
        prefixo_input = request.form.get('prefixo', '').strip().replace(" ", "")
        qtd_str = request.form.get('quantidade', '1').strip()
        
        try:
            quantidade = int(qtd_str)
            if quantidade < 1 or quantidade > 50:
                quantidade = 1
        except ValueError:
            quantidade = 1
        
        for _ in range(quantidade):
            cartao = gerar_cartao_unico(bandeira_escolhida, prefixo_input)
            cartoes.append(cartao)
    
    return render_template('index.html', 
                          cartoes=cartoes, 
                          bandeira_escolhida=bandeira_escolhida, 
                          prefixo_input=prefixo_input,
                          quantidade=quantidade)

if __name__ == '__main__':

    app.run(debug=True)
