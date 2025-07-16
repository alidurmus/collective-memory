# Collective Memory v2.1 Deployment Guide

Bu rehber Collective Memory v2.1'i production ortamında deploy etmek için adım adım talimatlar içerir.

## 🎯 Deployment Seçenekleri

- **🐳 Docker (Recommended)**: Containerized deployment
- **☁️ Cloud Platform**: AWS, Azure, GCP
- **🖥️ Bare Metal/VPS**: Direct server installation
- **🔄 Kubernetes**: Scalable container orchestration

## 🐳 Docker Deployment (Recommended)

### 1. Docker Setup

#### Dockerfile (Backend)

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# System dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Application code
COPY . .

# Create data directories
RUN mkdir -p .collective-memory/{database,config,cache,logs}

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:5000/system/status || exit 1

EXPOSE 5000

CMD ["python", "api_server.py", "--host", "0.0.0.0", "--port", "5000"]
```

#### Dockerfile (Frontend)

```dockerfile
FROM node:18-alpine as builder

WORKDIR /app
COPY frontend/package*.json ./
RUN npm ci --only=production

COPY frontend/ .
RUN npm run build

FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

#### docker-compose.yml

```yaml
version: '3.8'

services:
  collective-memory-backend:
    build: 
      context: .
      dockerfile: Dockerfile
    container_name: collective-memory-api
    restart: unless-stopped
    ports:
      - "5000:5000"
    volumes:
      - ./data:/app/data
      - ./.collective-memory:/app/.collective-memory
    environment:
      - FLASK_ENV=production
      - SECRET_KEY=${SECRET_KEY:-your-secret-key-here}
      - DATA_FOLDER=/app/data
      - LOG_LEVEL=info
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5000/system/status"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    networks:
      - collective-memory-network

  collective-memory-frontend:
    build:
      context: .
      dockerfile: frontend/Dockerfile
    container_name: collective-memory-web
    restart: unless-stopped
    ports:
      - "80:80"
      - "443:443"
    environment:
      - VITE_API_URL=http://collective-memory-backend:5000
    depends_on:
      - collective-memory-backend
    networks:
      - collective-memory-network

  nginx:
    image: nginx:alpine
    container_name: collective-memory-proxy
    restart: unless-stopped
    ports:
      - "8080:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./ssl:/etc/nginx/ssl:ro
    depends_on:
      - collective-memory-frontend
      - collective-memory-backend
    networks:
      - collective-memory-network

networks:
  collective-memory-network:
    driver: bridge

volumes:
  collective-memory-data:
    driver: local
```

### 2. Environment Configuration

#### .env File

```bash
# Application Settings
SECRET_KEY=your-super-secret-key-change-this-in-production
FLASK_ENV=production
DEBUG=false

# Data Configuration
DATA_FOLDER=/app/data
MAX_FILE_SIZE_MB=100
MAX_INDEX_SIZE_MB=1000

# Database Settings
DATABASE_URL=sqlite:////.collective-memory/database/collective_memory.db
DATABASE_POOL_SIZE=10

# Cache Settings
CACHE_TYPE=redis
REDIS_URL=redis://redis:6379/0
CACHE_TTL_MINUTES=30

# Logging
LOG_LEVEL=info
LOG_FILE=/app/.collective-memory/logs/app.log
LOG_ROTATION=daily

# Security
ALLOWED_HOSTS=localhost,127.0.0.1,your-domain.com
CORS_ORIGINS=https://your-domain.com
RATE_LIMIT_PER_MINUTE=100

# Performance
WORKER_THREADS=4
MAX_MEMORY_MB=1024
ENABLE_SEMANTIC_SEARCH=true

# Monitoring
SENTRY_DSN=your-sentry-dsn-here
ENABLE_METRICS=true
METRICS_PORT=9090
```

### 3. Deployment Commands

```bash
# Clone repository
git clone https://github.com/your-username/collective-memory.git
cd collective-memory

# Create environment file
cp .env.example .env
# Edit .env with your production values

# Create data directories
mkdir -p data
mkdir -p .collective-memory/{database,config,cache,logs}

# Build and start services
docker-compose up -d

# Check service status
docker-compose ps
docker-compose logs -f

# Initialize database (first time only)
docker-compose exec collective-memory-backend python -c "from src.database import init_db; init_db()"

# Run initial indexing
docker-compose exec collective-memory-backend python main.py --data-folder /app/data
```

## ☁️ Cloud Platform Deployment

### AWS Deployment

#### Using AWS ECS

```yaml
# ecs-task-definition.json
{
  "family": "collective-memory",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "1024",
  "memory": "2048",
  "executionRoleArn": "arn:aws:iam::account:role/ecsTaskExecutionRole",
  "taskRoleArn": "arn:aws:iam::account:role/ecsTaskRole",
  "containerDefinitions": [
    {
      "name": "collective-memory-backend",
      "image": "your-account.dkr.ecr.region.amazonaws.com/collective-memory:latest",
      "portMappings": [
        {
          "containerPort": 5000,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {
          "name": "FLASK_ENV",
          "value": "production"
        }
      ],
      "secrets": [
        {
          "name": "SECRET_KEY",
          "valueFrom": "arn:aws:secretsmanager:region:account:secret:collective-memory-secret"
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/collective-memory",
          "awslogs-region": "us-west-2",
          "awslogs-stream-prefix": "ecs"
        }
      }
    }
  ]
}
```

#### CloudFormation Template

```yaml
AWSTemplateFormatVersion: '2010-09-09'
Description: 'Collective Memory v2.1 Infrastructure'

Parameters:
  EnvironmentName:
    Description: Environment name prefix
    Type: String
    Default: collective-memory

Resources:
  VPC:
    Type: AWS::EC2::VPC
    Properties:
      CidrBlock: 10.0.0.0/16
      EnableDnsHostnames: true
      EnableDnsSupport: true
      Tags:
        - Key: Name
          Value: !Sub ${EnvironmentName}-VPC

  ECSCluster:
    Type: AWS::ECS::Cluster
    Properties:
      ClusterName: !Sub ${EnvironmentName}-cluster
      CapacityProviders:
        - FARGATE
        - FARGATE_SPOT

  ApplicationLoadBalancer:
    Type: AWS::ElasticLoadBalancingV2::LoadBalancer
    Properties:
      Name: !Sub ${EnvironmentName}-ALB
      Scheme: internet-facing
      Type: application
      Subnets:
        - !Ref PublicSubnet1
        - !Ref PublicSubnet2
      SecurityGroups:
        - !Ref ALBSecurityGroup

  # Additional resources...
```

### Azure Deployment

#### Azure Container Instances

```bash
# Create resource group
az group create --name collective-memory-rg --location eastus

# Create container instance
az container create \
  --resource-group collective-memory-rg \
  --name collective-memory \
  --image your-registry/collective-memory:latest \
  --cpu 2 \
  --memory 4 \
  --ports 5000 80 \
  --environment-variables \
    FLASK_ENV=production \
    DATA_FOLDER=/app/data \
  --secure-environment-variables \
    SECRET_KEY=your-secret-key \
  --restart-policy Always
```

### Google Cloud Platform

#### Cloud Run Deployment

```yaml
# cloud-run-service.yaml
apiVersion: serving.knative.dev/v1
kind: Service
metadata:
  name: collective-memory
  annotations:
    run.googleapis.com/ingress: all
spec:
  template:
    metadata:
      annotations:
        autoscaling.knative.dev/maxScale: "10"
        run.googleapis.com/cpu-throttling: "false"
    spec:
      containerConcurrency: 80
      containers:
      - image: gcr.io/your-project/collective-memory:latest
        ports:
        - containerPort: 5000
        env:
        - name: FLASK_ENV
          value: production
        - name: SECRET_KEY
          valueFrom:
            secretKeyRef:
              name: collective-memory-secret
              key: secret-key
        resources:
          limits:
            cpu: 2000m
            memory: 4Gi
```

## 🖥️ Bare Metal/VPS Deployment

### System Requirements

#### Minimum Requirements
- **CPU**: 2 cores, 2.4 GHz
- **RAM**: 4 GB
- **Storage**: 20 GB SSD
- **Network**: 100 Mbps
- **OS**: Ubuntu 20.04+, CentOS 8+, or equivalent

#### Recommended Requirements
- **CPU**: 4 cores, 3.0 GHz
- **RAM**: 8 GB
- **Storage**: 100 GB SSD
- **Network**: 1 Gbps
- **OS**: Ubuntu 22.04 LTS

### Installation Steps

#### 1. System Setup

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install required packages
sudo apt install -y \
  python3.11 \
  python3-pip \
  python3-venv \
  nodejs \
  npm \
  nginx \
  redis-server \
  sqlite3 \
  git \
  curl \
  htop

# Create user for application
sudo adduser --system --group collective-memory
sudo usermod -aG www-data collective-memory
```

#### 2. Application Setup

```bash
# Clone and setup application
sudo su - collective-memory
git clone https://github.com/your-username/collective-memory.git /home/collective-memory/app
cd /home/collective-memory/app

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Setup directories
mkdir -p .collective-memory/{database,config,cache,logs}
mkdir -p data

# Build frontend
cd frontend
npm install
npm run build
```

#### 3. Systemd Service

```ini
# /etc/systemd/system/collective-memory.service
[Unit]
Description=Collective Memory API Server
After=network.target

[Service]
Type=simple
User=collective-memory
Group=collective-memory
WorkingDirectory=/home/collective-memory/app
Environment=PATH=/home/collective-memory/app/venv/bin
Environment=FLASK_ENV=production
Environment=SECRET_KEY=your-secret-key
ExecStart=/home/collective-memory/app/venv/bin/python api_server.py --host 0.0.0.0 --port 5000
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```bash
# Enable and start service
sudo systemctl daemon-reload
sudo systemctl enable collective-memory
sudo systemctl start collective-memory
sudo systemctl status collective-memory
```

#### 4. Nginx Configuration

```nginx
# /etc/nginx/sites-available/collective-memory
server {
    listen 80;
    server_name your-domain.com;
    
    # Redirect HTTP to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name your-domain.com;
    
    # SSL Configuration
    ssl_certificate /path/to/certificate.crt;
    ssl_certificate_key /path/to/private.key;
    ssl_session_timeout 1d;
    ssl_session_cache shared:SSL:50m;
    ssl_stapling on;
    ssl_stapling_verify on;
    
    # Security headers
    add_header X-Frame-Options DENY;
    add_header X-Content-Type-Options nosniff;
    add_header X-XSS-Protection "1; mode=block";
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    
    # Frontend static files
    location / {
        root /home/collective-memory/app/frontend/dist;
        try_files $uri $uri/ /index.html;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
    
    # API proxy
    location /api/ {
        proxy_pass http://127.0.0.1:5000/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # WebSocket support
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        
        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }
    
    # Upload limits
    client_max_body_size 100m;
    
    # Gzip compression
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_types text/plain text/css text/xml text/javascript application/javascript application/xml+rss application/json;
}
```

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/collective-memory /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

## 🔄 Kubernetes Deployment

### Kubernetes Manifests

#### Namespace

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: collective-memory
```

#### ConfigMap

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: collective-memory-config
  namespace: collective-memory
data:
  FLASK_ENV: "production"
  DATA_FOLDER: "/app/data"
  LOG_LEVEL: "info"
  WORKER_THREADS: "4"
```

#### Secret

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: collective-memory-secret
  namespace: collective-memory
type: Opaque
stringData:
  secret-key: "your-super-secret-key"
  redis-url: "redis://redis:6379/0"
```

#### Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: collective-memory-backend
  namespace: collective-memory
spec:
  replicas: 3
  selector:
    matchLabels:
      app: collective-memory-backend
  template:
    metadata:
      labels:
        app: collective-memory-backend
    spec:
      containers:
      - name: collective-memory
        image: your-registry/collective-memory:latest
        ports:
        - containerPort: 5000
        envFrom:
        - configMapRef:
            name: collective-memory-config
        - secretRef:
            name: collective-memory-secret
        volumeMounts:
        - name: data-volume
          mountPath: /app/data
        - name: cache-volume
          mountPath: /app/.collective-memory
        livenessProbe:
          httpGet:
            path: /system/status
            port: 5000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /system/status
            port: 5000
          initialDelaySeconds: 5
          periodSeconds: 5
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "2Gi"
            cpu: "1000m"
      volumes:
      - name: data-volume
        persistentVolumeClaim:
          claimName: collective-memory-data-pvc
      - name: cache-volume
        emptyDir: {}
```

#### Service

```yaml
apiVersion: v1
kind: Service
metadata:
  name: collective-memory-service
  namespace: collective-memory
spec:
  selector:
    app: collective-memory-backend
  ports:
  - port: 80
    targetPort: 5000
  type: ClusterIP
```

#### Ingress

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: collective-memory-ingress
  namespace: collective-memory
  annotations:
    kubernetes.io/ingress.class: "nginx"
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
    nginx.ingress.kubernetes.io/proxy-body-size: "100m"
spec:
  tls:
  - hosts:
    - collective-memory.your-domain.com
    secretName: collective-memory-tls
  rules:
  - host: collective-memory.your-domain.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: collective-memory-service
            port:
              number: 80
```

### Helm Chart

#### Chart.yaml

```yaml
apiVersion: v2
name: collective-memory
description: AI-powered knowledge management system
version: 2.1.0
appVersion: "2.1.0"
```

#### values.yaml

```yaml
replicaCount: 3

image:
  repository: your-registry/collective-memory
  tag: "latest"
  pullPolicy: IfNotPresent

service:
  type: ClusterIP
  port: 80

ingress:
  enabled: true
  className: "nginx"
  hosts:
    - host: collective-memory.your-domain.com
      paths:
        - path: /
          pathType: Prefix
  tls:
    - secretName: collective-memory-tls
      hosts:
        - collective-memory.your-domain.com

resources:
  requests:
    memory: "512Mi"
    cpu: "250m"
  limits:
    memory: "2Gi"
    cpu: "1000m"

persistence:
  enabled: true
  size: 50Gi
  storageClass: "gp2"

redis:
  enabled: true
  auth:
    enabled: false
```

## 🔒 Security Hardening

### SSL/TLS Configuration

#### Let's Encrypt with Certbot

```bash
# Install certbot
sudo apt install certbot python3-certbot-nginx

# Obtain certificate
sudo certbot --nginx -d your-domain.com

# Auto-renewal
sudo crontab -e
# Add: 0 12 * * * /usr/bin/certbot renew --quiet
```

### Firewall Configuration

```bash
# UFW setup
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable

# iptables alternative
sudo iptables -A INPUT -p tcp --dport 22 -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 80 -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 443 -j ACCEPT
sudo iptables -A INPUT -j DROP
```

### Application Security

#### Environment Variables

```bash
# Secure environment file permissions
chmod 600 .env
chown collective-memory:collective-memory .env

# Generate secure secret key
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

#### Rate Limiting

```nginx
# Nginx rate limiting
http {
    limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
    
    server {
        location /api/ {
            limit_req zone=api burst=20 nodelay;
            # ... other config
        }
    }
}
```

## 📊 Monitoring & Logging

### System Monitoring

#### Prometheus Configuration

```yaml
# prometheus.yml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'collective-memory'
    static_configs:
      - targets: ['localhost:9090']
    metrics_path: '/metrics'
```

#### Grafana Dashboard

```json
{
  "dashboard": {
    "title": "Collective Memory Monitoring",
    "panels": [
      {
        "title": "API Response Time",
        "type": "graph",
        "targets": [
          {
            "expr": "collective_memory_request_duration_seconds"
          }
        ]
      },
      {
        "title": "Search Requests/sec",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(collective_memory_searches_total[5m])"
          }
        ]
      }
    ]
  }
}
```

### Centralized Logging

#### ELK Stack Configuration

```yaml
# docker-compose.logging.yml
version: '3.8'
services:
  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:8.5.0
    environment:
      - discovery.type=single-node
      - xpack.security.enabled=false
    ports:
      - "9200:9200"

  logstash:
    image: docker.elastic.co/logstash/logstash:8.5.0
    volumes:
      - ./logstash.conf:/usr/share/logstash/pipeline/logstash.conf
    ports:
      - "5044:5044"

  kibana:
    image: docker.elastic.co/kibana/kibana:8.5.0
    ports:
      - "5601:5601"
    environment:
      - ELASTICSEARCH_URL=http://elasticsearch:9200
```

## 🚀 Performance Optimization

### Database Optimization

```sql
-- SQLite optimization
PRAGMA journal_mode = WAL;
PRAGMA synchronous = NORMAL;
PRAGMA cache_size = 10000;
PRAGMA temp_store = memory;
PRAGMA mmap_size = 268435456;
```

### Caching Strategy

```python
# Redis caching configuration
CACHE_CONFIG = {
    'CACHE_TYPE': 'redis',
    'CACHE_REDIS_URL': 'redis://localhost:6379/0',
    'CACHE_DEFAULT_TIMEOUT': 300,
    'CACHE_KEY_PREFIX': 'collective_memory:',
}
```

### Load Balancing

#### HAProxy Configuration

```
global
    daemon
    maxconn 4096

defaults
    mode http
    timeout connect 5000ms
    timeout client 50000ms
    timeout server 50000ms

frontend collective_memory_frontend
    bind *:80
    default_backend collective_memory_backend

backend collective_memory_backend
    balance roundrobin
    server web1 127.0.0.1:5001 check
    server web2 127.0.0.1:5002 check
    server web3 127.0.0.1:5003 check
```

## 🔄 Backup & Recovery

### Automated Backup Script

```bash
#!/bin/bash
# backup.sh

BACKUP_DIR="/backup/collective-memory"
DATE=$(date +%Y%m%d_%H%M%S)
APP_DIR="/home/collective-memory/app"

# Create backup directory
mkdir -p "$BACKUP_DIR"

# Backup database
sqlite3 "$APP_DIR/.collective-memory/database/collective_memory.db" ".backup '$BACKUP_DIR/database_$DATE.db'"

# Backup configuration
tar -czf "$BACKUP_DIR/config_$DATE.tar.gz" -C "$APP_DIR" .collective-memory/config

# Backup data files
tar -czf "$BACKUP_DIR/data_$DATE.tar.gz" -C "$APP_DIR" data

# Cleanup old backups (keep last 30 days)
find "$BACKUP_DIR" -name "*.db" -mtime +30 -delete
find "$BACKUP_DIR" -name "*.tar.gz" -mtime +30 -delete

echo "Backup completed: $DATE"
```

### Recovery Procedures

```bash
# Stop services
sudo systemctl stop collective-memory

# Restore database
cp /backup/collective-memory/database_YYYYMMDD_HHMMSS.db \
   /home/collective-memory/app/.collective-memory/database/collective_memory.db

# Restore configuration
tar -xzf /backup/collective-memory/config_YYYYMMDD_HHMMSS.tar.gz \
   -C /home/collective-memory/app

# Restore data
tar -xzf /backup/collective-memory/data_YYYYMMDD_HHMMSS.tar.gz \
   -C /home/collective-memory/app

# Fix permissions
chown -R collective-memory:collective-memory /home/collective-memory/app

# Start services
sudo systemctl start collective-memory
```

## 🔧 Troubleshooting

### Common Issues

#### Port Already in Use
```bash
# Find process using port 5000
sudo netstat -tulpn | grep :5000
sudo kill -9 <PID>
```

#### Database Lock Issues
```bash
# Check database locks
sudo fuser /home/collective-memory/app/.collective-memory/database/collective_memory.db

# Reset WAL mode
sqlite3 /path/to/database.db "PRAGMA journal_mode=DELETE; PRAGMA journal_mode=WAL;"
```

#### Memory Issues
```bash
# Monitor memory usage
htop
sudo journalctl -u collective-memory -f

# Adjust system limits
echo "collective-memory soft memlock unlimited" >> /etc/security/limits.conf
echo "collective-memory hard memlock unlimited" >> /etc/security/limits.conf
```

### Health Checks

```bash
# API health check
curl -f http://localhost:5000/system/status || exit 1

# Service status
sudo systemctl status collective-memory

# Log monitoring
sudo journalctl -u collective-memory --since "1 hour ago"
```

---

**Bu deployment guide ile Collective Memory v2.1'i production ortamında güvenli ve ölçeklenebilir şekilde deploy edebilirsiniz.** 🚀 