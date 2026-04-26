# imagem base
FROM python:3.11-slim

# evita logs travados
ENV PYTHONUNBUFFERED=1

# diretório de trabalho
WORKDIR /app

# copia dependências
COPY requirements.txt .

# instala dependências
RUN pip install --no-cache-dir -r requirements.txt

# copia o projeto
COPY . .

# expõe porta do streamlit
EXPOSE 8501

# comando para rodar o app
CMD ["streamlit", "run", "src/app.py", "--server.port=8501", "--server.address=0.0.0.0"]