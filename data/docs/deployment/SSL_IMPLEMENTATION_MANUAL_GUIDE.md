# 🔒 Context7 ERP - Manual SSL Implementation Guide

**Date:** 13 Temmuz 2025  
**Version:** v2.2.0-glassmorphism-enhanced + Manual SSL Implementation  
**QMS Reference:** REC-SECURITY-SSL-MANUAL-250713-001  
**Status:** ✅ Ready for Implementation

---

## 🎯 **SSL Implementation Overview**

### **Target Configuration**
- **Server:** 31.97.44.248 (srv858543.hstgr.cloud)
- **SSL Type:** IP-based self-signed certificate
- **Domain:** IP address (31.97.44.248)
- **Protocol:** HTTPS with redirect from HTTP
- **Security:** Production-grade headers and configurations

### **Implementation Status**
- ✅ **Scripts Prepared:** All SSL scripts ready
- ✅ **Django Settings:** HTTPS production settings configured
- ✅ **Nginx Config:** SSL proxy configuration prepared
- ✅ **Test Scripts:** SSL validation scripts ready
- 🔄 **Deployment:** Manual execution required

---

## 📋 **Manual Implementation Steps**

### **Step 1: Upload Scripts to Server**
```bash
# SSH to production server
ssh root@31.97.44.248

# Create SSL setup directory
mkdir -p /root/ssl-setup
cd /root/ssl-setup

# Upload scripts manually or copy content
# Files to upload:
# - production_ssl_ip_based.sh
# - ssl_test_validation.sh
# - https_production_settings.py
```

### **Step 2: Copy Script Contents**

#### **A) Create production_ssl_ip_based.sh**
```bash
cat > /root/ssl-setup/production_ssl_ip_based.sh << 'EOF'
#!/bin/bash

# Context7 ERP - IP-based SSL Setup Script
set -e

echo "🔒 Context7 ERP - IP-based SSL Setup"
echo "===================================="

IP_ADDRESS="31.97.44.248"
PROJECT_PATH="/home/context7/context7-erp"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

print_status() { echo -e "${BLUE}[INFO]${NC} $1"; }
print_success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }

# Check root
if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root"
   exit 1
fi

print_status "Starting IP-based SSL setup..."

# Update packages
print_status "Updating system packages..."
apt update && apt upgrade -y

# Install packages
print_status "Installing required packages..."
apt install -y nginx openssl ufw

# Configure firewall
print_status "Configuring firewall..."
ufw allow 'Nginx Full'
ufw allow 'OpenSSH'
ufw --force enable

# Create SSL directory
print_status "Creating SSL directory..."
mkdir -p /etc/nginx/ssl

# Generate certificate
print_status "Generating SSL certificate..."
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout /etc/nginx/ssl/context7-ip.key \
    -out /etc/nginx/ssl/context7-ip.crt \
    -subj "/C=TR/ST=Istanbul/L=Istanbul/O=Context7 ERP/OU=Production/CN=$IP_ADDRESS" \
    -addext "subjectAltName=IP:$IP_ADDRESS"

print_success "SSL certificate generated!"

# Create Nginx configuration
print_status "Creating Nginx configuration..."
cat > /etc/nginx/sites-available/context7-erp-ip-ssl << 'NGINX_EOF'
# HTTP to HTTPS redirect
server {
    listen 80;
    server_name 31.97.44.248;
    return 301 https://$server_name$request_uri;
}

# HTTPS server
server {
    listen 443 ssl http2;
    server_name 31.97.44.248;
    
    # SSL Configuration
    ssl_certificate /etc/nginx/ssl/context7-ip.crt;
    ssl_certificate_key /etc/nginx/ssl/context7-ip.key;
    
    # SSL Security
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_prefer_server_ciphers off;
    ssl_session_timeout 1d;
    ssl_session_cache shared:SSL:50m;
    
    # Security Headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Frame-Options DENY always;
    add_header X-Content-Type-Options nosniff always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
    
    # Django proxy
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header X-Forwarded-Host $host;
        proxy_set_header X-Forwarded-Port $server_port;
        
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }
    
    # Static files
    location /static/ {
        alias /home/context7/context7-erp/staticfiles/;
        expires 1y;
        add_header Cache-Control "public, immutable";
        gzip on;
        gzip_types text/css application/javascript;
    }
    
    # Media files
    location /media/ {
        alias /home/context7/context7-erp/media/;
        expires 1M;
        add_header Cache-Control "public";
    }
    
    # Security blocks
    location ~ /\. { deny all; }
    location ~ \.(env|log|ini|conf)$ { deny all; }
}
NGINX_EOF

# Enable site
print_status "Enabling site..."
rm -f /etc/nginx/sites-enabled/default
ln -sf /etc/nginx/sites-available/context7-erp-ip-ssl /etc/nginx/sites-enabled/

# Test and restart
print_status "Testing Nginx configuration..."
nginx -t

print_status "Restarting Nginx..."
systemctl restart nginx
systemctl enable nginx

print_success "SSL setup complete!"
echo "🔗 HTTPS URL: https://$IP_ADDRESS"
EOF

chmod +x /root/ssl-setup/production_ssl_ip_based.sh
```

#### **B) Create SSL Test Script**
```bash
cat > /root/ssl-setup/ssl_test_validation.sh << 'EOF'
#!/bin/bash

echo "🔍 SSL Test & Validation"
echo "======================="

IP_ADDRESS="31.97.44.248"
TESTS_PASSED=0
TESTS_TOTAL=0

run_test() {
    echo -n "Testing $1... "
    TESTS_TOTAL=$((TESTS_TOTAL + 1))
    
    if eval "$2" >/dev/null 2>&1; then
        echo "PASS"
        TESTS_PASSED=$((TESTS_PASSED + 1))
    else
        echo "FAIL"
    fi
}

# SSL Tests
run_test "SSL Certificate Exists" "test -f /etc/nginx/ssl/context7-ip.crt"
run_test "SSL Key Exists" "test -f /etc/nginx/ssl/context7-ip.key"
run_test "Nginx Config Valid" "nginx -t"
run_test "Nginx Running" "systemctl is-active nginx"
run_test "Port 443 Open" "netstat -ln | grep -q ':443'"
run_test "HTTP Redirect" "curl -s -I http://$IP_ADDRESS | grep -q '301\|302'"
run_test "HTTPS Response" "curl -k -s -I https://$IP_ADDRESS | grep -q 'HTTP'"
run_test "HSTS Header" "curl -k -s -I https://$IP_ADDRESS | grep -qi 'strict-transport-security'"

echo ""
echo "Results: $TESTS_PASSED/$TESTS_TOTAL tests passed"

if [ $TESTS_PASSED -eq $TESTS_TOTAL ]; then
    echo "✅ ALL TESTS PASSED!"
else
    echo "❌ Some tests failed"
fi
EOF

chmod +x /root/ssl-setup/ssl_test_validation.sh
```

### **Step 3: Execute SSL Setup**
```bash
# Run SSL setup
cd /root/ssl-setup
./production_ssl_ip_based.sh

# Wait for completion, then run tests
./ssl_test_validation.sh
```

### **Step 4: Update Django Settings**
```bash
# Create HTTPS settings file
cat > /home/context7/context7-erp/dashboard_project/https_production_settings.py << 'EOF'
from .postgresql_settings import *

# HTTPS Configuration
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True

# Session Security
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True

# Allowed Hosts
ALLOWED_HOSTS = ['31.97.44.248', 'localhost', '127.0.0.1']

# CSRF Origins
CSRF_TRUSTED_ORIGINS = ['https://31.97.44.248']

print("🔒 HTTPS Production Settings Loaded")
EOF

# Update environment
cat > /home/context7/context7-erp/.env.https << 'EOF'
DJANGO_SETTINGS_MODULE=dashboard_project.https_production_settings
HTTPS_ENABLED=True
SSL_TYPE=ip_based
FORCE_HTTPS=True
EOF

# Restart Django with HTTPS settings
cd /home/context7/context7-erp
source .env.https
python manage.py collectstatic --noinput
systemctl restart django
```

### **Step 5: Final Verification**
```bash
# Test HTTPS connectivity
curl -k -s https://31.97.44.248 | head -20

# Check service status
systemctl status nginx
systemctl status django

# View logs if needed
tail -f /var/log/nginx/error.log
```

---

## 🎯 **Expected Results**

### **Successful Implementation Indicators**
- ✅ HTTPS URL responds: `https://31.97.44.248`
- ✅ HTTP redirects to HTTPS automatically
- ✅ Browser shows certificate warning (normal for self-signed)
- ✅ All Context7 ERP functionality works over HTTPS
- ✅ Security headers present in response

### **Browser Access**
1. Navigate to: `https://31.97.44.248`
2. Accept certificate exception (self-signed warning)
3. Login to Context7 ERP system
4. Verify all features work over HTTPS

---

## 🛡️ **Security Notes**

### **Self-Signed Certificate**
- Browser will show security warning
- Accept the exception to proceed
- Certificate valid for 365 days
- IP-based certificate (not domain-based)

### **Production Security**
- HSTS enabled (1 year)
- XSS protection active
- Frame options deny
- Content type nosniff
- Secure cookies enabled

---

## 📊 **Troubleshooting**

### **Common Issues**
1. **Port 443 access denied**: Check firewall settings
2. **Nginx fails to start**: Check configuration syntax
3. **Django 502 error**: Verify Django service running
4. **Certificate warnings**: Normal for self-signed certificates

### **Log Locations**
- Nginx errors: `/var/log/nginx/error.log`
- Django logs: `journalctl -u django -f`
- SSL setup logs: Terminal output during setup

---

## ✅ **Implementation Checklist**

- [ ] SSH access to production server
- [ ] Upload and execute SSL setup script
- [ ] Verify SSL tests pass
- [ ] Update Django HTTPS settings
- [ ] Restart Django service
- [ ] Test HTTPS access in browser
- [ ] Accept certificate exception
- [ ] Verify all functionality
- [ ] Document completion

---

**🎯 Success Criteria:** HTTPS access working with self-signed certificate, all security headers active, Django app accessible over SSL.

**📞 Support:** Follow QMS Central Protocol v1.0 for any issues during implementation. 