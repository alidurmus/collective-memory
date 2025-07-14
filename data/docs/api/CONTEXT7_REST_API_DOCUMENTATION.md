# 🔗 Context7 ERP System - REST API Documentation

**Version**: v1.0.0  
**Base URL**: `http://127.0.0.1:8000/api/v1/` (Development) | `http://31.97.44.248:8000/api/v1/` (Production)  
**Authentication**: JWT Bearer Token  
**QMS Reference**: REC-API-250111-013  
**Date**: 11 Ocak 2025  

---

## 📋 **API Overview**

Context7 ERP System provides a comprehensive RESTful API covering all 8 core ERP modules with modern authentication, robust error handling, and extensive functionality.

### **🎯 Key Features**
- **JWT Authentication** with refresh token support
- **8 ERP Modules**: Complete business process coverage
- **Quality Control**: JSON-based flexible quality management
- **Real-time Analytics**: Dashboard statistics and metrics
- **Health Monitoring**: System status and performance endpoints
- **Modern Standards**: DRF + OpenAPI 3.0 compliant

### **📊 API Coverage**
| Module | Endpoints | Status | Features |
|--------|-----------|--------|----------|
| **Authentication** | 4 endpoints | ✅ Active | JWT, refresh, verify, user profile |
| **Products** | 5 endpoints | ✅ Active | CRUD, categories, filtering |
| **Customers** | 5 endpoints | ✅ Active | CRM, orders history, analytics |
| **Suppliers** | 5 endpoints | ✅ Active | Vendor management, procurement |
| **Sales Orders** | 6 endpoints | ✅ Active | Order lifecycle, status tracking |
| **Purchase Orders** | 6 endpoints | ✅ Active | Procurement, approvals, receiving |
| **Quality Control** | 16 endpoints | ✅ Active | JSON-based criteria, inspections |
| **Dashboard** | 8 endpoints | ✅ Active | Analytics, KPIs, real-time stats |
| **Health Check** | 3 endpoints | ✅ Active | System monitoring, metrics |
| **Todo Management** | 6 endpoints | ✅ Active | Task automation, categories |

---

## 🔐 **Authentication**

### **Authentication Flow**
```
1. POST /auth/login/     → Get access + refresh tokens
2. Use Bearer token      → Access protected endpoints  
3. POST /auth/refresh/   → Refresh expired tokens
4. POST /auth/verify/    → Verify token validity
```

### **Authentication Endpoints**

#### **🔑 POST /auth/login/**
Obtain JWT access and refresh tokens.

```http
POST /api/v1/auth/login/
Content-Type: application/json

{
    "username": "admin",
    "password": "your_password"
}
```

**Response:**
```json
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "user": {
        "id": 1,
        "username": "admin",
        "email": "admin@example.com",
        "first_name": "Admin",
        "last_name": "User"
    }
}
```

#### **🔄 POST /auth/refresh/**
Refresh expired access token.

```http
POST /api/v1/auth/refresh/
Content-Type: application/json

{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

#### **✅ POST /auth/verify/**
Verify token validity.

```http
POST /api/v1/auth/verify/
Content-Type: application/json

{
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

#### **👤 GET /auth/user/**
Get current authenticated user details.

```http
GET /api/v1/auth/user/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

---

## 🏭 **Core ERP Resources**

### **📦 Products API**

#### **GET /products/**
List all products with filtering and search.

```http
GET /api/v1/products/?category=furniture&search=chair&ordering=-created_at
Authorization: Bearer {token}
```

**Query Parameters:**
- `category` (string): Filter by product category
- `search` (string): Search in name, code, description
- `ordering` (string): Sort by field (`name`, `-created_at`, `price`)
- `page` (int): Page number for pagination
- `page_size` (int): Items per page (default: 20)

**Response:**
```json
{
    "count": 150,
    "next": "http://api.example.com/products/?page=2",
    "previous": null,
    "results": [
        {
            "id": "uuid-string",
            "name": "Office Chair Deluxe",
            "code": "CHAIR-001",
            "category": {
                "id": "uuid-string",
                "name": "Office Furniture",
                "code": "OFF-FURN"
            },
            "unit_price": "299.99",
            "unit_of_measure": "piece",
            "description": "Ergonomic office chair with lumbar support",
            "current_stock": "50.00",
            "minimum_stock": "10.00",
            "maximum_stock": "200.00",
            "is_active": true,
            "created_at": "2025-01-11T10:30:00Z",
            "updated_at": "2025-01-11T10:30:00Z"
        }
    ]
}
```

#### **POST /products/**
Create a new product.

```http
POST /api/v1/products/
Authorization: Bearer {token}
Content-Type: application/json

{
    "name": "Executive Desk",
    "code": "DESK-002",
    "category": "uuid-of-category",
    "unit_price": "899.99",
    "unit_of_measure": "piece",
    "description": "Large executive desk with drawers",
    "minimum_stock": "5.00",
    "maximum_stock": "50.00"
}
```

#### **GET /products/{id}/**
Retrieve specific product details.

#### **PUT/PATCH /products/{id}/**
Update product (full/partial).

#### **DELETE /products/{id}/**
Delete product (soft delete).

### **👥 Customers API**

#### **GET /customers/**
List customers with CRM data.

```http
GET /api/v1/customers/?customer_type=corporate&city=Istanbul
Authorization: Bearer {token}
```

**Response:**
```json
{
    "count": 85,
    "results": [
        {
            "id": "uuid-string",
            "name": "ABC Mobilya Ltd.",
            "code": "CUST-001",
            "tax_number": "1234567890",
            "contact_person": "Ahmet Yılmaz",
            "email": "ahmet@abcmobilya.com",
            "phone": "+90 212 555 0123",
            "address": "Atatürk Mah. Mobilya Sk. No:15",
            "city": "Istanbul",
            "customer_type": "corporate",
            "credit_limit": "50000.00",
            "payment_terms_days": 30,
            "total_orders": 15,
            "total_amount": "125000.00",
            "last_order_date": "2025-01-10",
            "is_active": true
        }
    ]
}
```

### **🏢 Suppliers API**

#### **GET /suppliers/**
List suppliers with procurement data.

```http
GET /api/v1/suppliers/?payment_terms_days__lte=30
Authorization: Bearer {token}
```

### **🛒 Sales Orders API**

#### **GET /sales-orders/**
List sales orders with status tracking.

```http
GET /api/v1/sales-orders/?status=confirmed&customer=uuid
Authorization: Bearer {token}
```

**Response:**
```json
{
    "count": 25,
    "results": [
        {
            "id": "uuid-string",
            "order_number": "SO-2025-001",
            "customer": {
                "id": "uuid-string",
                "name": "ABC Mobilya Ltd.",
                "code": "CUST-001"
            },
            "order_date": "2025-01-10",
            "delivery_date": "2025-01-20",
            "status": "confirmed",
            "total_amount": "8500.00",
            "discount_amount": "500.00",
            "notes": "Rush order for hotel project",
            "items": [
                {
                    "id": "uuid-string",
                    "product": {
                        "id": "uuid-string",
                        "name": "Office Chair Deluxe",
                        "code": "CHAIR-001"
                    },
                    "quantity": "10.00",
                    "unit_price": "299.99",
                    "total_price": "2999.90",
                    "discount_percentage": "5.00"
                }
            ],
            "created_at": "2025-01-10T09:15:00Z"
        }
    ]
}
```

#### **POST /sales-orders/**
Create new sales order.

```http
POST /api/v1/sales-orders/
Authorization: Bearer {token}
Content-Type: application/json

{
    "customer": "customer-uuid",
    "order_date": "2025-01-11",
    "delivery_date": "2025-01-21",
    "notes": "Special delivery instructions",
    "items": [
        {
            "product": "product-uuid",
            "quantity": "5.00",
            "unit_price": "299.99",
            "discount_percentage": "10.00"
        }
    ]
}
```

### **📋 Purchase Orders API**

#### **GET /purchase-orders/**
List purchase orders with supplier tracking.

```http
GET /api/v1/purchase-orders/?status=sent&supplier=uuid
Authorization: Bearer {token}
```

---

## ✅ **Quality Control API**

Context7 ERP features a sophisticated JSON-based quality control system with flexible criteria management.

### **🎯 Quality Criteria Templates**

#### **GET /quality-criteria-templates/**
List quality criteria templates.

```http
GET /api/v1/quality-criteria-templates/?template_type=product
Authorization: Bearer {token}
```

**Response:**
```json
{
    "count": 12,
    "results": [
        {
            "id": "uuid-string",
            "name": "Office Furniture Quality Standard",
            "template_type": "product",
            "version": "1.2",
            "criteria_data": {
                "criteria": [
                    {
                        "id": "dimension_check",
                        "name": "Dimension Check",
                        "type": "measurement",
                        "unit": "cm",
                        "min_value": 75,
                        "max_value": 80,
                        "target_value": 77.5,
                        "tolerance": 2.5,
                        "is_critical": true
                    },
                    {
                        "id": "surface_finish",
                        "name": "Surface Finish Quality",
                        "type": "visual",
                        "options": ["excellent", "good", "acceptable", "poor"],
                        "acceptable_values": ["excellent", "good"],
                        "is_critical": false
                    }
                ]
            },
            "description": "Standard quality criteria for office furniture products",
            "is_active": true,
            "created_at": "2025-01-05T14:20:00Z"
        }
    ]
}
```

#### **POST /quality-criteria-templates/**
Create new quality criteria template.

```http
POST /api/v1/quality-criteria-templates/
Authorization: Bearer {token}
Content-Type: application/json

{
    "name": "Material Inspection Standard",
    "template_type": "material",
    "version": "1.0",
    "criteria_data": {
        "criteria": [
            {
                "id": "hardness_test",
                "name": "Material Hardness",
                "type": "measurement",
                "unit": "HRC",
                "min_value": 45,
                "max_value": 55,
                "target_value": 50,
                "tolerance": 3,
                "is_critical": true
            }
        ]
    },
    "description": "Quality criteria for raw materials"
}
```

### **🔬 Quality Inspection Results**

#### **GET /quality-inspection-results/**
List inspection results with filtering.

```http
GET /api/v1/quality-inspection-results/?form_type=incoming&overall_status=passed
Authorization: Bearer {token}
```

**Response:**
```json
{
    "count": 45,
    "results": [
        {
            "id": "uuid-string",
            "form_type": "incoming",
            "inspection_date": "2025-01-11",
            "inspector": {
                "id": 5,
                "username": "inspector1",
                "first_name": "Quality",
                "last_name": "Inspector"
            },
            "content_type": "product",
            "product": {
                "id": "uuid-string",
                "name": "Office Chair Deluxe",
                "code": "CHAIR-001"
            },
            "batch_number": "BATCH-2025-001",
            "quantity": "100.00",
            "measurement_results": {
                "dimension_check": {
                    "measured_value": 77.2,
                    "status": "passed",
                    "notes": "Within tolerance"
                },
                "surface_finish": {
                    "selected_value": "excellent",
                    "status": "passed",
                    "notes": "Perfect surface quality"
                }
            },
            "overall_status": "passed",
            "comments": "All criteria met successfully",
            "created_at": "2025-01-11T11:30:00Z"
        }
    ]
}
```

#### **POST /quality-inspection-results/**
Create new inspection result.

```http
POST /api/v1/quality-inspection-results/
Authorization: Bearer {token}
Content-Type: application/json

{
    "form_type": "final",
    "inspection_date": "2025-01-11",
    "content_type": "product",
    "product": "product-uuid",
    "batch_number": "BATCH-2025-002",
    "quantity": "50.00",
    "measurement_results": {
        "dimension_check": {
            "measured_value": 76.8,
            "status": "passed"
        },
        "surface_finish": {
            "selected_value": "good",
            "status": "passed"
        }
    },
    "overall_status": "passed",
    "comments": "Final inspection completed successfully"
}
```

---

## 📊 **Dashboard & Analytics API**

### **📈 GET /dashboard-stats/**
Get comprehensive dashboard statistics.

```http
GET /api/v1/dashboard-stats/
Authorization: Bearer {token}
```

**Response:**
```json
{
    "overview": {
        "total_products": 150,
        "total_customers": 85,
        "total_suppliers": 42,
        "active_orders": 25
    },
    "sales": {
        "total_sales": "2500000.00",
        "monthly_sales": "185000.00",
        "sales_growth": "12.5",
        "top_customers": [
            {
                "name": "ABC Mobilya Ltd.",
                "total_amount": "125000.00"
            }
        ]
    },
    "production": {
        "active_orders": 15,
        "completed_today": 8,
        "efficiency_rate": "92.3"
    },
    "inventory": {
        "total_stock_value": "850000.00",
        "low_stock_items": 12,
        "out_of_stock_items": 3
    },
    "quality": {
        "inspections_today": 25,
        "pass_rate": "96.8",
        "critical_issues": 1
    }
}
```

### **🏭 GET /quality-control-dashboard/**
Quality-specific dashboard metrics.

```http
GET /api/v1/quality-control-dashboard/
Authorization: Bearer {token}
```

---

## 🏥 **Health Check & Monitoring API**

### **🔍 GET /core/health/**
Basic health check endpoint.

```http
GET /api/v1/core/health/
```

**Response:**
```json
{
    "status": "healthy",
    "timestamp": "2025-01-11T12:30:45.123456Z",
    "version": "v2.2.0-glassmorphism-enhanced",
    "checks": {
        "database": "healthy",
        "cache": "healthy",
        "memory_usage": "normal"
    }
}
```

### **📊 GET /core/health/detailed/**
Comprehensive system metrics.

```http
GET /api/v1/core/health/detailed/
Authorization: Bearer {token}
```

**Response:**
```json
{
    "status": "healthy",
    "system": {
        "memory": {
            "usage_percent": 67.3,
            "available_mb": 2048,
            "status": "normal"
        },
        "cpu": {
            "usage_percent": 23.5,
            "load_average": [0.75, 0.82, 0.91]
        },
        "disk": {
            "usage_percent": 45.2,
            "free_space_gb": 128.5
        }
    },
    "database": {
        "status": "connected",
        "query_time_ms": 4.2,
        "connection_count": 12
    },
    "cache": {
        "status": "active",
        "hit_ratio": 89.6,
        "memory_usage_mb": 156.3
    },
    "api": {
        "requests_per_minute": 45,
        "average_response_time_ms": 125,
        "error_rate": 0.1
    }
}
```

---

## 📋 **Todo Management API**

### **✅ GET /core/api/v1/todos/**
List todos with filtering and categories.

```http
GET /api/v1/core/api/v1/todos/?status=pending&priority=high
Authorization: Bearer {token}
```

### **📊 GET /core/api/v1/todo-stats/**
Todo analytics and statistics.

```http
GET /api/v1/core/api/v1/todo-stats/
Authorization: Bearer {token}
```

---

## 🔧 **Request/Response Standards**

### **📤 Standard Response Format**
All API responses follow consistent structure:

```json
{
    "success": true,
    "data": { /* Response data */ },
    "message": "Operation completed successfully",
    "timestamp": "2025-01-11T12:30:45Z",
    "request_id": "req_abc123",
    "pagination": {
        "count": 100,
        "next": "url",
        "previous": "url"
    }
}
```

### **❌ Error Response Format**
```json
{
    "success": false,
    "error": {
        "code": "VALIDATION_ERROR",
        "message": "Invalid input data",
        "details": {
            "field_name": ["This field is required."]
        }
    },
    "timestamp": "2025-01-11T12:30:45Z",
    "request_id": "req_abc123"
}
```

### **📋 HTTP Status Codes**
- **200 OK**: Successful GET, PUT, PATCH
- **201 Created**: Successful POST
- **204 No Content**: Successful DELETE
- **400 Bad Request**: Validation errors
- **401 Unauthorized**: Authentication required
- **403 Forbidden**: Permission denied
- **404 Not Found**: Resource not found
- **429 Too Many Requests**: Rate limit exceeded
- **500 Internal Server Error**: Server error

---

## 🔒 **Security & Rate Limiting**

### **🛡️ Security Headers**
All API responses include security headers:
- `X-Content-Type-Options: nosniff`
- `X-Frame-Options: DENY`
- `X-XSS-Protection: 1; mode=block`
- `Strict-Transport-Security: max-age=31536000`

### **⏱️ Rate Limiting**
- **Authenticated Users**: 1000 requests/hour
- **Dashboard API**: 200 requests/hour
- **Anonymous Users**: 100 requests/hour
- **Health Check**: No limits

### **🔐 Authentication Header**
Include JWT token in all authenticated requests:
```http
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

---

## 📖 **API Usage Examples**

### **🔄 Complete Workflow Example**
```bash
# 1. Authenticate
curl -X POST http://localhost:8000/api/v1/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "password"}'

# 2. Get products
curl -X GET http://localhost:8000/api/v1/products/ \
  -H "Authorization: Bearer YOUR_TOKEN"

# 3. Create sales order
curl -X POST http://localhost:8000/api/v1/sales-orders/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"customer": "uuid", "items": [...]}'

# 4. Quality inspection
curl -X POST http://localhost:8000/api/v1/quality-inspection-results/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"form_type": "final", "product": "uuid", ...}'
```

### **🐍 Python Client Example**
```python
import requests

class Context7ERPClient:
    def __init__(self, base_url, username, password):
        self.base_url = base_url
        self.session = requests.Session()
        self.authenticate(username, password)
    
    def authenticate(self, username, password):
        response = self.session.post(
            f"{self.base_url}/auth/login/",
            json={"username": username, "password": password}
        )
        token = response.json()["access"]
        self.session.headers.update({
            "Authorization": f"Bearer {token}"
        })
    
    def get_products(self, **filters):
        return self.session.get(
            f"{self.base_url}/products/",
            params=filters
        ).json()
    
    def create_sales_order(self, order_data):
        return self.session.post(
            f"{self.base_url}/sales-orders/",
            json=order_data
        ).json()

# Usage
client = Context7ERPClient(
    "http://localhost:8000/api/v1",
    "admin", 
    "password"
)

products = client.get_products(category="furniture")
order = client.create_sales_order({
    "customer": "uuid",
    "items": [{"product": "uuid", "quantity": "5.00"}]
})
```

---

## 📚 **Advanced Features**

### **🔍 Advanced Filtering**
```http
# Complex filtering with Q objects
GET /api/v1/products/?search=chair&category=furniture&price__gte=100&price__lte=500

# Date range filtering
GET /api/v1/sales-orders/?order_date__gte=2025-01-01&order_date__lte=2025-01-31

# Related field filtering
GET /api/v1/sales-orders/?customer__city=Istanbul&items__product__category=furniture
```

### **📊 Aggregation & Analytics**
```http
# Dashboard with aggregated data
GET /api/v1/dashboard-stats/?period=monthly&group_by=category

# Quality control analytics
GET /api/v1/quality-criteria-stats/?form_type=final&date_range=last_30_days
```

### **📦 Bulk Operations**
```http
# Bulk create products
POST /api/v1/products/bulk-create/
[
    {"name": "Product 1", "code": "PROD-001"},
    {"name": "Product 2", "code": "PROD-002"}
]

# Bulk update quality inspections
PATCH /api/v1/quality-inspection-results/bulk-update/
{
    "ids": ["uuid1", "uuid2"],
    "data": {"overall_status": "approved"}
}
```

---

## 🚀 **Performance & Optimization**

### **⚡ Performance Features**
- **Database Optimization**: Optimized queries with select_related/prefetch_related
- **Caching**: Redis-based caching for frequently accessed data
- **Pagination**: Efficient pagination with cursor-based pagination for large datasets
- **Compression**: GZIP response compression enabled
- **Connection Pooling**: Database connection pooling for high concurrency

### **📊 Performance Metrics**
- **Average Response Time**: <200ms for most endpoints
- **Database Query Time**: <50ms average
- **Cache Hit Ratio**: >80% for frequently accessed data
- **Concurrent Users**: Supports 100+ concurrent API users

---

## 🐛 **Troubleshooting**

### **Common Issues**

#### **🔐 Authentication Issues**
```json
// 401 Unauthorized
{
    "detail": "Given token not valid for any token type",
    "code": "token_not_valid",
    "messages": [
        {
            "token_class": "AccessToken",
            "token_type": "access",
            "message": "Token is invalid or expired"
        }
    ]
}
```
**Solution**: Refresh token using `/auth/refresh/` endpoint.

#### **📝 Validation Errors**
```json
// 400 Bad Request
{
    "name": ["This field is required."],
    "unit_price": ["A valid number is required."],
    "category": ["Invalid pk \"invalid-uuid\" - object does not exist."]
}
```
**Solution**: Check required fields and data types.

#### **⏱️ Rate Limiting**
```json
// 429 Too Many Requests
{
    "detail": "Request was throttled. Expected available in 3600 seconds."
}
```
**Solution**: Wait for rate limit reset or contact admin for higher limits.

---

## 📞 **Support & Contact**

### **🔗 Additional Resources**
- **Swagger UI**: `http://localhost:8000/api/docs/` (Interactive API documentation)
- **OpenAPI Schema**: `http://localhost:8000/api/schema/`
- **Postman Collection**: Available on request

### **📧 API Support**
- **Technical Issues**: Create GitHub issue with API error details
- **Feature Requests**: Submit via GitHub Issues with `enhancement` label
- **Security Issues**: Report via private communication channels

### **📋 Changelog**
- **v1.0.0** (January 2025): Initial API release with 8 ERP modules
- **v1.1.0** (Planned): Enhanced quality control features
- **v1.2.0** (Planned): Advanced analytics and reporting APIs

---

**🎯 Success**: Context7 ERP API provides comprehensive access to all business processes with modern REST standards, robust authentication, and excellent performance for enterprise applications.

**📊 Coverage**: 50+ endpoints across 8 ERP modules with 100% feature parity to web interface.

**🔐 Security**: Enterprise-grade security with JWT authentication, rate limiting, and comprehensive input validation.

---

*Context7 ERP System - Enterprise API Excellence* 