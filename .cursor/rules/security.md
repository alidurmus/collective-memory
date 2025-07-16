# 🔒 Güvenlik Kuralları

## Veri Güvenliği
- **API Keys**: Environment variables'da sakla
- **Passwords**: Asla hardcode etme
- **Sensitive Data**: .gitignore'a ekle
- **SQL Injection**: ORM kullan, raw SQL yasak
- **XSS Protection**: Input sanitization zorunlu

## Authentication/Authorization
- **Session Management**: Django sessions
- **CSRF Protection**: Django CSRF middleware
- **Rate Limiting**: API endpoint'ler için
- **Input Validation**: Tüm user input'ları validate et

## Güvenlik Kontrolleri
```python
# ✅ Güvenlik örneği
import os
from django.conf import settings

# Environment variables kullanımı
SECRET_KEY = os.environ.get('SECRET_KEY')
DATABASE_URL = os.environ.get('DATABASE_URL')

# Input validation
def validate_user_input(data):
    if not data or len(data) > 1000:
        raise ValueError("Geçersiz input")
    return data

# SQL injection prevention
def get_user_safely(user_id):
    return User.objects.filter(id=user_id).first()
```

## Frontend Güvenlik
- **HTTPS**: Secure connections
- **CSP**: Content Security Policy
- **Authentication**: Token-based auth
- **Input Sanitization**: XSS prevention 