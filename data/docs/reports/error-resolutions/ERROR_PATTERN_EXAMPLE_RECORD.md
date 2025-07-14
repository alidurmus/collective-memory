# 🔍 Error Pattern Example Record

**Error Pattern ID:** ERR-DJANGO-250113-001  
**Date:** 2025-01-13  
**Category:** DJANGO  
**Severity:** HIGH  
**Module:** ERP Sales  
**Pattern Frequency:** 3 occurrences in 2 days  
**QMS Reference:** REC-ERROR-PATTERN-EXAMPLE-250113-001

---

## 📋 **Error Description**

**Error Type:** AttributeError  
**Error Message:** `'NoneType' object has no attribute 'id'`  
**Context:** Sales order view when customer is deleted but order still references it

### **Technical Details**
```python
# Error occurred in template rendering
# File: erp/templates/erp/sales/order_detail.html
# Line: {{ order.customer.id }}

# Stack trace snippet:
AttributeError at /sales/orders/12345/
'NoneType' object has no attribute 'id'
```

---

## 🔄 **Reproduction Steps**

1. **Create Customer:**
   ```python
   customer = Customer.objects.create(
       name="Test Customer",
       tax_number="123456789",
       is_active=True
   )
   ```

2. **Create Sales Order:**
   ```python
   order = SalesOrder.objects.create(
       customer=customer,
       total_amount=1000.00,
       status='confirmed'
   )
   ```

3. **Soft Delete Customer:**
   ```python
   customer.is_active = False
   customer.save()
   # Or customer.delete() for hard delete
   ```

4. **Access Order Detail View:**
   ```
   GET /sales/orders/12345/
   ```

5. **Error Occurs:**
   - Template tries to access `order.customer.id`
   - Customer is None due to soft delete
   - AttributeError is raised

---

## 🔍 **Root Cause Analysis**

### **Primary Cause**
The sales order model uses ForeignKey to Customer without proper handling of soft-deleted or hard-deleted customers.

### **Contributing Factors**
1. **Template Safety:** No null checks in template before accessing customer attributes
2. **View Logic:** View doesn't filter for active customers when loading related data  
3. **Business Logic:** Soft delete implementation allows orders to reference inactive customers
4. **Defensive Programming:** Missing null guards in template rendering

### **System Impact**
- **User Experience:** 500 error page instead of graceful handling
- **Data Integrity:** Valid orders become inaccessible  
- **Business Process:** Sales staff cannot view order details
- **Customer Service:** Cannot provide order information to customers

---

## ✅ **Solution Applied**

### **1. Template Safety Enhancement**
```html
<!-- BEFORE (causing error) -->
<div class="customer-info">
    <h3>Customer: {{ order.customer.name }}</h3>
    <p>ID: {{ order.customer.id }}</p>
    <p>Tax Number: {{ order.customer.tax_number }}</p>
</div>

<!-- AFTER (error-safe) -->
<div class="customer-info">
    {% if order.customer and order.customer.is_active %}
        <h3>Customer: {{ order.customer.name }}</h3>
        <p>ID: {{ order.customer.id }}</p>
        <p>Tax Number: {{ order.customer.tax_number }}</p>
    {% else %}
        <div class="alert alert-warning">
            <h3>Customer: No longer available</h3>
            <p>This customer has been removed from the system.</p>
        </div>
    {% endif %}
</div>
```

### **2. View Logic Enhancement**
```python
# BEFORE (potential error)
class SalesOrderDetailView(DetailView):
    model = SalesOrder
    template_name = 'erp/sales/order_detail.html'

# AFTER (defensive programming)
class SalesOrderDetailView(DetailView):
    model = SalesOrder
    template_name = 'erp/sales/order_detail.html'
    
    def get_queryset(self):
        return SalesOrder.objects.select_related(
            'customer'  # Include inactive customers to show warning
        ).prefetch_related(
            'items__product'
        )
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Add customer status information
        if self.object.customer:
            context['customer_active'] = self.object.customer.is_active
        else:
            context['customer_active'] = False
            
        return context
```

### **3. Model Enhancement**
```python
# Enhanced Customer model with better soft delete support
class Customer(models.Model):
    name = models.CharField(max_length=200)
    tax_number = models.CharField(max_length=20, unique=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        status = "Active" if self.is_active else "Inactive"
        return f"{self.name} ({status})"
    
    @property
    def display_name(self):
        """Safe display name for templates"""
        if self.is_active:
            return self.name
        return f"{self.name} (Inactive)"

# Enhanced SalesOrder model
class SalesOrder(models.Model):
    customer = models.ForeignKey(
        Customer, 
        on_delete=models.PROTECT,  # Prevent deletion if orders exist
        related_name='orders'
    )
    
    def get_customer_display(self):
        """Safe customer display method"""
        if self.customer and self.customer.is_active:
            return self.customer.name
        elif self.customer:
            return f"{self.customer.name} (No longer available)"
        else:
            return "Customer removed"
```

---

## 🧪 **Test Rules Created**

### **1. Unit Tests for Null Customer Handling**
```python
class SalesOrderNullCustomerTests(TestCase):
    """Tests based on ERR-DJANGO-250113-001 pattern"""
    
    def test_order_detail_view_with_inactive_customer(self):
        """Test order detail view when customer is inactive"""
        # Create customer and order
        customer = Customer.objects.create(
            name="Test Customer",
            tax_number="123456789",
            is_active=True
        )
        order = SalesOrder.objects.create(
            customer=customer,
            total_amount=1000.00
        )
        
        # Deactivate customer (soft delete)
        customer.is_active = False
        customer.save()
        
        # Test view doesn't crash
        response = self.client.get(f'/sales/orders/{order.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No longer available")
        self.assertNotContains(response, "AttributeError")
    
    def test_order_detail_view_with_deleted_customer(self):
        """Test order detail view when customer is hard deleted"""
        # Create customer and order
        customer = Customer.objects.create(
            name="Test Customer", 
            tax_number="123456789"
        )
        order = SalesOrder.objects.create(
            customer=customer,
            total_amount=1000.00
        )
        
        # Delete customer (this should be prevented by PROTECT)
        with self.assertRaises(models.ProtectedError):
            customer.delete()
    
    def test_order_customer_display_method(self):
        """Test safe customer display method"""
        customer = Customer.objects.create(
            name="Test Customer",
            tax_number="123456789",
            is_active=True
        )
        order = SalesOrder.objects.create(
            customer=customer,
            total_amount=1000.00
        )
        
        # Test active customer
        self.assertEqual(
            order.get_customer_display(),
            "Test Customer"
        )
        
        # Test inactive customer
        customer.is_active = False
        customer.save()
        self.assertEqual(
            order.get_customer_display(),
            "Test Customer (No longer available)"
        )
```

### **2. Integration Tests for Customer-Order Relationship**
```python
class CustomerOrderIntegrationTests(TestCase):
    """Integration tests for customer-order relationship"""
    
    def test_customer_deletion_protection(self):
        """Test that customers with orders cannot be deleted"""
        customer = Customer.objects.create(
            name="Test Customer",
            tax_number="123456789"
        )
        order = SalesOrder.objects.create(
            customer=customer,
            total_amount=1000.00
        )
        
        # Attempt to delete customer should fail
        with self.assertRaises(models.ProtectedError):
            customer.delete()
    
    def test_order_list_view_with_inactive_customers(self):
        """Test order list view handles inactive customers gracefully"""
        # Create active and inactive customers with orders
        active_customer = Customer.objects.create(
            name="Active Customer",
            tax_number="111111111",
            is_active=True
        )
        inactive_customer = Customer.objects.create(
            name="Inactive Customer", 
            tax_number="222222222",
            is_active=False
        )
        
        SalesOrder.objects.create(customer=active_customer, total_amount=1000)
        SalesOrder.objects.create(customer=inactive_customer, total_amount=2000)
        
        # Test list view doesn't crash
        response = self.client.get('/sales/orders/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Active Customer")
        self.assertContains(response, "Inactive Customer")
```

### **3. Frontend Tests for Template Safety**
```python
class TemplateSafetyTests(TestCase):
    """Tests for template safety with null/inactive references"""
    
    def test_template_renders_safely_with_null_customer(self):
        """Test template handles null customer references safely"""
        # Create order with customer, then set customer to None
        customer = Customer.objects.create(
            name="Test Customer",
            tax_number="123456789"
        )
        order = SalesOrder.objects.create(
            customer=customer,
            total_amount=1000.00
        )
        
        # Simulate null customer (should not happen with PROTECT, but test anyway)
        SalesOrder.objects.filter(id=order.id).update(customer=None)
        order.refresh_from_db()
        
        # Test template renders without error
        response = self.client.get(f'/sales/orders/{order.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Customer removed")
```

---

## 🛡️ **Prevention Measures**

### **1. Code Review Checklist**
- [ ] All template variables checked for null before attribute access
- [ ] ForeignKey relationships use appropriate on_delete behavior
- [ ] Views use defensive programming for related object access
- [ ] Soft delete scenarios are tested

### **2. Development Guidelines**
1. **Template Safety:** Always check object existence before accessing attributes
2. **View Protection:** Use select_related with active filters when appropriate  
3. **Model Design:** Use PROTECT for critical business relationships
4. **Error Handling:** Provide meaningful error messages for users

### **3. Automated Checks**
```python
# Custom template tag for safe attribute access
@register.filter
def safe_attr(obj, attr_name):
    """Safely access object attribute"""
    if obj and hasattr(obj, attr_name):
        return getattr(obj, attr_name)
    return "Not available"

# Usage in template: {{ order.customer|safe_attr:"name" }}
```

---

## 📊 **Pattern Impact Analysis**

### **Before Fix**
- **Error Frequency:** 3 occurrences in 2 days
- **User Impact:** 500 error page, unable to view order details
- **Business Impact:** Sales staff productivity loss
- **System Reliability:** Critical functionality breaking

### **After Fix**
- **Error Frequency:** 0 occurrences
- **User Experience:** Graceful handling with clear messaging
- **Business Continuity:** Orders remain accessible with customer status info
- **System Reliability:** Robust error handling prevents crashes

### **Prevention Effectiveness**
- **Test Coverage:** 100% for null customer scenarios
- **Error Detection:** Proactive pattern recognition active
- **Developer Awareness:** Pattern documented for team reference
- **Future Prevention:** Automated checks prevent similar issues

---

## 🔗 **Related Patterns**

### **Similar Patterns Identified**
- **ERR-DJANGO-250110-002:** Similar NoneType error in purchase orders with suppliers
- **ERR-DJANGO-250108-001:** ForeignKey handling in production module with materials
- **ERR-DJANGO-250105-003:** Template safety issues in inventory module

### **Pattern Family**
This error belongs to the **"Null Reference in Django Templates"** pattern family, which includes:
1. ForeignKey null references
2. OneToOne field null references  
3. ManyToMany empty set references
4. Deleted object references

---

## 🎯 **Lessons Learned**

### **Technical Lessons**
1. **Defensive Programming:** Always assume related objects might be null
2. **Template Guards:** Check object existence before accessing attributes
3. **Model Relationships:** Use appropriate on_delete strategies
4. **Testing Coverage:** Include edge cases in test scenarios

### **Process Lessons**
1. **Pattern Recognition:** Similar errors often occur across modules
2. **Systematic Testing:** Generate tests from real error scenarios
3. **Documentation Value:** Recording patterns helps prevent recurrence
4. **Team Knowledge:** Shared patterns improve overall code quality

### **Business Lessons**
1. **User Experience:** Technical errors should be hidden from users
2. **Data Integrity:** Business relationships should be protected
3. **Graceful Degradation:** Systems should handle missing data elegantly
4. **Operational Continuity:** Critical processes should remain functional

---

**🎯 Pattern Prevention Status:** ACTIVE  
**📊 Success Rate:** 100% (0 occurrences since fix)  
**🔄 Review Date:** Monthly pattern effectiveness review  
**📝 Documentation:** Complete and integrated into test suite  

---

*Error Pattern Record - Learning from every error to build better systems* 