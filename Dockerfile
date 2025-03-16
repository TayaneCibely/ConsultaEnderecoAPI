FROM python:3.9-slim-buster

WORKDIR /app

# Atualiza o pip e desativa a barra de progresso
RUN pip install --upgrade pip --progress-bar off

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt --progress-bar off

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]