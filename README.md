# Consulta Endereço API

Aplicação em Python usando Flask como framework web, Prometheus para coleta de métricas e ViaCEP para consulta de endereços via CEP. O Flask lida com requisições de usuários, enviando o CEP ao ViaCEP, que retorna os dados do endereço. O Prometheus registra métricas como tempo de resposta e número de requisições, exibidas em tempo real no Grafana. As métricas ajudam a identificar gargalos, garantindo eficiência e desempenho.


## Tecnologias Utilizadas

### [Flask](https://flask.palletsprojects.com/en/stable/)
* Versão 2.3.2
Flask é um microframework web escrito em Python. Ele é leve, flexível e ideal para construir aplicações web e APIs de forma rápida e simples.

### [Python](https://www.python.org/)
Python é uma linguagem de programação de alto nível, conhecida por sua simplicidade e legibilidade. É amplamente usada em desenvolvimento web, automação, análise de dados e machine learning.

### [Docker](https://www.docker.com/)
Docker é uma plataforma de contêineres que permite empacotar aplicações e suas dependências em ambientes isolados e portáteis.

### [Grafana](https://grafana.com/)
Grafana é uma ferramenta de visualização de dados que permite criar dashboards interativos para monitoramento e análise de métricas.

### [Prometheus](https://prometheus.io/)
Prometheus é um sistema de monitoramento e alerta de código aberto, projetado para coletar e armazenar métricas de aplicações e infraestrutura.


## Deploy

Clone o projeto
```bash
  git clone https://github.com/TayaneCibely/ConsultaEnderecoAPI.git
```

Criar a imagem no docker

```bash
  docker-compose build
```
Subir os conteines

```bash
  docker-compose up
```

Acessar as os links 
* [Aplicação: Consulta de CEP](http://localhost:5000)
* [Phometheus](http://localhost:9090)
* [Grafana](http://localhost:3000)

Entrar no Grafana
```bash
  Usuário: admin
  Senha: admin
```
*Redefinir a senha do Grafana

Ainda no grafana click em:
```bash
  Add data source
```
Selecione:
```bash
   Prometheus
```

Insira em connection:
```bash
   http://prometheus:9090
```

Crie um novo dashboard
* +Create dashboard
* Add visualization

Selecione:
* Phometheus

Em:
```bash
   Query inspector
```

Insira esse em JSON:

```bash
   {
  "id": 1,
  "type": "timeseries",
  "title": "Monitoramento da API",
  "gridPos": {
    "x": 0,
    "y": 0,
    "h": 9,
    "w": 20
  },
  "fieldConfig": {
    "defaults": {
      "custom": {
        "drawStyle": "line",
        "lineInterpolation": "smooth",
        "barAlignment": 0,
        "barWidthFactor": 0.6,
        "lineWidth": 2,
        "fillOpacity": 10,
        "gradientMode": "opacity",
        "spanNulls": false,
        "insertNulls": false,
        "showPoints": "auto",
        "pointSize": 5,
        "stacking": {
          "mode": "none",
          "group": "A"
        },
        "axisPlacement": "auto",
        "axisLabel": "",
        "axisColorMode": "text",
        "axisBorderShow": false,
        "scaleDistribution": {
          "type": "linear"
        },
        "axisCenteredZero": false,
        "hideFrom": {
          "tooltip": false,
          "viz": false,
          "legend": false
        },
        "thresholdsStyle": {
          "mode": "off"
        }
      },
      "color": {
        "mode": "palette-classic",
        "fixedColor": "rgb(31, 120, 193)",
        "seriesBy": "last"
      },
      "mappings": [],
      "thresholds": {
        "mode": "absolute",
        "steps": [
          {
            "color": "green",
            "value": null
          },
          {
            "color": "red",
            "value": 80
          }
        ]
      },
      "unit": "short",
      "decimals": 2
    },
    "overrides": [
      {
        "matcher": {
          "id": "byName",
          "options": "Tempo de Resposta (95º percentil)"
        },
        "properties": [
          {
            "id": "color",
            "value": {
              "mode": "fixed",
              "fixedColor": "rgb(100, 150, 255)"
            }
          }
        ]
      },
      {
        "matcher": {
          "id": "byName",
          "options": "Status do Serviço"
        },
        "properties": [
          {
            "id": "color",
            "value": {
              "mode": "fixed",
              "fixedColor": "rgb(0, 50, 150)"
            }
          }
        ]
      }
    ]
  },
  "pluginVersion": "11.5.2",
  "targets": [
    {
      "refId": "A",
      "expr": "rate(via_cep_requests_total[1m])",
      "range": true,
      "instant": false,
      "datasource": {
        "uid": "deg0vnk9jx8g0e",
        "type": "prometheus"
      },
      "hide": false,
      "editorMode": "builder",
      "legendFormat": "Taxa de Requisições",
      "useBackend": false,
      "disableTextWrap": false,
      "fullMetaSearch": false,
      "includeNullMetadata": true
    },
    {
      "refId": "B",
      "expr": "histogram_quantile(0.95, sum(rate(via_cep_request_duration_seconds_bucket[1m])) by (le))",
      "range": true,
      "instant": false,
      "datasource": {
        "uid": "deg0vnk9jx8g0e",
        "type": "prometheus"
      },
      "hide": false,
      "editorMode": "builder",
      "legendFormat": "Tempo de Resposta (95º percentil)",
      "useBackend": false,
      "disableTextWrap": false,
      "fullMetaSearch": false,
      "includeNullMetadata": true
    },
    {
      "refId": "C",
      "expr": "up",
      "range": true,
      "instant": false,
      "datasource": {
        "uid": "deg0vnk9jx8g0e",
        "type": "prometheus"
      },
      "hide": false,
      "editorMode": "builder",
      "legendFormat": "Status do Serviço",
      "useBackend": false,
      "disableTextWrap": false,
      "fullMetaSearch": false,
      "includeNullMetadata": true
    }
  ],
  "datasource": {
    "type": "prometheus",
    "uid": "deg0vnk9jx8g0e"
  },
  "options": {
    "tooltip": {
      "mode": "single",
      "sort": "none",
      "hideZeros": false
    },
    "legend": {
      "showLegend": true,
      "displayMode": "list",
      "placement": "bottom",
      "calcs": []
    }
  }
}
```
Click em:
* Apply
* Save dashboard
* Save

### Retorne para Dashboards e selecione o dashboard criado.

### Agora o dashboard de monitoramento do grafana está pronto.

### Realize testes, fazendo requisições na aplicação do Consulta de Cep


##  🔗 Autores

- [Izabel Nascimento](https://github.com/izabelnascimento)

- [Leonardo Nunes](https://github.com/leonardonb)

- [Tayane Cibely](https://github.com/tayanecibely)



