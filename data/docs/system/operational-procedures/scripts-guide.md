# 🛠️ Context7 ERP - Deployment Scripts

## 📋 Available Scripts

### 🚀 **NEW: GitHub + OpenLiteSpeed Deployment**

#### **deploy_github_openlitespeed.sh** ⭐
**Automated deployment from GitHub repository using OpenLiteSpeed web server**

**Features:**
- **One-command deployment** from any GitHub repository
- **OpenLiteSpeed installation** (enterprise-grade web server)
- **Python LSAPI compilation** for optimal performance
- **Virtual environment setup** with all dependencies
- **Production configuration** with security settings
- **Automatic superuser creation**
- **Performance optimization** with LSCache

**Usage:**
```bash
# Make executable
chmod +x deploy_github_openlitespeed.sh

# Run deployment
sudo ./deploy_github_openlitespeed.sh https://github.com/alidurmus/python-dashboard.git

# Or download and run directly
wget https://raw.githubusercontent.com/YOUR-REPO/context7-erp/main/scripts/deploy_github_openlitespeed.sh
chmod +x deploy_github_openlitespeed.sh
sudo ./deploy_github_openlitespeed.sh
```

**Performance:**
- **1000+ requests/second** with LSCache
- **Enterprise-grade** web server performance
- **Web admin console** on port 7080
- **Automatic SSL** support ready

---

### 🗄️ **Database Scripts**

#### **database/start_postgresql.bat**
Windows batch script to start PostgreSQL service

#### **database/start_postgresql_docker.ps1**
PowerShell script to run PostgreSQL in Docker

#### **database/install_postgresql_service.bat**
Install PostgreSQL as Windows service

---

### 🌐 **Web Server Configuration**

#### **nginx/context7.conf**
Nginx configuration for Context7 ERP (if using Nginx instead of OpenLiteSpeed)

#### **systemd/context7.service**
Systemd service configuration for Context7 ERP

---

### 🚀 **Production Deployment**

#### **deploy_production.py**
Python script for production deployment management

#### **deploy_to_hostinger.py**
Specific deployment script for Hostinger VPS

#### **backup_production.sh**
Production backup automation script

---

### ⚙️ **Setup Scripts**

#### **setup/environment_setup.py**
Environment variables and configuration setup

#### **setup/setup_postgresql.py**
PostgreSQL database setup and configuration

---

## 🎯 **Recommended Usage**

### **For New Deployments:**
1. **High Performance**: Use `deploy_github_openlitespeed.sh` for enterprise-grade performance
2. **Standard Deployment**: Use `deploy_to_hostinger.py` for regular VPS deployment
3. **Local Development**: Use database scripts for local setup

### **For Production Management:**
1. **Backups**: Use `backup_production.sh` for automated backups
2. **Monitoring**: Use `deploy_production.py` for production management
3. **Updates**: Use GitHub deployment for automated updates

---

## 📊 **Performance Comparison**

| Script | Web Server | Performance | Complexity | Best For |
|--------|------------|-------------|------------|----------|
| **deploy_github_openlitespeed.sh** | OpenLiteSpeed | **Enterprise (1000+ req/s)** | Medium | **Production** |
| **deploy_to_hostinger.py** | Gunicorn + Nginx | Standard | Easy | **Quick deployment** |
| **deploy_production.py** | Configurable | Depends on config | High | **Custom setups** |

---

## 🔧 **Prerequisites**

### **For OpenLiteSpeed Deployment:**
- **OS**: Ubuntu 20.04+ / Debian 11+ / CentOS 8+
- **RAM**: 2GB+ (4GB recommended)
- **Root access** required
- **GitHub repository** with Context7 ERP

### **For Standard Deployment:**
- **Python 3.8+**
- **Git**
- **Virtual environment support**

---

## 📚 **Documentation Links**

- **OpenLiteSpeed Guide**: [docs/deployment/GITHUB_OPENLITESPEED_DEPLOYMENT.md](../docs/deployment/GITHUB_OPENLITESPEED_DEPLOYMENT.md)
- **Hostinger Guide**: [docs/deployment/HOSTINGER_DEPLOYMENT_GUIDE_FINAL.md](../docs/deployment/HOSTINGER_DEPLOYMENT_GUIDE_FINAL.md)
- **Production Success Report**: [docs/deployment/PRODUCTION_DEPLOYMENT_SUCCESS_REPORT.md](../docs/deployment/PRODUCTION_DEPLOYMENT_SUCCESS_REPORT.md)
- **Monitoring System**: [docs/deployment/CONTEXT7_MONITORING_COMPLETE_REPORT.md](../docs/deployment/CONTEXT7_MONITORING_COMPLETE_REPORT.md)

---

## 🛡️ **Security Notes**

- All scripts require **root privileges** for system modifications
- **Review scripts** before execution on production systems
- **Backup existing installations** before running deployment scripts
- **Test on staging environment** first when possible

---

**📅 Last Updated**: December 29, 2024  
**🚀 Latest Addition**: GitHub + OpenLiteSpeed deployment  
**⚡ Performance**: Enterprise-grade options available  
**🏛️ QMS Compliance**: Central Protocol v1.0 Active  
**QMS Reference**: REC-SYSTEM-SCRIPTS-241229-001 