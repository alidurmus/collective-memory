# 🔐 Context7 ERP - SSH Connection Guide

## 📋 Server Information
- **Host**: srv858543.hstgr.cloud
- **IP**: 31.97.44.248
- **User**: root
- **Password**: Qz@2C9E0h9tjq)s6ghtD

---

## 🚀 Connection Methods

### Method 1: Direct SSH (Windows)
```bash
# PowerShell or Command Prompt
ssh root@31.97.44.248
# Enter password when prompted: Qz@2C9E0h9tjq)s6ghtD
```

### Method 2: SSH with Hostname
```bash
ssh root@srv858543.hstgr.cloud
# Enter password when prompted
```

### Method 3: Alternative Port (if standard fails)
```bash
# Try common alternative ports
ssh -p 22 root@31.97.44.248
ssh -p 2222 root@31.97.44.248
```

---

## 🔧 Troubleshooting SSH Issues

### Issue 1: Permission Denied
**Symptom**: `Permission denied (publickey,password)`

**Solutions**:
```bash
# Force password authentication
ssh -o PasswordAuthentication=yes root@31.97.44.248

# Disable strict host key checking
ssh -o StrictHostKeyChecking=no root@31.97.44.248

# Verbose mode for debugging
ssh -v root@31.97.44.248
```

### Issue 2: Connection Timeout
**Solutions**:
```bash
# Check if server is responding
ping 31.97.44.248

# Try with different timeout
ssh -o ConnectTimeout=30 root@31.97.44.248
```

### Issue 3: Host Key Verification Failed
**Solution**:
```bash
# Remove old host key (Windows)
ssh-keygen -R 31.97.44.248
ssh-keygen -R srv858543.hstgr.cloud

# Then retry connection
ssh root@31.97.44.248
```

---

## 🖥️ Alternative Connection Tools

### PuTTY (Windows)
1. Download PuTTY from https://putty.org/
2. **Host Name**: 31.97.44.248
3. **Port**: 22
4. **Connection Type**: SSH
5. **Username**: root
6. **Password**: Qz@2C9E0h9tjq)s6ghtD

### WinSCP (File Transfer + Terminal)
1. **Protocol**: SFTP
2. **Host**: 31.97.44.248
3. **Port**: 22
4. **Username**: root
5. **Password**: Qz@2C9E0h9tjq)s6ghtD

---

## ✅ Once Connected - System Check Commands

### Check System Status
```bash
# System info
uname -a
cat /etc/os-release

# Disk space
df -h

# Memory usage
free -h

# Running services
systemctl status
```

### Check Context7 ERP Status
```bash
# Check if Context7 is running
systemctl status context7-erp

# Check application directory
ls -la /home/context7/
cd /home/context7/context7-erp/

# Check logs
tail -f /home/context7/context7-erp/logs/django.log

# Check database
sudo -u context7 /home/context7/venv/bin/python /home/context7/context7-erp/manage.py check
```

### Check Network & Port Status
```bash
# Check open ports
netstat -tulpn | grep :80
netstat -tulpn | grep :443
netstat -tulpn | grep :8000

# Check firewall
ufw status

# Check nginx/apache
systemctl status nginx
systemctl status apache2
```

---

## 🔄 Quick System Recovery Commands

### Restart Services
```bash
# Restart Context7 ERP
systemctl restart context7-erp

# Restart web server
systemctl restart nginx

# Restart all services
systemctl restart context7-erp nginx
```

### Update Application
```bash
# Navigate to application
cd /home/context7/context7-erp/

# Pull latest changes (if git repo)
git pull origin main

# Update dependencies
/home/context7/venv/bin/pip install -r requirements.txt

# Migrate database
sudo -u context7 /home/context7/venv/bin/python manage.py migrate

# Collect static files
sudo -u context7 /home/context7/venv/bin/python manage.py collectstatic --noinput

# Restart service
systemctl restart context7-erp
```

---

## 📊 Expected System State

### Services Running:
- ✅ context7-erp.service
- ✅ nginx.service  
- ✅ postgresql.service (if using PostgreSQL)

### Directories:
- `/home/context7/context7-erp/` - Application directory
- `/home/context7/venv/` - Python virtual environment
- `/var/log/context7/` - Application logs

### Ports:
- **80**: HTTP (nginx)
- **443**: HTTPS (nginx with SSL)
- **8000**: Django development server (if running)

---

## 🆘 Emergency Commands

### If System is Down:
```bash
# Check all services
systemctl list-units --failed

# Restart all Context7 services
systemctl restart context7-erp nginx postgresql

# Check system resources
top
htop
```

### If Can't Access Website:
```bash
# Check if nginx is serving
curl http://localhost
curl http://31.97.44.248

# Check Django is responding
curl http://localhost:8000
```

---

**Last Updated**: December 29, 2024  
**Next Step**: Once connected, run system check commands to assess current state 