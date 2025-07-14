# Context7 ERP - Sentry Integration Guide

**Version:** v2.2.0-glassmorphism-enhanced + Sentry Integration  
**Date:** 13 July 2025  
**QMS Reference:** REC-SENTRY-INTEGRATION-250713-001

## 📋 Overview

Sentry integration provides comprehensive error tracking, performance monitoring, and user context for Context7 ERP system.

## 🚀 Features

### Error Tracking
- **Automatic Error Capture**: All unhandled exceptions
- **Custom Error Context**: ERP module, user, operation details
- **Error Filtering**: Skip common Django exceptions
- **Performance Issues**: Slow operation detection

### Performance Monitoring
- **Transaction Tracking**: API endpoints, database operations
- **Performance Profiling**: 10% sample rate
- **Slow Query Detection**: Database performance monitoring
- **Custom Performance Metrics**: Business operation timing

### User Context
- **User Information**: ID, username, email, permissions
- **Request Context**: Method, path, parameters
- **ERP Module Context**: Module-specific information
- **Business Operation Context**: Operation-specific data

## 🔧 Configuration

### Environment Variables
```bash
# Sentry Configuration
SENTRY_DSN=https://your-sentry-dsn@sentry.io/project-id
SENTRY_ENVIRONMENT=production
SENTRY_RELEASE=context7-erp@v2.2.0-glassmorphism-enhanced
```

### Django Settings
```python
# Enable Sentry
DJANGO_SETTINGS_MODULE=dashboard_project.sentry_settings

# Sentry will be automatically configured if DSN is provided
```

## 📊 Usage Examples

### Basic Error Capture
```python
from core.sentry.utils import capture_erp_error

try:
    # Your code here
    pass
except Exception as e:
    capture_erp_error(
        error=e,
        module='sales',
        user=request.user,
        extra_data={'order_id': order.id}
    )
```

### Business Logic Error
```python
from core.sentry.utils import capture_business_logic_error

if insufficient_stock:
    capture_business_logic_error(
        error_message='Insufficient stock for order',
        operation='create_sales_order',
        data={'product_id': product.id, 'requested': quantity, 'available': stock},
        user=request.user
    )
```

### Performance Monitoring
```python
from core.sentry.utils import capture_performance_issue
import time

start_time = time.time()
# Your slow operation
duration = time.time() - start_time

if duration > 5.0:
    capture_performance_issue(
        operation='generate_report',
        duration=duration,
        extra_data={'report_type': 'sales_summary'}
    )
```

### Using Decorators
```python
from core.sentry.decorators import sentry_monitor, sentry_api_monitor

@sentry_monitor(module='sales', operation='create_order')
def create_sales_order(customer_id, items):
    # Your function code
    pass

@sentry_api_monitor(endpoint='sales_api')
def sales_api_view(request):
    # Your API view code
    pass
```

## 🏷️ Available Decorators

### Function Monitoring
- `@sentry_monitor(module, operation)`: General function monitoring
- `@sentry_database_monitor(model_name, operation)`: Database operations
- `@sentry_business_logic_monitor(business_process)`: Business logic
- `@sentry_transaction(name, operation)`: Performance transactions

### API Monitoring
- `@sentry_api_monitor(endpoint)`: API endpoint monitoring
- `@sentry_security_monitor(event_type, severity)`: Security operations

### ERP-Specific Decorators
- `@monitor_sales_operation(operation)`: Sales module operations
- `@monitor_inventory_operation(operation)`: Inventory operations
- `@monitor_production_operation(operation)`: Production operations
- `@monitor_quality_operation(operation)`: Quality control operations

## 🧪 Testing

### Test Sentry Integration
```bash
# Send test error
python manage.py sentry_test --error

# Send test message
python manage.py sentry_test --message

# Send performance issue
python manage.py sentry_test --performance

# Send all test events
python manage.py sentry_test --all
```

### Manual Testing
```python
import sentry_sdk

# Test basic error
sentry_sdk.capture_exception(Exception("Test error"))

# Test message
sentry_sdk.capture_message("Test message", level='info')

# Test transaction
with sentry_sdk.start_transaction(name="test", op="test"):
    # Your code here
    pass
```

## 📈 Monitoring Dashboard

### Sentry Dashboard Features
- **Error Tracking**: Real-time error monitoring
- **Performance**: Transaction and query performance
- **Releases**: Track deployments and releases
- **Alerts**: Email/Slack notifications for issues

### Key Metrics to Monitor
- **Error Rate**: Errors per minute/hour
- **Performance**: 95th percentile response times
- **User Impact**: Users affected by errors
- **Release Health**: Error rates by release version

## 🔍 Troubleshooting

### Common Issues

#### Sentry Not Working
```bash
# Check if Sentry is enabled
python manage.py shell
>>> from django.conf import settings
>>> print(settings.ENABLE_SENTRY)
>>> print(settings.SENTRY_DSN)
```

#### Too Many Events
- Adjust sample rates in settings
- Use before_send filters
- Check error filtering rules

#### Missing Context
- Ensure decorators are applied
- Check middleware configuration
- Verify user authentication

### Debug Mode
```python
# Enable Sentry debug mode
SENTRY_DEBUG = True
```

## 📝 Best Practices

### Error Handling
1. **Use Specific Exceptions**: Create custom exception classes
2. **Add Context**: Include relevant business data
3. **Filter Noise**: Skip expected errors (404, etc.)
4. **User Privacy**: Don't send PII data

### Performance Monitoring
1. **Sample Appropriately**: Use 10-20% sample rate
2. **Monitor Critical Paths**: Focus on business-critical operations
3. **Set Thresholds**: Define performance thresholds
4. **Regular Review**: Review performance data weekly

### Security
1. **No PII**: Never send personally identifiable information
2. **Sanitize Data**: Clean sensitive data before sending
3. **Access Control**: Limit Sentry dashboard access
4. **Data Retention**: Configure appropriate retention policies

## 🔗 Integration Points

### Django Integration
- **Middleware**: Automatic request/response monitoring
- **Logging**: Integration with Django logging
- **Database**: Query performance monitoring
- **Cache**: Redis operation monitoring

### Celery Integration
- **Task Monitoring**: Async task error tracking
- **Performance**: Task execution time monitoring
- **Beat Tasks**: Periodic task monitoring
- **Worker Health**: Worker process monitoring

### Custom Integration
- **Business Logic**: ERP operation monitoring
- **API Endpoints**: REST API monitoring
- **Security Events**: Authentication/authorization monitoring
- **Data Validation**: Input validation error tracking

---

## 📞 Support

For Sentry-related issues:
1. Check Sentry dashboard for error details
2. Review Django logs for integration issues
3. Use management commands for testing
4. Consult Sentry documentation for advanced features

**QMS Reference:** REC-SENTRY-INTEGRATION-250713-001  
**Last Updated:** 13 July 2025
