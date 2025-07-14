# 🔐 Context7 ERP - SSL Certificate Implementation Plan

**Date**: 11 Ocak 2025  
**Production Server**: http://31.97.44.248:8000  
**Target**: https://intermeks.com (SSL Ready)  
**Purpose**: Implement HTTPS security for production deployment  
**QMS Reference**: REC-SECURITY-SSL-IMPLEMENTATION-250111-018

---

## 📋 **SSL Implementation Status**

### ✅ **Current Status**
- **HTTP Server**: ✅ Active (31.97.44.248:8000)
- **Security Headers**: ✅ Active (CSP, XSS-Protection, etc.)
- **Domain**: intermeks.com (DNS configuration pending)
- **VPS Access**: ✅ Root access available
- **Django HTTPS Settings**: ✅ Ready (dashboard_project/https_settings.py)

### 🎯 **Target Configuration**
- **HTTPS**: https://intermeks.com
- **SSL Certificate**: Let's Encrypt (Free)
- **Web Server**: Nginx + Gunicorn
- **Auto-Renewal**: Certbot automation
- **Security Score**: SSL Labs A+ rating

---

## 🚀 **SSL Implementation Steps**

### **Phase 1: Domain Configuration** (30 minutes)
```bash
# DNS Settings (at domain provider)
A Record: intermeks.com → 31.97.44.248
A Record: www.intermeks.com → 31.97.44.248
CNAME: * → intermeks.com (optional wildcard)

# Verify DNS propagation
nslookup intermeks.com
dig intermeks.com
```

### **Phase 2: Nginx Installation & Configuration** (45 minutes)
```bash
# SSH to VPS
ssh root@31.97.44.248

# Install Nginx
apt update
apt install nginx
systemctl enable nginx
systemctl start nginx

# Create Nginx configuration
cat > /etc/nginx/sites-available/intermeks.com << 'EOF'
server {
    listen 80;
    server_name intermeks.com www.intermeks.com 31.97.44.248;
    
    # Redirect HTTP to HTTPS (after SSL setup)
    # return 301 https://$server_name$request_uri;
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header X-Forwarded-Host $server_name;
    }
    
    location /static/ {
        alias /home/context7/context7-erp/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
    
    location /media/ {
        alias /home/context7/context7-erp/media/;
        expires 30d;
    }
}
EOF

# Enable site
ln -s /etc/nginx/sites-available/intermeks.com /etc/nginx/sites-enabled/
nginx -t
systemctl reload nginx
```

### **Phase 3: Let's Encrypt SSL Certificate** (30 minutes)
```bash
# Install Certbot
apt install certbot python3-certbot-nginx

# Obtain SSL certificate
certbot --nginx -d intermeks.com -d www.intermeks.com

# Test auto-renewal
certbot renew --dry-run

# Setup auto-renewal cron job
echo "0 12 * * * /usr/bin/certbot renew --quiet" | crontab -
```

### **Phase 4: Django HTTPS Configuration** (15 minutes)
```bash
# Update Django settings for HTTPS
cd /home/context7/context7-erp/

# Create production HTTPS settings
cat > dashboard_project/production_https.py << 'EOF'
from .settings import *

# HTTPS Configuration
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Update ALLOWED_HOSTS
ALLOWED_HOSTS = [
    'intermeks.com',
    'www.intermeks.com',
    '31.97.44.248',
    'localhost',
    '127.0.0.1'
]

# Security Headers
SECURE_REFERRER_POLICY = 'strict-origin-when-cross-origin'
SECURE_CROSS_ORIGIN_OPENER_POLICY = 'same-origin'

# Content Security Policy
CSP_DEFAULT_SRC = ("'self'",)
CSP_SCRIPT_SRC = ("'self'", "'unsafe-inline'", "https://cdn.jsdelivr.net")
CSP_STYLE_SRC = ("'self'", "'unsafe-inline'", "https://fonts.googleapis.com")
CSP_FONT_SRC = ("'self'", "https://fonts.gstatic.com")
CSP_IMG_SRC = ("'self'", "data:", "https:")
EOF

# Restart Django with HTTPS settings
systemctl stop context7-erp
systemctl start context7-erp
```

### **Phase 5: Testing & Validation** (20 minutes)
```bash
# Test HTTPS access
curl -I https://intermeks.com
curl -I https://www.intermeks.com

# Test HTTP to HTTPS redirect
curl -I http://intermeks.com

# SSL Labs test (external)
# Visit: https://www.ssllabs.com/ssltest/analyze.html?d=intermeks.com

# Django security check
python manage.py check --deploy --settings=dashboard_project.production_https
```

---

## 🔧 **Implementation Commands**

### **Quick SSL Setup Script**
```bash
#!/bin/bash
# SSL Implementation Script for Context7 ERP

echo "🔐 Starting SSL implementation for Context7 ERP..."

# Phase 1: Nginx Installation
echo "📦 Installing Nginx..."
apt update && apt install -y nginx certbot python3-certbot-nginx
systemctl enable nginx

# Phase 2: Create Nginx config
echo "⚙️ Configuring Nginx..."
cat > /etc/nginx/sites-available/intermeks.com << 'EOF'
server {
    listen 80;
    server_name intermeks.com www.intermeks.com;
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    location /static/ {
        alias /home/context7/context7-erp/staticfiles/;
    }
}
EOF

ln -sf /etc/nginx/sites-available/intermeks.com /etc/nginx/sites-enabled/
nginx -t && systemctl start nginx

# Phase 3: SSL Certificate
echo "🔒 Obtaining SSL certificate..."
certbot --nginx -d intermeks.com -d www.intermeks.com --non-interactive --agree-tos --email admin@intermeks.com

# Phase 4: Auto-renewal
echo "🔄 Setting up auto-renewal..."
echo "0 12 * * * /usr/bin/certbot renew --quiet" | crontab -

echo "✅ SSL implementation completed!"
echo "🌐 Your site is now available at: https://intermeks.com"
```

### **Django HTTPS Update Commands**
```bash
# Update Django settings
cd /home/context7/context7-erp/
export DJANGO_SETTINGS_MODULE=dashboard_project.production_https

# Test configuration
python manage.py check --deploy

# Restart with HTTPS settings
systemctl restart context7-erp

# Verify HTTPS is working
curl -I https://intermeks.com
```

---

## 🔍 **SSL Testing Checklist**

### **Automated Tests**
```bash
# SSL Certificate Validation
openssl s_client -connect intermeks.com:443 -servername intermeks.com

# Security Headers Check
curl -I https://intermeks.com | grep -i security

# HSTS Header Verification
curl -I https://intermeks.com | grep -i strict-transport-security

# Django Security Check
python manage.py check --deploy --settings=dashboard_project.production_https
```

### **Manual Verification**
| Test | URL | Expected | Status |
|------|-----|----------|--------|
| **HTTPS Access** | https://intermeks.com | Site loads | ⏳ PENDING |
| **HTTP Redirect** | http://intermeks.com | Redirects to HTTPS | ⏳ PENDING |
| **SSL Certificate** | Browser check | Valid certificate | ⏳ PENDING |
| **Security Headers** | Developer tools | Headers present | ⏳ PENDING |
| **SSL Labs Test** | External test | A+ rating | ⏳ PENDING |

---

## 📊 **SSL Performance Impact**

### **Expected Changes**
- **Response Time**: +10-20ms (TLS handshake)
- **Security Score**: 85/100 → 100/100
- **SEO Benefits**: HTTPS ranking boost
- **User Trust**: Secure padlock icon
- **Compliance**: GDPR/PCI DSS requirements

### **Monitoring Metrics**
```bash
# SSL Certificate Expiry Monitoring
echo "0 6 * * * /usr/local/bin/check_ssl_expiry.sh" | crontab -

# Create monitoring script
cat > /usr/local/bin/check_ssl_expiry.sh << 'EOF'
#!/bin/bash
DOMAIN="intermeks.com"
EXPIRY_DATE=$(echo | openssl s_client -servername $DOMAIN -connect $DOMAIN:443 2>/dev/null | openssl x509 -noout -dates | grep notAfter | cut -d= -f2)
DAYS_LEFT=$(( ($(date -d "$EXPIRY_DATE" +%s) - $(date +%s)) / 86400 ))

if [ $DAYS_LEFT -lt 30 ]; then
    echo "⚠️ SSL certificate for $DOMAIN expires in $DAYS_LEFT days"
    # Send alert notification
fi
EOF

chmod +x /usr/local/bin/check_ssl_expiry.sh
```

---

## 🚨 **Troubleshooting Guide**

### **Common Issues & Solutions**

#### **Issue 1: DNS Not Propagated**
```bash
# Check DNS propagation
nslookup intermeks.com
dig intermeks.com @8.8.8.8

# Wait for propagation (up to 48 hours)
# Use online tools: whatsmydns.net
```

#### **Issue 2: Certbot Fails**
```bash
# Check domain accessibility
curl -I http://intermeks.com

# Verify Nginx configuration
nginx -t

# Check firewall
ufw status
ufw allow 80
ufw allow 443
```

#### **Issue 3: Mixed Content Errors**
```bash
# Update Django templates
# Change http:// links to https:// or //
# Update STATIC_URL and MEDIA_URL in settings
```

#### **Issue 4: Redirect Loops**
```bash
# Check proxy headers in Nginx
proxy_set_header X-Forwarded-Proto $scheme;

# Update Django settings
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
```

---

## 🎯 **Success Criteria**

### **SSL Implementation Goals**
- [ ] **SSL Certificate**: Valid Let's Encrypt certificate
- [ ] **HTTPS Redirect**: HTTP automatically redirects to HTTPS
- [ ] **Security Headers**: All security headers implemented
- [ ] **SSL Labs Score**: A+ rating achieved
- [ ] **Django Security**: All security checks pass
- [ ] **Auto-Renewal**: Certificate auto-renewal working
- [ ] **Performance**: Response time impact <20ms
- [ ] **Monitoring**: SSL expiry monitoring active

### **Quality Gates**
- [ ] **No Mixed Content**: All resources load over HTTPS
- [ ] **Valid Certificate**: Certificate valid and trusted
- [ ] **Security Headers**: HSTS, CSP, XSS protection active
- [ ] **Django Compliance**: `manage.py check --deploy` passes
- [ ] **External Validation**: SSL Labs A+ rating

---

## 📅 **Implementation Timeline**

### **Immediate (Today)**
- [x] ✅ Create SSL implementation plan
- [ ] ⏳ Configure DNS settings (if not done)
- [ ] ⏳ Install and configure Nginx

### **This Week**
- [ ] ⏳ Obtain Let's Encrypt certificate
- [ ] ⏳ Configure Django HTTPS settings
- [ ] ⏳ Test SSL implementation
- [ ] ⏳ Set up monitoring and auto-renewal

### **Next Week**
- [ ] 📋 Monitor SSL performance
- [ ] 📋 Optimize HTTPS configuration
- [ ] 📋 Document SSL procedures
- [ ] 📋 Create SSL maintenance guide

---

## 📞 **Next Steps**

### **Priority Actions**
1. **Domain DNS Configuration**: Point intermeks.com to 31.97.44.248
2. **Nginx Installation**: Set up reverse proxy
3. **SSL Certificate**: Obtain Let's Encrypt certificate
4. **Django Configuration**: Enable HTTPS settings
5. **Testing & Validation**: Comprehensive SSL testing

### **Dependencies**
- **DNS Access**: Domain provider credentials needed
- **VPS Access**: Root SSH access to 31.97.44.248
- **Domain Ownership**: Verification for SSL certificate

---

**🎯 Goal**: Implement enterprise-grade HTTPS security with A+ SSL Labs rating

**📝 Status**: SSL implementation plan ready for execution

**🔗 Related Tasks**: 
- [ ] **[TYPE: SECURITY] SSL Certificate Setup**: Production HTTPS configuration
- [ ] **[TYPE: DEPLOYMENT] Nginx Setup**: Production web server
- [ ] **[TYPE: SECURITY] Security Headers Enhancement**: Advanced security 