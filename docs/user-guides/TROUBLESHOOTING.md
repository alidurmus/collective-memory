# Collective Memory v2.1 Troubleshooting Guide

Bu rehber Collective Memory v2.1 ile karşılaşılan yaygın sorunları ve çözümlerini içerir.

## 🚨 Hızlı Tanı

### Sistem Durumu Kontrolü

```bash
# 1. Servis durumu kontrol
curl -f http://localhost:5000/system/status

# 2. Port kontrolü
netstat -tulpn | grep :5000
netstat -tulpn | grep :5173

# 3. Log kontrolü
tail -f .collective-memory/logs/app.log

# 4. Disk alanı
df -h

# 5. Memory kullanımı
free -h
```

### Test Komutları

```bash
# Backend test
python tests/test_runner.py --basic

# API test (server çalışırken)
python tests/test_runner.py --api

# Frontend test (frontend server çalışırken)
python tests/test_runner.py --ui
```

## 🖥️ Backend Sorunları

### 1. API Server Başlamıyor

#### Hata: "Port 5000 already in use"

```bash
# Problemi tespit et
lsof -i :5000
ps aux | grep api_server

# Çözüm 1: Process'i sonlandır
kill -9 <PID>

# Çözüm 2: Farklı port kullan
python api_server.py --port 5001
```

#### Hata: "ModuleNotFoundError"

```bash
# Problemi tespit et
python -c "import flask, nltk, sentence_transformers"

# Çözüm: Dependencies yeniden kur
pip install -r requirements.txt

# Virtual environment kontrolü
which python
echo $VIRTUAL_ENV
```

#### Hata: "Permission denied writing to .collective-memory"

```bash
# Problemi tespit et
ls -la .collective-memory/

# Çözüm: İzinleri düzelt
chmod -R 755 .collective-memory/
mkdir -p .collective-memory/{database,config,cache,logs}
```

### 2. Database Sorunları

#### Hata: "Database locked"

```bash
# Problemi tespit et
lsof .collective-memory/database/collective_memory.db

# Çözüm 1: Process'leri sonlandır
fuser -k .collective-memory/database/collective_memory.db

# Çözüm 2: WAL mode reset
sqlite3 .collective-memory/database/collective_memory.db "PRAGMA journal_mode=DELETE; PRAGMA journal_mode=WAL;"

# Çözüm 3: Database yeniden oluştur
rm .collective-memory/database/collective_memory.db
python -c "from src.database import init_db; init_db()"
```

#### Hata: "Disk I/O error"

```bash
# Disk alanı kontrol
df -h
du -sh .collective-memory/

# Temp dosyalar temizle
rm -rf .collective-memory/cache/*
rm -rf /tmp/collective-memory-*

# Database repair
sqlite3 .collective-memory/database/collective_memory.db ".backup backup.db"
mv backup.db .collective-memory/database/collective_memory.db
```

### 3. Search Engine Sorunları

#### Hata: "Semantic search not working"

```bash
# Model dosyalarını kontrol et
ls -la ~/.cache/huggingface/

# Model'i yeniden indir
python -c "
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('all-MiniLM-L6-v2')
print('Model loaded successfully')
"

# Cache'i temizle
rm -rf ~/.cache/huggingface/
rm -rf .collective-memory/cache/semantic_*
```

#### Hata: "Search timeout"

```bash
# Index durumunu kontrol et
curl http://localhost:5000/system/stats

# Index'i yeniden oluştur
curl -X POST http://localhost:5000/system/indexing/start

# Timeout ayarlarını artır
export SEARCH_TIMEOUT=60
python api_server.py
```

### 4. Memory/Performance Sorunları

#### Hata: "Out of memory"

```bash
# Memory kullanımını kontrol et
ps aux --sort=-%mem | head -10
free -h

# Çözüm 1: Cache'i temizle
curl -X POST http://localhost:5000/system/cache/clear

# Çözüm 2: Semantic search'ü devre dışı bırak
curl -X PUT http://localhost:5000/config \
  -H "Content-Type: application/json" \
  -d '{"search_settings": {"enable_semantic": false}}'

# Çözüm 3: Worker thread sayısını azalt
export WORKER_THREADS=2
python api_server.py
```

## 🌐 Frontend Sorunları

### 1. Development Server Başlamıyor

#### Hata: "npm ENOENT package.json"

```bash
# Doğru dizinde olduğunuzdan emin olun
cd frontend
ls -la package.json

# Dependencies'leri kur
npm install

# Cache'i temizle
npm cache clean --force
rm -rf node_modules package-lock.json
npm install
```

#### Hata: "Port 5173 already in use"

```bash
# Port'u kontrol et
lsof -i :5173

# Farklı port kullan
npm run dev -- --port 3000

# Veya package.json'da değiştir
"scripts": {
  "dev": "vite --port 3000"
}
```

### 2. Build Sorunları

#### Hata: "Build failed - memory exceeded"

```bash
# Node memory limit artır
export NODE_OPTIONS="--max_old_space_size=4096"
npm run build

# Vite config optimize et
# vite.config.js
export default defineConfig({
  build: {
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['react', 'react-dom'],
          ui: ['@headlessui/react', 'lucide-react']
        }
      }
    }
  }
})
```

#### Hata: "API connection failed"

```bash
# Environment variables kontrol
cat frontend/.env

# VITE_API_URL doğru mu?
echo $VITE_API_URL

# Backend çalışıyor mu?
curl http://localhost:5000/system/status

# CORS ayarları kontrol
curl -H "Origin: http://localhost:5173" \
     -H "Access-Control-Request-Method: POST" \
     -H "Access-Control-Request-Headers: X-Requested-With" \
     -X OPTIONS \
     http://localhost:5000/search
```

### 3. Browser Console Hataları

#### Hata: "Failed to fetch"

```javascript
// Browser console'da test et
fetch('http://localhost:5000/system/status')
  .then(r => r.json())
  .then(console.log)
  .catch(console.error);

// Network tab'ını kontrol et (F12)
// CORS headers var mı?
// 200 OK response geliyor mu?
```

#### Hata: "Uncaught TypeError: Cannot read properties"

```bash
# Dependencies version uyumsuzluğu
npm ls
npm audit

# React version kontrol
npm ls react react-dom

# Node version kontrol
node --version  # v18+ gerekli
npm --version
```

## 🧪 Test Sorunları

### 1. Playwright Testleri

#### Hata: "Browser executable not found"

```bash
# Browser'ları kur
cd frontend
npx playwright install

# Specific browser kur
npx playwright install chromium

# System dependencies
sudo apt-get install libnss3 libatk-bridge2.0-0 libgtk-3-0
```

#### Hata: "Test timeout"

```javascript
// playwright.config.js
module.exports = defineConfig({
  timeout: 60000,  // 60 saniye
  expect: {
    timeout: 10000  // 10 saniye
  },
  use: {
    actionTimeout: 30000  // 30 saniye
  }
});
```

#### Hata: "Page not found"

```bash
# Frontend server çalışıyor mu?
curl http://localhost:5173

# Backend server çalışıyor mu?
curl http://localhost:5000/system/status

# Test'i headed mode'da çalıştır
npx playwright test --headed --debug
```

### 2. Backend Test Sorunları

#### Hata: "API tests failing"

```python
# test_api_endpoints.py debug mode
import requests
import logging

logging.basicConfig(level=logging.DEBUG)

# Connection test
try:
    response = requests.get("http://localhost:5000/system/status", timeout=5)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")
```

## 🐳 Docker Sorunları

### 1. Container Build Sorunları

#### Hata: "Docker build failed"

```bash
# Build log'ları kontrol et
docker build . --no-cache 2>&1 | tee build.log

# Multi-stage build debug
docker build --target builder .

# Disk alanı kontrol
docker system df
docker system prune -f
```

#### Hata: "Permission denied"

```bash
# Docker daemon çalışıyor mu?
sudo systemctl status docker

# User docker grubunda mı?
groups $USER
sudo usermod -aG docker $USER
newgrp docker
```

### 2. Container Runtime Sorunları

#### Hata: "Container exiting immediately"

```bash
# Container log'ları
docker logs collective-memory-api

# Interactive mode'da çalıştır
docker run -it collective-memory:latest /bin/bash

# Health check kontrol
docker inspect collective-memory-api | grep -A 5 Health
```

#### Hata: "Volume mount issues"

```bash
# Volume permissions
ls -la data/
sudo chown -R 1000:1000 data/

# SELinux context (RedHat/CentOS)
sudo setsebool -P container_manage_cgroup true
```

## 🌐 Network Sorunları

### 1. API Connectivity

#### Hata: "Connection refused"

```bash
# Port'lar açık mı?
telnet localhost 5000
telnet localhost 5173

# Firewall kontrol
sudo ufw status
sudo iptables -L

# Local network test
curl -v http://127.0.0.1:5000/system/status
curl -v http://localhost:5000/system/status
```

#### Hata: "CORS policy error"

```python
# api_server.py CORS ayarları kontrol
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=['http://localhost:5173', 'http://localhost:3000'])

# Debug mode'da tüm origin'lere izin ver
if app.debug:
    CORS(app, origins='*')
```

### 2. WebSocket Sorunları

#### Hata: "WebSocket connection failed"

```javascript
// Frontend'de WebSocket test
const socket = io('http://localhost:5000', {
  transports: ['websocket', 'polling'],
  timeout: 20000
});

socket.on('connect', () => console.log('Connected'));
socket.on('disconnect', () => console.log('Disconnected'));
socket.on('connect_error', (error) => console.error('Connection error:', error));
```

```bash
# Backend WebSocket test
pip install python-socketio[client]
python -c "
import socketio
sio = socketio.SimpleClient()
sio.connect('http://localhost:5000')
print('Connected successfully')
sio.disconnect()
"
```

## 💾 Storage Sorunları

### 1. Disk Alanı Sorunları

#### Hata: "No space left on device"

```bash
# Disk kullanımı analiz
df -h
du -sh * | sort -hr

# Collective Memory dosya boyutları
du -sh .collective-memory/*
du -sh data/*

# Log dosyalarını temizle
find .collective-memory/logs/ -name "*.log" -mtime +7 -delete
find .collective-memory/cache/ -type f -mtime +1 -delete

# Eski index dosyalarını temizle
find .collective-memory/ -name "*.index" -mtime +30 -delete
```

### 2. File Permission Sorunları

```bash
# Tüm dosya izinlerini düzelt
find . -type f -name "*.py" -exec chmod 644 {} \;
find . -type f -name "*.sh" -exec chmod 755 {} \;
find . -type d -exec chmod 755 {} \;

# Database izinleri
chmod 664 .collective-memory/database/*.db
chmod 755 .collective-memory/database/

# Log izinleri
chmod 644 .collective-memory/logs/*.log
chmod 755 .collective-memory/logs/
```

## 🔐 Security Sorunları

### 1. SSL/TLS Sorunları

#### Hata: "SSL certificate issues"

```bash
# Certificate geçerliliği kontrol
openssl x509 -in certificate.crt -text -noout
openssl x509 -in certificate.crt -enddate -noout

# Let's Encrypt renewal
sudo certbot renew --dry-run
sudo certbot certificates

# Nginx SSL test
nginx -t
openssl s_client -connect your-domain.com:443
```

### 2. Authentication Sorunları

```bash
# Secret key kontrolü
grep SECRET_KEY .env
python -c "import os; print(len(os.environ.get('SECRET_KEY', '')))"

# Token validation test
curl -H "Authorization: Bearer YOUR_TOKEN" \
     http://localhost:5000/system/status
```

## 📊 Performance Sorunları

### 1. Slow Response Times

```bash
# API response time test
time curl http://localhost:5000/search \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"query": "test", "type": "basic"}'

# Database performance
sqlite3 .collective-memory/database/collective_memory.db \
  "EXPLAIN QUERY PLAN SELECT * FROM files WHERE content MATCH 'test';"

# Index statistics
curl http://localhost:5000/system/stats | jq '.data.performance'
```

### 2. Memory Leaks

```bash
# Memory monitoring
while true; do
  ps aux | grep api_server | grep -v grep
  sleep 10
done

# Python memory profiling
pip install memory-profiler
python -m memory_profiler api_server.py
```

## 🛠️ Advanced Debugging

### 1. Debug Mode Etkinleştirme

```bash
# Backend debug mode
export FLASK_DEBUG=1
export LOG_LEVEL=debug
python api_server.py --debug

# Frontend debug mode
export NODE_ENV=development
export DEBUG=*
npm run dev
```

### 2. Logging Detayları

```python
# api_server.py debug logging
import logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s [%(name)s] %(message)s',
    handlers=[
        logging.FileHandler('.collective-memory/logs/debug.log'),
        logging.StreamHandler()
    ]
)
```

### 3. Performance Profiling

```bash
# Python profiling
pip install cProfile
python -m cProfile -o profile.stats api_server.py

# Analyze profile
python -c "
import pstats
p = pstats.Stats('profile.stats')
p.sort_stats('cumulative').print_stats(20)
"

# Frontend performance
# Chrome DevTools -> Performance tab
# Lighthouse audit
npx lighthouse http://localhost:5173 --view
```

## 📞 Destek Alma

### 1. Bilgi Toplama

```bash
# System info script
cat > debug_info.sh << 'EOF'
#!/bin/bash
echo "=== Collective Memory Debug Info ==="
echo "Date: $(date)"
echo "OS: $(uname -a)"
echo "Python: $(python --version)"
echo "Node: $(node --version)"
echo "Disk: $(df -h .)"
echo "Memory: $(free -h)"
echo "Processes:"
ps aux | grep -E "(api_server|npm|node)" | grep -v grep
echo "Ports:"
netstat -tulpn | grep -E "(5000|5173)"
echo "Logs (last 20 lines):"
tail -20 .collective-memory/logs/app.log 2>/dev/null || echo "No logs found"
EOF

chmod +x debug_info.sh
./debug_info.sh > debug_info.txt
```

### 2. GitHub Issue Template

```markdown
## Environment
- OS: [Windows/macOS/Linux + version]
- Python version: [output of `python --version`]
- Node version: [output of `node --version`]
- Collective Memory version: [v2.1.0]

## Problem Description
[Clear description of the issue]

## Steps to Reproduce
1. [First step]
2. [Second step]
3. [Third step]

## Expected Behavior
[What you expected to happen]

## Actual Behavior
[What actually happened]

## Logs
```
[Paste relevant log outputs]
```

## Additional Context
[Screenshots, config files, etc.]
```

### 3. Community Resources

- **GitHub Issues**: https://github.com/collective-memory/issues
- **Discussions**: https://github.com/collective-memory/discussions
- **Wiki**: https://github.com/collective-memory/wiki
- **Stack Overflow**: Tag `collective-memory`

---

**Bu troubleshooting guide sürekli güncellenmektedir. Yeni sorunlar ve çözümler için GitHub repository'sini takip edin.** 