# 🔐 Authentication & Authorization Module

**Module:** Authentication & Authorization System  
**Version:** v2.2.0-glassmorphism-enhanced  
**Status:** ✅ Production Ready (100% Complete)  
**Last Updated:** 12 Ocak 2025  
**QMS Reference:** REC-AUTH-FEATURES-250112-002

---

## 📋 **Module Overview**

Authentication & Authorization modülü, Context7 ERP sisteminin güvenlik omurgasını oluşturur. Modern JWT tabanlı authentication, role-based access control ve enterprise-grade security features sağlar.

### **🎯 Purpose & Business Value**
- **Secure Access:** Güvenli kullanıcı kimlik doğrulaması
- **Role Management:** Departman ve rol bazlı erişim kontrolü
- **Session Security:** Güvenli oturum yönetimi
- **Audit Trail:** Kullanıcı aktivitelerinin izlenmesi
- **Compliance:** Enterprise security standartlarına uyum

### **👥 Target Users**
- **System Administrators:** User management ve security configuration
- **IT Managers:** Security policy implementation
- **Department Managers:** Team access management
- **End Users:** Secure system access

---

## 🏗️ **Technical Architecture**

### **📁 File Structure**
```
users/
├── __init__.py
├── apps.py                     # Django app configuration
├── admin.py                    # Admin interface for user management
├── models.py                   # User, Role, Permission models
├── views.py                    # Authentication views
├── forms.py                    # Authentication forms
├── urls.py                     # URL patterns
├── serializers.py              # API serializers
├── permissions.py              # Custom permission classes
├── middleware.py               # Authentication middleware
├── utils.py                    # Authentication utilities
├── migrations/                 # Database migrations
└── templates/
    └── users/
        ├── login.html          # Login page
        ├── logout.html         # Logout confirmation
        ├── profile.html        # User profile
        └── password_reset.html # Password reset
```

### **🗄️ Models & Database Schema**

#### **Extended User Model**
```python
class User(AbstractUser):
    """Extended Django User model with ERP-specific fields"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    employee = models.OneToOneField('erp.Employee', on_delete=models.SET_NULL, null=True, blank=True)
    department = models.ForeignKey('erp.Department', on_delete=models.SET_NULL, null=True)
    phone = models.CharField(max_length=20, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    timezone = models.CharField(max_length=50, default='Europe/Istanbul')
    language = models.CharField(max_length=10, choices=[('tr', 'Turkish'), ('en', 'English')], default='tr')
    is_department_manager = models.BooleanField(default=False)
    last_login_ip = models.GenericIPAddressField(null=True, blank=True)
    failed_login_attempts = models.PositiveIntegerField(default=0)
    account_locked_until = models.DateTimeField(null=True, blank=True)
    password_changed_at = models.DateTimeField(auto_now_add=True)
    must_change_password = models.BooleanField(default=False)
    two_factor_enabled = models.BooleanField(default=False)
    two_factor_secret = models.CharField(max_length=32, blank=True)
```

#### **Role Model**
```python
class Role(Context7BaseModel):
    """Role definition for RBAC system"""
    
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True)
    department = models.ForeignKey('erp.Department', on_delete=models.SET_NULL, null=True)
    permissions = models.ManyToManyField('auth.Permission', blank=True)
    is_system_role = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['name']
        verbose_name = 'Role'
        verbose_name_plural = 'Roles'
```

#### **UserSession Model**
```python
class UserSession(Context7BaseModel):
    """Track user sessions for security monitoring"""
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    session_key = models.CharField(max_length=40, unique=True)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField()
    login_time = models.DateTimeField(auto_now_add=True)
    logout_time = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    device_info = models.JSONField(default=dict)
```

#### **UserActivity Model**
```python
class UserActivity(Context7BaseModel):
    """Log user activities for audit trail"""
    
    ACTION_TYPES = [
        ('login', 'Login'),
        ('logout', 'Logout'),
        ('view', 'View'),
        ('create', 'Create'),
        ('update', 'Update'),
        ('delete', 'Delete'),
        ('export', 'Export'),
        ('import', 'Import'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=20, choices=ACTION_TYPES)
    object_type = models.CharField(max_length=50, blank=True)
    object_id = models.CharField(max_length=50, blank=True)
    description = models.TextField()
    ip_address = models.GenericIPAddressField()
    timestamp = models.DateTimeField(auto_now_add=True)
    additional_data = models.JSONField(default=dict)
```

---

## ⚙️ **Features & Functionality**

### **🔥 Core Authentication Features**

#### **1. JWT Authentication**
- **Token-based Authentication:** Stateless JWT tokens
- **Refresh Token Support:** Secure token renewal
- **Token Blacklisting:** Revoked token management
- **Configurable Expiry:** Customizable token lifetimes

```python
# JWT Configuration
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
}
```

#### **2. Multi-Factor Authentication (2FA)**
- **TOTP Support:** Time-based one-time passwords
- **QR Code Generation:** Easy setup via authenticator apps
- **Backup Codes:** Emergency access codes
- **Conditional 2FA:** Role-based 2FA requirements

#### **3. Session Management**
- **Concurrent Session Control:** Limit concurrent logins
- **Session Timeout:** Automatic logout after inactivity
- **Device Tracking:** Monitor login devices
- **Remote Logout:** Admin capability to terminate sessions

#### **4. Password Security**
- **Password Complexity:** Configurable password rules
- **Password History:** Prevent password reuse
- **Account Lockout:** Brute force protection
- **Password Expiry:** Configurable password expiration

### **🛡️ Authorization Features**

#### **1. Role-Based Access Control (RBAC)**
- **Hierarchical Roles:** Department ve system roles
- **Permission Granularity:** Fine-grained permissions
- **Dynamic Permissions:** Runtime permission evaluation
- **Permission Inheritance:** Role hierarchy support

#### **2. Department-Based Access**
- **Data Isolation:** Department-specific data access
- **Cross-Department Rules:** Configurable cross-access
- **Manager Privileges:** Enhanced access for managers
- **Delegation Support:** Temporary access delegation

#### **3. Resource-Level Permissions**
- **Object-Level Security:** Per-record access control
- **Field-Level Security:** Sensitive field protection
- **Action-Based Permissions:** Create, read, update, delete controls
- **Conditional Access:** Context-aware permissions

### **🔒 Security Features**

#### **1. Advanced Security Middleware**
```python
class AdvancedSecurityMiddleware:
    """Comprehensive security middleware"""
    
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        # IP-based access control
        self.check_ip_whitelist(request)
        
        # Rate limiting
        self.apply_rate_limiting(request)
        
        # Security headers
        response = self.get_response(request)
        self.add_security_headers(response)
        
        # Activity logging
        self.log_user_activity(request)
        
        return response
```

#### **2. Audit Trail**
- **Complete Activity Log:** All user actions logged
- **Forensic Analysis:** Detailed investigation capabilities
- **Compliance Reporting:** Regulatory compliance reports
- **Real-time Monitoring:** Live activity monitoring

#### **3. IP-Based Security**
- **IP Whitelisting:** Restrict access by IP address
- **Geolocation Tracking:** Monitor login locations
- **VPN Detection:** Identify VPN usage
- **Risk Assessment:** Automated risk scoring

---

## 🔧 **Configuration & Setup**

### **📦 Dependencies**
```python
# requirements.txt entries for authentication
djangorestframework-simplejwt>=5.2.0
django-otp>=1.1.3              # 2FA support
django-ratelimit>=3.0.1        # Rate limiting
geoip2>=4.6.0                  # Geolocation
qrcode>=7.3.1                  # QR code generation
```

### **⚙️ Security Settings**
```python
# settings.py - Authentication specific settings
AUTH_CONFIG = {
    'MAX_LOGIN_ATTEMPTS': 5,
    'ACCOUNT_LOCKOUT_DURATION': 900,  # 15 minutes
    'SESSION_TIMEOUT': 3600,  # 1 hour
    'PASSWORD_RESET_TIMEOUT': 3600,  # 1 hour
    'REQUIRE_2FA_FOR_ADMIN': True,
    'ENABLE_IP_WHITELISTING': False,
    'LOG_ALL_ACTIVITIES': True,
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {'min_length': 8,}
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
    {
        'NAME': 'users.validators.CustomPasswordValidator',
        'OPTIONS': {
            'require_uppercase': True,
            'require_lowercase': True,
            'require_digits': True,
            'require_special_chars': True,
        }
    },
]
```

### **🌐 URL Configuration**
```python
# users/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

router = DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'roles', views.RoleViewSet)

urlpatterns = [
    # Web interface
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('password/change/', views.PasswordChangeView.as_view(), name='password_change'),
    path('2fa/setup/', views.TwoFactorSetupView.as_view(), name='2fa_setup'),
    
    # API endpoints
    path('api/token/', views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/blacklist/', views.TokenBlacklistView.as_view(), name='token_blacklist'),
    path('api/', include(router.urls)),
]
```

---

## 📚 **User Guide**

### **🚀 Getting Started**

#### **1. User Registration & Setup**
1. Admin creates user account
2. User receives setup email with temporary password
3. User completes profile setup
4. Optional 2FA configuration

#### **2. Login Process**
1. Enter username/email ve password
2. Complete 2FA if enabled
3. Accept terms if updated
4. Redirect to dashboard

#### **3. Profile Management**
- **Personal Information:** Update contact details
- **Security Settings:** Change password, setup 2FA
- **Preferences:** Language, timezone, notifications
- **Session Management:** View active sessions

### **🔐 Security Best Practices**

#### **For Users**
- Use strong, unique passwords
- Enable 2FA for enhanced security
- Regularly review active sessions
- Report suspicious activities
- Keep contact information updated

#### **For Administrators**
- Regularly review user permissions
- Monitor failed login attempts
- Implement IP whitelisting if needed
- Regular security audits
- Keep security policies updated

### **👥 Role Management**

#### **Creating Roles**
```python
# Example role creation
admin_role = Role.objects.create(
    name='ERP Administrator',
    code='erp_admin',
    description='Full system administration access',
    is_system_role=True
)

# Assign permissions
admin_role.permissions.add(
    Permission.objects.get(codename='add_user'),
    Permission.objects.get(codename='change_user'),
    Permission.objects.get(codename='delete_user'),
)
```

#### **Department-Based Roles**
- **Sales Manager:** Sales module full access
- **Finance User:** Finance module read/write
- **Production Supervisor:** Production monitoring
- **Quality Inspector:** Quality control functions

---

## 🧪 **Testing & Quality**

### **📊 Security Testing**
- **Penetration Testing:** Regular security assessments
- **Vulnerability Scanning:** Automated security scans
- **Authentication Testing:** Login flow validation
- **Authorization Testing:** Permission enforcement
- **Session Security:** Session hijacking prevention

### **⚡ Performance Metrics**
- **Login Time:** <500ms average
- **Token Validation:** <50ms average
- **Permission Check:** <10ms average
- **Session Lookup:** <20ms average

### **🔒 Compliance Standards**
- **GDPR:** Data protection compliance
- **ISO 27001:** Information security management
- **OWASP:** Web application security standards
- **SOX:** Financial reporting compliance

---

## 🔗 **Integration**

### **📡 API Authentication**
```python
# API authentication example
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def protected_endpoint(request):
    return Response({'user': request.user.username})
```

### **🔄 External System Integration**
- **LDAP/Active Directory:** Enterprise directory integration
- **SAML SSO:** Single sign-on capability
- **OAuth2:** Third-party authentication
- **API Keys:** Service-to-service authentication

### **📊 Monitoring Integration**
- **Sentry:** Error tracking ve alerting
- **Prometheus:** Performance metrics
- **ELK Stack:** Log analysis
- **Custom Dashboards:** Security monitoring

---

## 📈 **Maintenance & Support**

### **🔄 Regular Maintenance**
- **Weekly:** Review failed login attempts
- **Monthly:** Audit user permissions
- **Quarterly:** Security policy review
- **Yearly:** Penetration testing

### **🛠️ Common Issues & Solutions**

#### **Account Lockouts**
```python
# Unlock user account
user = User.objects.get(username='username')
user.failed_login_attempts = 0
user.account_locked_until = None
user.save()
```

#### **Password Reset Issues**
- Verify email configuration
- Check password complexity requirements
- Ensure token validity period

#### **2FA Problems**
- Verify time synchronization
- Check authenticator app setup
- Provide backup codes

### **📊 Security Monitoring**
- **Failed Login Monitoring:** Alert on suspicious patterns
- **Permission Changes:** Track role modifications
- **Session Anomalies:** Unusual session patterns
- **Geographic Analysis:** Login location analysis

---

**🎯 Mission:** Provide enterprise-grade authentication ve authorization capabilities that ensure secure access while maintaining user experience ve operational efficiency.

**📞 QMS Reference:** REC-AUTH-FEATURES-250112-002 - Comprehensive Authentication Module Documentation

---

*Authentication Module - Enterprise Security with User-Friendly Experience* 