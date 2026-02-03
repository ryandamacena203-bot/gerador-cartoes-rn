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

def gerar_cartao_unico(bandeira, prefixo_input=""):
    tamanho = 15 if bandeira == "amex" else 16
    cvv = random.randint(1000, 9999) if bandeira == "amex" else random.randint(100, 999)
    
    if prefixo_input and prefixo_input.isdigit():
        numero = completar_com_luhn(prefixo_input, tamanho)
    else:
        prefixos = {
            "visa": "4",
            "mastercard": random.choice(["51","52","53","54","55"]),
            "amex": random.choice(["34","37"]),
            "elo": random.choice(["4011","431274","438935","451416","457393","457631","504175","506699","506778","509000","636368"]),
            "hipercard": random.choice(["38","60"]),
        }
        prefixo_base = prefixos.get(bandeira, "4")
        numero = completar_com_luhn(prefixo_base, tamanho)
    
    mes = random.randint(1, 12)
    ano = random.randint(25, 30)
    
    return {
        "bandeira": bandeira.upper(),
        "numero": numero,
        "validade": f"{mes:02d}/{ano:02d}",
        "cvv": cvv
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