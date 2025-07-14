# 🚀 Context7 ERP - GitHub + OpenLiteSpeed Deployment Guide

**Repository**: https://github.com/alidurmus/python-dashboard.git

## 📋 Overview

This guide will help you deploy Context7 ERP system from GitHub repository using OpenLiteSpeed web server. OpenLiteSpeed provides high performance and enterprise-grade features for Django applications.

### 🎯 What You'll Get:
- **High Performance**: OpenLiteSpeed web server optimized for Django
- **Easy Management**: Web-based admin console
- **Production Ready**: Enterprise features and caching
- **GitHub Integration**: Direct deployment from repository
- **Modern UI**: Context7 Glassmorphism design

---

## 📋 Prerequisites

### Server Requirements:
- **OS**: Ubuntu 20.04+ / Debian 11+ / CentOS 8+
- **RAM**: Minimum 2GB (4GB recommended)
- **Storage**: 20GB+ available space
- **Network**: Public IP address

### Access Requirements:
- **Root access** to the server
- **GitHub account** with repository access
- **Domain name** (optional, can use IP)

---

## 🚀 **STEP 1: Install OpenLiteSpeed** ⏱️ 5 minutes

### Option A: One-Click Installation Script
```bash
# Download and run OpenLiteSpeed installation script
wget https://raw.githubusercontent.com/litespeedtech/ols1clk/master/ols1clk.sh
chmod +x ols1clk.sh
./ols1clk.sh
```

### Option B: Repository Installation (Ubuntu/Debian)
```bash
# Add LiteSpeed repository
wget -O - http://rpms.litespeedtech.com/debian/enable_lst_debian_repo.sh | bash

# Update package list
apt-get update

# Install OpenLiteSpeed
apt-get install openlitespeed

# Start and enable OpenLiteSpeed
systemctl start lsws
systemctl enable lsws
```

### Option C: Repository Installation (CentOS/RHEL)
```bash
# Add LiteSpeed repository
rpm -Uvh http://rpms.litespeedtech.com/centos/litespeed-repo-1.1-1.el8.noarch.rpm

# Install OpenLiteSpeed
yum install openlitespeed

# Start and enable OpenLiteSpeed
systemctl start lsws
systemctl enable lsws
```

---

## 🔧 **STEP 2: Configure OpenLiteSpeed** ⏱️ 3 minutes

### Set Admin Password
```bash
# Set WebAdmin console password
/usr/local/lsws/admin/misc/admpass.sh
```

### Access WebAdmin Console
- **URL**: `https://YOUR-SERVER-IP:7080`
- **Username**: `admin`
- **Password**: (password you just set)

---

## 🐍 **STEP 3: Install Python and Dependencies** ⏱️ 5 minutes

### Install Python and Development Tools
```bash
# Ubuntu/Debian
apt-get update
apt-get install -y python3 python3-pip python3-venv python3-dev \
                   postgresql postgresql-contrib libpq-dev \
                   git curl wget unzip build-essential \
                   redis-server supervisor

# CentOS/RHEL
yum groupinstall -y "Development Tools"
yum install -y python3 python3-pip python3-devel \
               postgresql postgresql-server postgresql-devel \
               git curl wget unzip redis \
               supervisor
```

### Install Python LSAPI
```bash
# Download Python LSAPI
cd /tmp
curl -O http://www.litespeedtech.com/packages/lsapi/wsgi-lsapi-2.1.tgz
tar xf wsgi-lsapi-2.1.tgz
cd wsgi-lsapi-2.1

# Compile and install
python3 ./configure.py
make
cp lswsgi /usr/local/lsws/fcgi-bin/
chmod +x /usr/local/lsws/fcgi-bin/lswsgi
```

---

## 📦 **STEP 4: Deploy Context7 ERP from GitHub** ⏱️ 10 minutes

### Create Project User and Directories
```bash
# Create context7 user
useradd -m -s /bin/bash context7
passwd context7

# Create project directories
mkdir -p /usr/local/lsws/Example/html
cd /usr/local/lsws/Example/html

# Set up project structure
mkdir -p {lib/python3.8/site-packages,bin,logs,static,media}
```

### Clone Repository and Setup
```bash
# Switch to context7 user
su - context7

# Clone Context7 ERP repository
cd /usr/local/lsws/Example/html
git clone https://github.com/alidurmus/python-dashboard.git context7_project

# Copy project files to proper location
cp -r context7_project/* lib/python3.8/site-packages/
cd lib/python3.8/site-packages
```

### Create Virtual Environment
```bash
# Create virtual environment
python3 -m venv /usr/local/lsws/Example/html/venv
source /usr/local/lsws/Example/html/venv/bin/activate

# Create symlink for easier access
ln -sf /usr/local/lsws/Example/html/venv/bin/python /usr/local/lsws/Example/html/bin/python
```

### Install Dependencies
```bash
# Install Python packages
pip install --upgrade pip
pip install -r requirements.txt

# Install to site-packages location
pip install --target /usr/local/lsws/Example/html/lib/python3.8/site-packages -r requirements.txt
```

---

## ⚙️ **STEP 5: Configure Django Application** ⏱️ 8 minutes

### Create Production Settings
```bash
# Navigate to project directory
cd /usr/local/lsws/Example/html/lib/python3.8/site-packages

# Create production environment file
cat > .env << 'EOF'
# Context7 ERP - Production Environment
DEBUG=False
SECRET_KEY=your-secret-key-here
DJANGO_SETTINGS_MODULE=dashboard_project.sqlite_settings

# Server Configuration
ALLOWED_HOSTS=your-server-ip,your-domain.com,localhost,127.0.0.1

# Database (SQLite for simplicity)
DATABASE_URL=sqlite:///db.sqlite3

# Static Files
STATIC_ROOT=/usr/local/lsws/Example/html/static/
MEDIA_ROOT=/usr/local/lsws/Example/html/media/

# Cache and Performance
ENABLE_CACHING=True
RATE_LIMITING_ENABLED=True
EOF
```

### Django Setup Commands
```bash
# Set environment variable
export DJANGO_SETTINGS_MODULE=dashboard_project.sqlite_settings

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Create superuser
python manage.py createsuperuser

# Load sample data (if available)
if [ -f "sample_data/create_comprehensive_sample_data.py" ]; then
    python sample_data/create_comprehensive_sample_data.py
fi
```

### Create WSGI Configuration
```bash
# Create wsgi.py if not exists
cat > wsgi.py << 'EOF'
import os
import sys
import django
from django.core.wsgi import get_wsgi_application

# Add project directory to Python path
sys.path.insert(0, '/usr/local/lsws/Example/html/lib/python3.8/site-packages')

# Set environment variable
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard_project.sqlite_settings')

# Initialize Django
django.setup()

# Get WSGI application
application = get_wsgi_application()
EOF
```

---

## 🌐 **STEP 6: Configure OpenLiteSpeed Virtual Host** ⏱️ 10 minutes

### Access WebAdmin Console
1. Open browser: `https://YOUR-SERVER-IP:7080`
2. Login with admin credentials

### Configure Virtual Host Context

#### Step 6.1: Create App Server Context
Navigate to **Virtual Hosts > Example > Context** and **Add** new **App Server** context:

**General Settings:**
- **Type**: `App Server`
- **URI**: `/`
- **Location**: `/usr/local/lsws/Example/html/lib/python3.8/site-packages/`
- **Binary Path**: `/usr/local/lsws/fcgi-bin/lswsgi`
- **Application Type**: `WSGI`

**Script Handler:**
- **Suffixes**: `py`
- **Script Path**: `/usr/local/lsws/fcgi-bin/lswsgi`

**App Server Settings:**
- **Startup File**: `wsgi.py`
- **Application Type**: `WSGI`
- **Module Name**: `wsgi`

**Environment Variables:**
```
PYTHONPATH=/usr/local/lsws/Example/html/lib/python3.8:/usr/local/lsws/Example/html/lib/python3.8/site-packages
LS_PYTHONBIN=/usr/local/lsws/Example/html/bin/python
DJANGO_SETTINGS_MODULE=dashboard_project.sqlite_settings
```

#### Step 6.2: Create Static Files Context
**Add** new **Static** context:

- **Type**: `Static`
- **URI**: `/static/`
- **Location**: `/usr/local/lsws/Example/html/static/`
- **Accessible**: `Yes`
- **Index Files**: `index.html`

#### Step 6.3: Create Media Files Context
**Add** new **Static** context:

- **Type**: `Static`
- **URI**: `/media/`
- **Location**: `/usr/local/lsws/Example/html/media/`
- **Accessible**: `Yes`

### Configure Listeners
Navigate to **Listeners** and ensure:
- **HTTP Listener**: Port 80, IP `*`
- **HTTPS Listener**: Port 443, IP `*` (if SSL configured)

---

## 🔒 **STEP 7: Set Permissions** ⏱️ 2 minutes

```bash
# Set ownership to nobody:nogroup (OpenLiteSpeed user)
chown -R nobody:nogroup /usr/local/lsws/Example/html/

# Set proper permissions
chmod -R 755 /usr/local/lsws/Example/html/
chmod +x /usr/local/lsws/Example/html/bin/python
chmod +x /usr/local/lsws/fcgi-bin/lswsgi

# Ensure database file is writable
chmod 664 /usr/local/lsws/Example/html/lib/python3.8/site-packages/db.sqlite3
chown nobody:nogroup /usr/local/lsws/Example/html/lib/python3.8/site-packages/db.sqlite3
```

---

## 🎯 **STEP 8: Enable LSCache (Optional Performance Boost)** ⏱️ 3 minutes

### Configure Cache Rules
In **Virtual Hosts > Example > Context > App Server**, add **Rewrite Rules**:

```apache
# Enable LSCache for Context7 ERP
CacheLookup on

# Cache all pages except admin and API endpoints
RewriteCond %{REQUEST_URI} !^/admin/
RewriteCond %{REQUEST_URI} !^/api/
RewriteRule .* - [E=cache-control:max-age=300]

# Cache static files for longer
RewriteCond %{REQUEST_URI} ^/static/
RewriteRule .* - [E=cache-control:max-age=86400]

# Cache media files
RewriteCond %{REQUEST_URI} ^/media/
RewriteRule .* - [E=cache-control:max-age=86400]
```

---

## 🔄 **STEP 9: Restart and Test** ⏱️ 2 minutes

### Restart OpenLiteSpeed
```bash
# Restart the web server
systemctl restart lsws

# Check status
systemctl status lsws
```

### Test the Installation
1. **Main Website**: `http://YOUR-SERVER-IP`
2. **Admin Panel**: `http://YOUR-SERVER-IP/admin/`
3. **API Endpoint**: `http://YOUR-SERVER-IP/api/v1/`

### Expected Results:
- ✅ Context7 ERP dashboard loads
- ✅ Modern glassmorphism UI displays
- ✅ Admin panel accessible
- ✅ All 8 ERP modules working
- ✅ Fast page load times with LSCache

---

## 📊 **STEP 10: Post-Deployment Configuration** ⏱️ 5 minutes

### Database Setup (PostgreSQL - Optional)
```bash
# If you prefer PostgreSQL over SQLite
sudo -u postgres createdb context7_erp
sudo -u postgres createuser context7
sudo -u postgres psql -c "ALTER USER context7 PASSWORD 'your-password';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE context7_erp TO context7;"

# Update .env file
# DATABASE_URL=postgresql://context7:password@localhost/context7_erp
```

### SSL Certificate Setup
```bash
# Install Certbot for Let's Encrypt
apt-get install certbot

# Get SSL certificate
certbot certonly --webroot -w /usr/local/lsws/Example/html -d your-domain.com

# Configure SSL in OpenLiteSpeed WebAdmin Console
# SSL Tab: Private Key File: /etc/letsencrypt/live/your-domain.com/privkey.pem
# SSL Tab: Certificate File: /etc/letsencrypt/live/your-domain.com/fullchain.pem
```

### Monitoring and Logs
```bash
# View OpenLiteSpeed access logs
tail -f /usr/local/lsws/logs/access.log

# View error logs
tail -f /usr/local/lsws/logs/error.log

# View Django application logs
tail -f /usr/local/lsws/Example/html/logs/django.log
```

---

## 🔄 **Auto-Update from GitHub** 

### Create Update Script
```bash
cat > /home/context7/update_from_github.sh << 'EOF'
#!/bin/bash
echo "🔄 Updating Context7 ERP from GitHub..."

cd /usr/local/lsws/Example/html/lib/python3.8/site-packages
source /usr/local/lsws/Example/html/venv/bin/activate

# Backup current version
cp -r . /home/context7/backup-$(date +%Y%m%d_%H%M%S)

# Pull latest changes
git pull origin main

# Install/update dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Set permissions
chown -R nobody:nogroup /usr/local/lsws/Example/html/

# Restart web server
systemctl restart lsws

echo "✅ Update completed successfully!"
EOF

chmod +x /home/context7/update_from_github.sh
```

### Setup Automatic Updates (Cron)
```bash
# Add to crontab for weekly updates
crontab -e

# Add line for weekly updates (every Sunday at 2 AM)
0 2 * * 0 /home/context7/update_from_github.sh >> /var/log/context7_updates.log 2>&1
```

---

## 🛠️ **Troubleshooting**

### Common Issues and Solutions

#### Issue 1: 500 Internal Server Error
```bash
# Check error logs
tail -f /usr/local/lsws/logs/error.log

# Check Python path and permissions
ls -la /usr/local/lsws/Example/html/lib/python3.8/site-packages/
chown -R nobody:nogroup /usr/local/lsws/Example/html/
```

#### Issue 2: Static Files Not Loading
```bash
# Verify static context configuration
# Check that URI: /static/ points to correct location
# Ensure files exist: ls -la /usr/local/lsws/Example/html/static/

# Recollect static files
cd /usr/local/lsws/Example/html/lib/python3.8/site-packages
python manage.py collectstatic --noinput
```

#### Issue 3: Database Connection Error
```bash
# Check database file permissions
ls -la /usr/local/lsws/Example/html/lib/python3.8/site-packages/db.sqlite3
chmod 664 db.sqlite3
chown nobody:nogroup db.sqlite3
```

#### Issue 4: WSGI Import Error
```bash
# Verify Python path in environment variables
# Check wsgi.py file exists and has correct imports
# Verify DJANGO_SETTINGS_MODULE is correct
```

### Performance Optimization

#### Enable Compression
In **Virtual Hosts > Example > General**:
- **Enable Compression**: `Yes`
- **Compressible Types**: `text/*, application/javascript, application/json`

#### Tune Worker Processes
In **Server > Tuning**:
- **Max Connections**: `2000`
- **Max SSL Connections**: `1000`
- **Max Keep-Alive Requests**: `1000`

---

## 📈 **Expected Performance**

### Performance Benchmarks:
- **Response Time**: < 200ms (with LSCache)
- **Concurrent Users**: 500+ users
- **Throughput**: 1000+ requests/second
- **Memory Usage**: ~500MB for base installation

### Monitoring Commands:
```bash
# Check server resources
htop
free -h
df -h

# Check OpenLiteSpeed status
/usr/local/lsws/bin/lshttpd -v
systemctl status lsws

# Check cache hit ratio
tail -f /usr/local/lsws/logs/access.log | grep "cache-control"
```

---

## 🎉 **Success Checklist**

### ✅ **Deployment Complete When:**
- [ ] OpenLiteSpeed running on port 80/443
- [ ] Context7 ERP accessible at your domain/IP
- [ ] Admin panel working: `/admin/`
- [ ] All 8 ERP modules accessible
- [ ] Modern glassmorphism UI displaying
- [ ] Static files loading correctly
- [ ] Database operations working
- [ ] LSCache enabled and working
- [ ] SSL certificate installed (if applicable)
- [ ] Auto-update script configured

### 🚀 **Your Context7 ERP System is Ready!**
- **Main Site**: `http://your-domain.com`
- **Admin Panel**: `http://your-domain.com/admin/`
- **API**: `http://your-domain.com/api/v1/`
- **8 ERP Modules**: Inventory, Sales, Production, HR, Finance, Quality Control, Work Orders, Purchasing

---

## 📞 **Support Resources**

### Documentation Links:
- **OpenLiteSpeed Docs**: [https://docs.openlitespeed.org/](https://docs.openlitespeed.org/)
- **Django Cloud Images**: [https://docs.litespeedtech.com/cloud/images/django/](https://docs.litespeedtech.com/cloud/images/django/)
- **Context7 ERP Docs**: [docs/README.md](../README.md)

### Community Support:
- **OpenLiteSpeed Forum**: [https://forum.openlitespeed.org/](https://forum.openlitespeed.org/)
- **LiteSpeed Slack**: [https://litespeedtech.com/slack](https://litespeedtech.com/slack)

---

**📅 Created**: December 29, 2024  
**🔄 Last Updated**: December 29, 2024  
**⚡ Status**: Production Ready  
**🏷️ Version**: v2.2.0-glassmorphism-enhanced  

**🚀 Deploy Context7 ERP with confidence using OpenLiteSpeed!** 