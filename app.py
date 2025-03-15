from flask import Flask, render_template, request
import requests
import json
import time
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST, CollectorRegistry

app = Flask(__name__)

VIA_CEP_URL = "http://www.viacep.com.br/ws/{}/json"

# Criando um registrador exclusivo para evitar métricas automáticas
registry = CollectorRegistry()

# Contador de requisições ao ViaCEP
via_cep_requests_total = Counter('via_cep_requests_total', 'Total de consultas ao ViaCEP', registry=registry)

# Histograma para medir tempo de resposta das requisições ao ViaCEP
via_cep_request_duration_seconds = Histogram(
    'via_cep_request_duration_seconds', 'Duração das requisições ao ViaCEP (em segundos)',
    registry=registry,
    buckets=[0.1, 0.3, 0.5, 1, 2, 3, 5]  # Definição de intervalos para análise
)

def consulta_cep(cep):
    start_time = time.time()  # Início da contagem do tempo
    response = requests.get(VIA_CEP_URL.format(cep))
    
    duration = time.time() - start_time  # Tempo total da requisição
    via_cep_request_duration_seconds.observe(duration)  # Armazena o tempo na métrica
    
    via_cep_requests_total.inc()  # Incrementa o contador de requisições
    
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

# Expor apenas as métricas personalizadas
@app.route('/metrics')
def metrics():
    return generate_latest(registry), 200, {'Content-Type': CONTENT_TYPE_LATEST}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
