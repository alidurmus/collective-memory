# 📚 **Context7 Django ERP - API Dokümantasyon Standartları v1.0**

**Amaç:** Context7 Django ERP System'in REST API'lerinin tutarlı, kapsamlı ve kullanıcı dostu şekilde belgelenmesi için geliştirilmiş standarttır. Django REST Framework, Swagger/OpenAPI ve API best practices'leri temel alır.

**Protokol Referansı:** [`CONTEXT7_CENTRAL_PROTOCOL.md`](CONTEXT7_CENTRAL_PROTOCOL.md) - Bölüm 6.2

---

## **🏗️ Context7 ERP API Mimarisi**

### **📊 API Dokümantasyon Hiyerarşisi**

```
docs/api/
├── API_DOCUMENTATION_STANDARDS.md     # 📋 Bu dosya - API dok standartları
├── openapi/                           # 🔧 OpenAPI/Swagger dosyaları
│   ├── context7-erp-openapi.yaml      # 🗂️ Ana OpenAPI specification
│   ├── components/                    # 🧩 Reusable API components
│   │   ├── schemas/                   # 📋 Data model schemas
│   │   ├── responses/                 # 📤 Standard response formats
│   │   ├── parameters/                # 📥 Common parameters
│   │   └── security/                  # 🔐 Security schemes
│   └── modules/                       # 📂 ERP module specific APIs
│       ├── production-api.yaml        # 🏭 Production API specs
│       ├── inventory-api.yaml         # 📦 Inventory API specs
│       ├── sales-api.yaml             # 💰 Sales API specs
│       ├── purchasing-api.yaml        # 🛒 Purchasing API specs
│       ├── quality-api.yaml           # ✅ Quality API specs
│       ├── finance-api.yaml           # 💹 Finance API specs
│       ├── hr-api.yaml                # 👥 HR API specs
│       └── reports-api.yaml           # 📈 Reports API specs
├── guides/                            # 📖 API kullanım rehberleri
│   ├── authentication-guide.md       # 🔑 Authentication rehberi
│   ├── pagination-guide.md           # 📄 Pagination kullanımı
│   ├── filtering-guide.md             # 🔍 Filtering ve search
│   ├── error-handling-guide.md       # 🚨 Error handling
│   ├── rate-limiting-guide.md        # ⏱️ Rate limiting
│   └── integration-examples.md       # 🔗 Integration örnekleri
├── examples/                          # 📝 Code examples
│   ├── python/                       # 🐍 Python client examples
│   ├── javascript/                   # 📜 JavaScript examples
│   ├── postman/                      # 📮 Postman collections
│   └── curl/                         # 🌐 cURL examples
└── changelog/                         # 📅 API version history
    ├── v1.0.0.md                     # API v1.0.0 changelog
    └── migration-guides/             # 🔄 Version migration guides
```

---

## **📋 API Dokümantasyon Formatı ve Standartları**

### **🎯 OpenAPI Specification Standardı**

```yaml
# docs/api/openapi/context7-erp-openapi.yaml
openapi: 3.0.3
info:
  title: Context7 Django ERP API
  description: |
    Comprehensive REST API for Context7 Enterprise Resource Planning System.
    
    ## Features
    - 🔐 JWT Authentication
    - 📊 8 ERP Modules (Production, Inventory, Sales, etc.)
    - 📱 Modern RESTful design
    - 🎨 Context7 Glassmorphism integration
    - ⚡ High performance optimized endpoints
    
    ## Base URL
    - **Development:** `http://localhost:8000/api/v1/`
    - **Production:** `https://your-domain.com/api/v1/`
    
    ## Authentication
    All API endpoints require JWT authentication. Obtain token via `/auth/token/` endpoint.
    
  version: "1.0.0"
  contact:
    name: Context7 ERP API Support
    email: api-support@context7.com
    url: https://docs.context7.com
  license:
    name: Context7 License
    url: https://context7.com/license
  
servers:
  - url: http://localhost:8000/api/v1
    description: Development server
  - url: https://api.context7.com/v1
    description: Production server

# Global security scheme
security:
  - JWTAuth: []

# Reusable components
components:
  securitySchemes:
    JWTAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
      description: |
        JWT token authentication. Obtain token via `/auth/token/` endpoint.
        
        Example: `Authorization: Bearer <your_jwt_token>`
  
  schemas:
    Error:
      type: object
      required:
        - error_code
        - message
      properties:
        error_code:
          type: string
          description: Error reference code (ERR-TYPE-YYMMDD-SEQUENCE)
          example: "ERR-API-250609-001"
        message:
          type: string
          description: Human-readable error message
          example: "Invalid authentication credentials"
        details:
          type: object
          description: Additional error details
        timestamp:
          type: string
          format: date-time
          description: Error occurrence timestamp
    
    PaginatedResponse:
      type: object
      required:
        - count
        - results
      properties:
        count:
          type: integer
          description: Total number of items
          example: 150
        next:
          type: string
          nullable: true
          description: URL for next page
          example: "http://localhost:8000/api/v1/endpoint/?page=3"
        previous:
          type: string
          nullable: true
          description: URL for previous page
          example: "http://localhost:8000/api/v1/endpoint/?page=1"
        results:
          type: array
          description: Array of result objects
          items:
            type: object
  
  responses:
    BadRequest:
      description: Bad Request - Invalid input data
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
          example:
            error_code: "ERR-VALID-250609-001"
            message: "Validation failed"
            details:
              field_errors:
                quantity: ["This field must be a positive number"]
    
    Unauthorized:
      description: Unauthorized - Authentication required
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
          example:
            error_code: "ERR-AUTH-250609-001"
            message: "Authentication credentials were not provided"
    
    Forbidden:
      description: Forbidden - Insufficient permissions
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
          example:
            error_code: "ERR-PERM-250609-001"
            message: "You do not have permission to perform this action"
    
    NotFound:
      description: Not Found - Resource does not exist
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
          example:
            error_code: "ERR-API-250609-002"
            message: "Production order not found"
    
    InternalServerError:
      description: Internal Server Error
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
          example:
            error_code: "ERR-SYS-250609-001"
            message: "An unexpected error occurred"

# API paths will be organized by modules
paths:
  /auth/:
    $ref: './components/auth-endpoints.yaml'
  /production/:
    $ref: './modules/production-api.yaml'
  /inventory/:
    $ref: './modules/inventory-api.yaml'
  # ... other module paths
```

### **📊 ERP Module API Documentation Standardı**

```yaml
# docs/api/openapi/modules/production-api.yaml
# Production Management API Specification

/production/orders/:
  get:
    tags:
      - Production Management
    summary: List production orders
    description: |
      Retrieve a paginated list of production orders with optional filtering and sorting.
      
      ## Filtering Options
      - `status`: Filter by production status
      - `product_id`: Filter by product
      - `date_range`: Filter by date range
      
      ## Sorting Options
      - `created_at`: Sort by creation date
      - `priority`: Sort by priority level
      - `due_date`: Sort by due date
      
    parameters:
      - name: page
        in: query
        description: Page number for pagination
        required: false
        schema:
          type: integer
          minimum: 1
          default: 1
      - name: page_size
        in: query
        description: Number of items per page
        required: false
        schema:
          type: integer
          minimum: 1
          maximum: 100
          default: 20
      - name: status
        in: query
        description: Filter by production status
        required: false
        schema:
          type: string
          enum: [draft, planned, in_production, quality_check, completed, cancelled]
      - name: search
        in: query
        description: Search in order number, product name, or description
        required: false
        schema:
          type: string
          minLength: 2
      - name: ordering
        in: query
        description: Sort order (prefix with - for descending)
        required: false
        schema:
          type: string
          enum: [created_at, -created_at, priority, -priority, due_date, -due_date]
    
    responses:
      '200':
        description: Successful response with production orders
        content:
          application/json:
            schema:
              allOf:
                - $ref: '../components/schemas.yaml#/PaginatedResponse'
                - type: object
                  properties:
                    results:
                      type: array
                      items:
                        $ref: '#/components/schemas/ProductionOrder'
            example:
              count: 42
              next: "http://localhost:8000/api/v1/production/orders/?page=3"
              previous: "http://localhost:8000/api/v1/production/orders/?page=1"
              results:
                - id: 1
                  order_number: "PRD-2025-001"
                  product:
                    id: 15
                    name: "Premium Widget A"
                    sku: "PWA-001"
                  quantity: 100
                  status: "in_production"
                  priority: "high"
                  created_at: "2025-06-09T10:30:00Z"
                  due_date: "2025-06-15T00:00:00Z"
      '400':
        $ref: '../components/responses.yaml#/BadRequest'
      '401':
        $ref: '../components/responses.yaml#/Unauthorized'
      '500':
        $ref: '../components/responses.yaml#/InternalServerError'
  
  post:
    tags:
      - Production Management
    summary: Create new production order
    description: |
      Create a new production order with specified parameters.
      
      ## Business Rules
      - Product must exist and be active
      - Quantity must be positive
      - Due date must be in the future
      - Materials must be available (optional check)
      
    requestBody:
      required: true
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/ProductionOrderCreate'
          example:
            product_id: 15
            quantity: 100
            priority: "high"
            due_date: "2025-06-15"
            notes: "Rush order for premium client"
            check_materials: true
    
    responses:
      '201':
        description: Production order created successfully
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/ProductionOrder'
      '400':
        $ref: '../components/responses.yaml#/BadRequest'
      '401':
        $ref: '../components/responses.yaml#/Unauthorized'
      '403':
        $ref: '../components/responses.yaml#/Forbidden'

# Component schemas for Production module
components:
  schemas:
    ProductionOrder:
      type: object
      required:
        - id
        - order_number
        - product
        - quantity
        - status
      properties:
        id:
          type: integer
          description: Unique production order ID
          example: 1
        order_number:
          type: string
          description: Human-readable order number
          example: "PRD-2025-001"
        product:
          $ref: '#/components/schemas/ProductSummary'
        quantity:
          type: integer
          minimum: 1
          description: Quantity to produce
          example: 100
        status:
          type: string
          enum: [draft, planned, in_production, quality_check, completed, cancelled]
          description: Current production status
          example: "in_production"
        priority:
          type: string
          enum: [low, medium, high, urgent]
          description: Production priority level
          example: "high"
        created_at:
          type: string
          format: date-time
          description: Order creation timestamp
          example: "2025-06-09T10:30:00Z"
        due_date:
          type: string
          format: date
          description: Production due date
          example: "2025-06-15"
        notes:
          type: string
          nullable: true
          description: Additional notes
          example: "Rush order for premium client"
        progress_percentage:
          type: number
          minimum: 0
          maximum: 100
          description: Production completion percentage
          example: 65.5
    
    ProductionOrderCreate:
      type: object
      required:
        - product_id
        - quantity
        - due_date
      properties:
        product_id:
          type: integer
          description: ID of product to produce
          example: 15
        quantity:
          type: integer
          minimum: 1
          description: Quantity to produce
          example: 100
        priority:
          type: string
          enum: [low, medium, high, urgent]
          default: "medium"
          description: Production priority level
          example: "high"
        due_date:
          type: string
          format: date
          description: Production due date
          example: "2025-06-15"
        notes:
          type: string
          nullable: true
          maxLength: 1000
          description: Additional notes
          example: "Rush order for premium client"
        check_materials:
          type: boolean
          default: false
          description: Check material availability before creating order
          example: true
```

---

## **📖 API Dokümantasyon Yazım Kuralları**

### **✍️ Dokümantasyon İçerik Standartları**

#### **📋 Endpoint Açıklama Formatı**
```markdown
## [HTTP Method] /api/v1/endpoint/path/

**Purpose:** [Single sentence describing what this endpoint does]

**Business Context:** [How this endpoint fits into ERP business processes]

### Request Parameters
| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| param_name | string | Yes | Parameter description | "example_value" |

### Request Body Schema
[Detailed schema description with validation rules]

### Response Format
[Standard response structure with examples]

### Error Handling
[Specific error codes and handling for this endpoint]

### Business Rules
- [ ] Rule 1: Description
- [ ] Rule 2: Description

### Performance Notes
- Expected response time: < XXXms
- Rate limiting: XX requests/minute
- Caching: TTL XX minutes

### Example Usage
[Complete working examples in multiple languages]
```

#### **🔍 API Example Documentation**

```markdown
### POST /api/v1/production/orders/

**Purpose:** Create a new production order for manufacturing products.

**Business Context:** This endpoint initiates the production workflow in the ERP system, connecting inventory management with production planning and quality control processes.

#### Request Parameters
None (all data in request body)

#### Request Body Schema
```json
{
  "product_id": 15,          // [Required] Product to manufacture
  "quantity": 100,           // [Required] Production quantity (min: 1)
  "priority": "high",        // [Optional] Priority level (low/medium/high/urgent)
  "due_date": "2025-06-15",  // [Required] Production deadline (ISO date)
  "notes": "Rush order",     // [Optional] Additional notes (max: 1000 chars)
  "check_materials": true    // [Optional] Validate material availability
}
```

#### Response Format
```json
{
  "id": 123,
  "order_number": "PRD-2025-001",
  "product": {
    "id": 15,
    "name": "Premium Widget A",
    "sku": "PWA-001"
  },
  "quantity": 100,
  "status": "draft",
  "priority": "high",
  "created_at": "2025-06-09T10:30:00Z",
  "due_date": "2025-06-15",
  "progress_percentage": 0.0
}
```

#### Error Handling
- **ERR-VALID-250609-001**: Validation error (400)
- **ERR-AUTH-250609-001**: Authentication required (401)
- **ERR-PERM-250609-001**: Insufficient permissions (403)
- **ERR-API-250609-002**: Product not found (404)

#### Business Rules
- [x] Product must exist and be active
- [x] Quantity must be positive integer
- [x] Due date must be in the future
- [x] User must have production.add_productionorder permission
- [ ] Material availability check (if enabled)

#### Performance Notes
- Expected response time: < 200ms
- Rate limiting: 60 requests/minute per user
- No caching (real-time data)

#### Example Usage

**cURL Example:**
```bash
curl -X POST http://localhost:8000/api/v1/production/orders/ \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "product_id": 15,
    "quantity": 100,
    "priority": "high",
    "due_date": "2025-06-15",
    "notes": "Rush order for premium client"
  }'
```

**Python Example:**
```python
import requests

headers = {
    'Authorization': 'Bearer YOUR_JWT_TOKEN',
    'Content-Type': 'application/json'
}

data = {
    'product_id': 15,
    'quantity': 100,
    'priority': 'high',
    'due_date': '2025-06-15',
    'notes': 'Rush order for premium client'
}

response = requests.post(
    'http://localhost:8000/api/v1/production/orders/',
    headers=headers,
    json=data
)

if response.status_code == 201:
    order = response.json()
    print(f"Created order: {order['order_number']}")
else:
    error = response.json()
    print(f"Error: {error['message']}")
```

**JavaScript Example:**
```javascript
const createProductionOrder = async (orderData) => {
  try {
    const response = await fetch('/api/v1/production/orders/', {
      method: 'POST',
      headers: {
        'Authorization': 'Bearer ' + localStorage.getItem('jwt_token'),
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(orderData)
    });
    
    if (response.ok) {
      const order = await response.json();
      console.log('Order created:', order.order_number);
      return order;
    } else {
      const error = await response.json();
      throw new Error(error.message);
    }
  } catch (error) {
    console.error('Failed to create order:', error.message);
    throw error;
  }
};

// Usage
createProductionOrder({
  product_id: 15,
  quantity: 100,
  priority: 'high',
  due_date: '2025-06-15',
  notes: 'Rush order for premium client'
});
```
```

---

## **🔗 API Integration Patterns**

### **🔑 Authentication Pattern Documentation**

```markdown
# Context7 ERP API Authentication Guide

## JWT Token Authentication

Context7 ERP API uses JWT (JSON Web Token) authentication for secure API access.

### Obtaining Access Token

**Endpoint:** `POST /api/v1/auth/token/`

**Request:**
```json
{
  "username": "your_username",
  "password": "your_password"
}
```

**Response:**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "expires_in": 3600,
  "token_type": "Bearer"
}
```

### Using Access Token

Include the access token in the Authorization header for all API requests:

```http
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

### Token Refresh

When the access token expires, use the refresh token to obtain a new one:

**Endpoint:** `POST /api/v1/auth/token/refresh/`

**Request:**
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

### Error Handling

| Error Code | HTTP Status | Description | Solution |
|------------|-------------|-------------|----------|
| ERR-AUTH-250609-001 | 401 | Token missing | Include Authorization header |
| ERR-AUTH-250609-002 | 401 | Token expired | Refresh token or re-authenticate |
| ERR-AUTH-250609-003 | 401 | Token invalid | Re-authenticate |
| ERR-AUTH-250609-004 | 403 | Insufficient permissions | Check user permissions |
```

### **📄 Pagination Pattern Documentation**

```markdown
# Context7 ERP API Pagination Guide

## Standard Pagination Format

All list endpoints use cursor-based pagination for consistent performance.

### Request Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| page | integer | 1 | Page number |
| page_size | integer | 20 | Items per page (max: 100) |

### Response Format

```json
{
  "count": 150,
  "next": "http://localhost:8000/api/v1/endpoint/?page=3",
  "previous": "http://localhost:8000/api/v1/endpoint/?page=1",
  "results": [
    // Array of result objects
  ]
}
```

### Navigation Examples

**Next Page:**
```javascript
if (response.next) {
  fetch(response.next)
    .then(response => response.json())
    .then(data => {
      // Handle next page data
    });
}
```

**All Pages:**
```python
def get_all_items(url):
    all_items = []
    while url:
        response = requests.get(url, headers=headers).json()
        all_items.extend(response['results'])
        url = response['next']
    return all_items
```
```

---

## **📊 API Performance Documentation Standards**

### **⚡ Performance Metrics Documentation**

```markdown
## API Performance Standards

### Response Time Targets

| Endpoint Type | Target Response Time | Maximum Response Time |
|---------------|---------------------|----------------------|
| Authentication | < 100ms | 200ms |
| Simple CRUD | < 200ms | 400ms |
| Complex Queries | < 500ms | 1000ms |
| Report Generation | < 2000ms | 5000ms |
| File Uploads | < 1000ms | 3000ms |

### Rate Limiting

| User Type | Requests/Minute | Burst Limit |
|-----------|----------------|-------------|
| Anonymous | 10 | 20 |
| Authenticated | 60 | 120 |
| Premium | 300 | 600 |
| Admin | 1000 | 2000 |

### Performance Headers

All API responses include performance headers:

```http
X-Response-Time: 0.125s
X-DB-Queries: 3
X-Cache-Status: HIT
X-Rate-Limit-Remaining: 57
```
```

---

## **🧪 API Testing Documentation Standards**

### **✅ API Test Documentation Format**

```markdown
## API Testing Guide

### Test Categories

1. **Unit Tests**: Individual endpoint testing
2. **Integration Tests**: Cross-module API testing
3. **Performance Tests**: Load and stress testing
4. **Security Tests**: Authentication and authorization testing

### Test Example Template

```python
# tests/api/test_production_api.py
class TestProductionOrderAPI(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)
        
    def test_create_production_order_success(self):
        """Test successful production order creation"""
        # Given
        product = Product.objects.create(name='Test Product')
        data = {
            'product_id': product.id,
            'quantity': 100,
            'due_date': '2025-06-15'
        }
        
        # When
        response = self.client.post('/api/v1/production/orders/', data)
        
        # Then
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['quantity'], 100)
        self.assertTrue(
            ProductionOrder.objects.filter(id=response.data['id']).exists()
        )
    
    def test_create_production_order_invalid_data(self):
        """Test production order creation with invalid data"""
        # Given
        data = {
            'product_id': 999,  # Non-existent product
            'quantity': -10,    # Invalid quantity
        }
        
        # When
        response = self.client.post('/api/v1/production/orders/', data)
        
        # Then
        self.assertEqual(response.status_code, 400)
        self.assertIn('error_code', response.data)
        self.assertEqual(response.data['error_code'], 'ERR-VALID-250609-001')
```

### Postman Collection Example

```json
{
  "info": {
    "name": "Context7 ERP Production API",
    "description": "Production management API endpoints",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "item": [
    {
      "name": "Create Production Order",
      "request": {
        "method": "POST",
        "header": [
          {
            "key": "Authorization",
            "value": "Bearer {{jwt_token}}"
          }
        ],
        "body": {
          "mode": "raw",
          "raw": "{\n  \"product_id\": 15,\n  \"quantity\": 100,\n  \"priority\": \"high\",\n  \"due_date\": \"2025-06-15\"\n}"
        },
        "url": {
          "raw": "{{base_url}}/api/v1/production/orders/",
          "host": ["{{base_url}}"],
          "path": ["api", "v1", "production", "orders", ""]
        }
      },
      "response": []
    }
  ]
}
```
```

---

## **📚 API Documentation Maintenance**

### **🔄 Documentation Update Process**

```python
# scripts/update_api_docs.py
"""
Script to automatically update API documentation from code changes
"""

class APIDocumentationUpdater:
    def update_openapi_spec(self):
        """Update OpenAPI spec from Django REST Framework"""
        # Generate OpenAPI spec from DRF
        # Update YAML files
        # Validate spec integrity
        pass
    
    def update_code_examples(self):
        """Update code examples in documentation"""
        # Test all code examples
        # Update outdated examples
        # Generate new examples for new endpoints
        pass
    
    def validate_documentation(self):
        """Validate documentation consistency"""
        # Check for missing endpoints
        # Validate schema accuracy
        # Check example validity
        pass
```

### **📅 Documentation Review Checklist**

```markdown
## Monthly API Documentation Review

### Checklist Items
- [ ] All new endpoints documented
- [ ] OpenAPI spec updated
- [ ] Code examples tested and working
- [ ] Error codes documented
- [ ] Performance metrics updated
- [ ] Security guidelines current
- [ ] Integration guides updated
- [ ] Change log maintained
- [ ] User feedback incorporated
- [ ] Deprecated endpoints marked

### Review Process
1. **Technical Review**: Code-to-docs consistency
2. **Content Review**: Clarity and completeness
3. **User Experience Review**: Ease of understanding
4. **Performance Review**: Documentation load times
5. **Accessibility Review**: Screen reader compatibility
```

---

**📚 API Documentation Mottosu:** "İyi dokümantasyon, API'nin kullanılabilirliğini belirler. Context7 ERP API'leri her geliştirici için erişilebilir ve anlaşılır olmalıdır."

---

**🔄 Version:** v1.0 (Django ERP API Documentation System)  
**📅 Son Güncelleme:** 9 Haziran 2025  
**🏷️ Durum:** API Documentation Standards Aktif ✅  
**🎯 Scope:** Context7 Django ERP + Comprehensive API Documentation + OpenAPI Specification + Developer Experience 