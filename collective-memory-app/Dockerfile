# Stage 1: Build frontend
FROM node:20 AS frontend-build
WORKDIR /frontend
COPY frontend/package.json frontend/package-lock.json ./
RUN npm ci
COPY frontend/ ./
RUN npm run build

# Stage 2: Backend + production image
FROM python:3.11-slim
WORKDIR /app

# Sistem bağımlılıkları
RUN apt-get update && apt-get install -y \
    sqlite3 \
    && rm -rf /var/lib/apt/lists/*

# Python bağımlılıkları
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt \
    && pip install gunicorn

# Backend kodunu kopyala
COPY src/ ./src/
COPY config/ ./config/
COPY api_server.py ./

# Frontend build'i kopyala (statik dosyalar)
COPY --from=frontend-build /frontend/dist ./frontend-dist

# Flask'ın static_folder parametresiyle statik dosyaları serve etmesi için ayar
ENV FLASK_STATIC_FOLDER=/app/frontend-dist
ENV FLASK_APP=api_server.py
ENV FLASK_RUN_PORT=8000

# Production için gunicorn ile başlat
EXPOSE 8000
CMD ["gunicorn", "-b", "0.0.0.0:8000", "api_server:app"] 