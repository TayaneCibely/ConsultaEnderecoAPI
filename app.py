from flask import Flask, render_template, request
import requests
import json

app = Flask(__name__)

VIA_CEP_URL = "http://www.viacep.com.br/ws/{}/json"

def consulta_cep(cep):
    response = requests.get(VIA_CEP_URL.format(cep))
    if response.ok:
        address = json.loads(response.text)
        if address.get("erro"):
            raise ValueError("CEP inválido")
        return {
            "bairro": address.get("bairro", ""),
            "cep": address.get("cep", ""),
            "cidade": address.get("localidade", ""),
            "logradouro": address.get("logradouro", ""),
            "uf": address.get("uf", ""),
            "complemento": address.get("complemento", "")
        }
    elif response.status_code == 400:
        raise ValueError("Erro na chamada da API")

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/consulta-cep', methods=['POST'])
def consulta():
    cep = request.form['cep']
    try:
        address = consulta_cep(cep)
        return render_template('index.html', address=address)
    except ValueError as e:
        return render_template('index.html', error=str(e))

if __name__ == '__main__':
    app.run(debug=True)