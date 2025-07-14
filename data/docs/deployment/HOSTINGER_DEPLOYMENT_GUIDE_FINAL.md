# 🚀 Context7 ERP System - Hostinger Deployment Guide

## 📋 Server Information
- **Host**: srv858543.hstgr.cloud  
- **IP**: 31.97.44.248
- **Root Password**: Qz@2C9E0h9tjq)s6ghtD
- **Admin**: admin / XG3sWT3rDcuRhbhN

## 🎯 Quick Deployment (3 Steps)

### Step 1: Create and Upload Package
```bash
# From your local machine
chmod +x hostinger_deployment_package.sh
./hostinger_deployment_package.sh
```

### Step 2: Connect and Deploy
```bash
# Connect to server
ssh root@31.97.44.248

# Extract and deploy
cd /tmp
tar -xzf context7-erp-hostinger-*.tar.gz
cd context7-erp-hostinger-*
chmod +x hostinger_deploy_final.sh
./hostinger_deploy_final.sh
```

### Step 3: Start Server
```bash
sudo systemctl start context7-erp
sudo systemctl enable context7-erp
```

## 🌐 Access System

- **Main Site**: http://31.97.44.248
- **Admin Panel**: http://31.97.44.248/admin/
- **API**: http://31.97.44.248/api/

## 🔧 Manual Deployment (Fallback)

If automated deployment fails:

```bash
# 1. Upload files
tar -czf context7-erp.tar.gz . --exclude='venv' --exclude='__pycache__' --exclude='.git'
scp context7-erp.tar.gz root@31.97.44.248:/tmp/

# 2. Connect and setup
ssh root@31.97.44.248
cd /tmp && tar -xzf context7-erp.tar.gz

# 3. Install dependencies
apt-get update
apt-get install -y python3 python3-pip python3-venv nginx supervisor redis-server

# 4. Setup project
useradd -m -s /bin/bash context7
echo "context7:s6ghtD.fdSSadasf" | chpasswd
mkdir -p /home/context7/context7-erp
cp -r context7-erp/* /home/context7/context7-erp/
chown -R context7:context7 /home/context7/

# 5. Configure application
su - context7
cd /home/context7/context7-erp
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 6. Setup environment
cat > .env << 'EOF'
DEBUG=False
SECRET_KEY=your-secret-key-here
DJANGO_SETTINGS_MODULE=dashboard_project.sqlite_settings
DATABASE_URL=sqlite:///$(pwd)/db.sqlite3
ALLOWED_HOSTS=31.97.44.248,srv858543.hstgr.cloud,localhost,127.0.0.1
STATIC_ROOT=$(pwd)/staticfiles
MEDIA_ROOT=$(pwd)/media
EOF

# 7. Initialize Django
export DJANGO_SETTINGS_MODULE=dashboard_project.sqlite_settings
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser --username admin --email admin@intermeks.com
```

## 🎯 System Management

### Service Commands
```bash
# Start/stop/restart service
sudo systemctl start|stop|restart context7-erp

# Check status and logs
sudo systemctl status context7-erp
sudo journalctl -u context7-erp -f
```

### Database Management
```bash
su - context7
cd /home/context7/context7-erp
source venv/bin/activate
python manage.py migrate
python manage.py collectstatic --noinput
```

## 🚨 Troubleshooting

### Common Fixes
```bash
# Permission issues
sudo chown -R context7:context7 /home/context7/
sudo chmod -R 755 /home/context7/context7-erp/

# Port conflict
sudo netstat -tlnp | grep 8000
sudo kill -9 <process_id>

# Database issues
python manage.py migrate --run-syncdb

# Static files
python manage.py collectstatic --noinput --clear
```

### Log Locations
- **Service logs**: `journalctl -u context7-erp`
- **System logs**: `/var/log/syslog`
- **Nginx logs**: `/var/log/nginx/access.log`

## 📊 System Features

- **Framework**: Django 5.2.3 + Context7 Glassmorphism v2.2.0
- **Database**: SQLite (production-ready)
- **API**: Django REST Framework with JWT
- **Security**: Multi-tier rate limiting, XSS protection, CSRF
- **ERP Modules**: Sales, Purchasing, Production, Inventory, Finance, HR, Quality Control, Work Orders

## ✅ Deployment Checklist

- [ ] Server accessible via SSH
- [ ] Deployment package uploaded
- [ ] Dependencies installed
- [ ] Database migrated
- [ ] Admin user created
- [ ] Service running
- [ ] System accessible via browser (http://31.97.44.248)
- [ ] Admin panel working (admin/XG3sWT3rDcuRhbhN)

## 📞 Support

**Quick diagnostics**:
```bash
sudo systemctl status context7-erp
sudo journalctl -u context7-erp -f
curl -I http://localhost:8000
```

**System Status**: http://31.97.44.248 | Admin: admin/XG3sWT3rDcuRhbhN 