FROM python:3.11-slim

# Çalışma dizini ayarla
WORKDIR /app

# Sistem bağımlılıklarını yükle
RUN apt-get update && apt-get install -y \
    sqlite3 \
    && rm -rf /var/lib/apt/lists/*

# Python bağımlılıklarını kopyala ve yükle
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Uygulama dosyalarını kopyala
COPY src/ ./src/
COPY config/ ./config/

# Giriş noktasını ayarla
ENTRYPOINT ["python", "src/main.py"]
CMD ["--help"] 