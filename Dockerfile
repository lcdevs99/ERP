FROM python:3.12-slim

WORKDIR /code

# Instalar dependências do sistema necessárias para mysqlclient
RUN apt-get update && apt-get install -y \
    gcc \
    pkg-config \
    default-libmysqlclient-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
CMD ["python", "src/manage.py", "runserver", "0.0.0.0:8000"]