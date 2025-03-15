# Usa a imagem oficial do Python como base
FROM python:3.9

# Define o diretório de trabalho
WORKDIR /app

# Copia os arquivos do projeto para o container
COPY . /app

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Expõe a porta usada pelo Flask
EXPOSE 5000

# Comando para rodar a aplicação
CMD ["python", "app.py"]