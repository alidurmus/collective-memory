"""
Context7 ERP - Django Kod Pattern Örnekleri
Version: v2.2.0-glassmorphism-enhanced
Source: Çeşitli dosyalar
Purpose: Django best practices - büyük kod örnekleri
"""

from django.db import models, transaction
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q, Sum, Count, Avg
from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from decimal import Decimal
import logging

logger = logging.getLogger(__name__)

# =============================
# 1. MODEL PATTERN ÖRNEKLERİ
# =============================

class BaseModel(models.Model):
    """Tüm modeller için base class"""
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturulma Tarihi")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Güncellenme Tarihi")
    is_active = models.BooleanField(default=True, verbose_name="Aktif mi?")
    
    class Meta:
        abstract = True
        ordering = ['-created_at']

class Category(BaseModel):
    """Kategori modeli örneği"""
    name = models.CharField(max_length=100, unique=True, verbose_name="Kategori Adı")
    code = models.CharField(max_length=20, unique=True, verbose_name="Kategori Kodu")
    description = models.TextField(blank=True, null=True, verbose_name="Açıklama")
    parent = models.ForeignKey('self', on_delete=models.CASCADE, 
                              blank=True, null=True, verbose_name="Üst Kategori")
    
    class Meta:
        verbose_name = "Kategori"
        verbose_name_plural = "Kategoriler"
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('erp:category_detail', kwargs={'pk': self.pk})
    
    def get_children(self):
        """Alt kategorileri getir"""
        return self.category_set.filter(is_active=True)
    
    def get_all_children(self):
        """Tüm alt kategorileri recursive olarak getir"""
        children = []
        for child in self.get_children():
            children.append(child)
            children.extend(child.get_all_children())
        return children

class Product(BaseModel):
    """Ürün modeli örneği"""
    name = models.CharField(max_length=200, verbose_name="Ürün Adı")
    code = models.CharField(max_length=50, unique=True, verbose_name="Ürün Kodu")
    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name="Kategori")
    description = models.TextField(blank=True, null=True, verbose_name="Açıklama")
    price = models.DecimalField(max_digits=10, decimal_places=2, 
                               validators=[MinValueValidator(Decimal('0.01'))],
                               verbose_name="Fiyat")
    stock_quantity = models.IntegerField(default=0, 
                                       validators=[MinValueValidator(0)],
                                       verbose_name="Stok Miktarı")
    min_stock_level = models.IntegerField(default=10, verbose_name="Minimum Stok Seviyesi")
    image = models.ImageField(upload_to='products/', blank=True, null=True, verbose_name="Resim")
    
    class Meta:
        verbose_name = "Ürün"
        verbose_name_plural = "Ürünler"
        ordering = ['name']
        indexes = [
            models.Index(fields=['code']),
            models.Index(fields=['category', 'is_active']),
        ]
    
    def __str__(self):
        return f"{self.code} - {self.name}"
    
    def get_absolute_url(self):
        return reverse('erp:product_detail', kwargs={'pk': self.pk})
    
    @property
    def is_low_stock(self):
        """Stok seviyesi düşük mü?"""
        return self.stock_quantity <= self.min_stock_level
    
    def update_stock(self, quantity, operation='add'):
        """Stok güncelleme işlemi"""
        with transaction.atomic():
            if operation == 'add':
                self.stock_quantity += quantity
            elif operation == 'subtract':
                if self.stock_quantity >= quantity:
                    self.stock_quantity -= quantity
                else:
                    raise ValueError("Yetersiz stok!")
            self.save()

# =============================
# 2. VIEW PATTERN ÖRNEKLERİ
# =============================

class ProductListView(LoginRequiredMixin, ListView):
    """Ürün listesi view örneği"""
    model = Product
    template_name = 'erp/product_list.html'
    context_object_name = 'products'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = Product.objects.filter(is_active=True).select_related('category')
        
        # Arama filtresi
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) | 
                Q(code__icontains=search) |
                Q(description__icontains=search)
            )
        
        # Kategori filtresi
        category_id = self.request.GET.get('category')
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        
        # Stok filtresi
        stock_filter = self.request.GET.get('stock_filter')
        if stock_filter == 'low':
            queryset = queryset.filter(stock_quantity__lte=models.F('min_stock_level'))
        elif stock_filter == 'zero':
            queryset = queryset.filter(stock_quantity=0)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(is_active=True)
        context['total_products'] = self.get_queryset().count()
        context['low_stock_count'] = Product.objects.filter(
            is_active=True,
            stock_quantity__lte=models.F('min_stock_level')
        ).count()
        return context

class ProductDetailView(LoginRequiredMixin, DetailView):
    """Ürün detay view örneği"""
    model = Product
    template_name = 'erp/product_detail.html'
    context_object_name = 'product'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        
        # İlişkili veriler
        context['stock_movements'] = product.stockmovement_set.select_related(
            'transaction_type'
        ).order_by('-created_at')[:10]
        
        # İstatistikler
        context['total_sales'] = product.salesorderitem_set.aggregate(
            total=Sum('quantity')
        )['total'] or 0
        
        return context

class ProductCreateView(LoginRequiredMixin, CreateView):
    """Ürün oluşturma view örneği"""
    model = Product
    fields = ['name', 'code', 'category', 'description', 'price', 
              'stock_quantity', 'min_stock_level', 'image']
    template_name = 'erp/product_form.html'
    
    def form_valid(self, form):
        try:
            with transaction.atomic():
                response = super().form_valid(form)
                messages.success(self.request, f"Ürün '{self.object.name}' başarıyla oluşturuldu.")
                logger.info(f"Product created: {self.object.code} by {self.request.user}")
                return response
        except Exception as e:
            messages.error(self.request, f"Ürün oluşturulurken hata oluştu: {str(e)}")
            logger.error(f"Product creation error: {str(e)}")
            return self.form_invalid(form)

# =============================
# 3. API VIEW PATTERN ÖRNEKLERİ
# =============================

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def product_api_list(request):
    """Ürün listesi API endpoint örneği"""
    try:
        # Query parameters
        search = request.GET.get('search', '')
        category_id = request.GET.get('category_id')
        page = int(request.GET.get('page', 1))
        per_page = int(request.GET.get('per_page', 10))
        
        # Queryset oluşturma
        queryset = Product.objects.filter(is_active=True).select_related('category')
        
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) | Q(code__icontains=search)
            )
        
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        
        # Pagination
        paginator = Paginator(queryset, per_page)
        page_obj = paginator.get_page(page)
        
        # Serialization
        products = []
        for product in page_obj:
            products.append({
                'id': product.id,
                'name': product.name,
                'code': product.code,
                'category': {
                    'id': product.category.id,
                    'name': product.category.name
                },
                'price': str(product.price),
                'stock_quantity': product.stock_quantity,
                'is_low_stock': product.is_low_stock,
                'created_at': product.created_at.isoformat()
            })
        
        return Response({
            'success': True,
            'data': products,
            'pagination': {
                'current_page': page,
                'total_pages': paginator.num_pages,
                'total_items': paginator.count,
                'per_page': per_page
            }
        })
        
    except Exception as e:
        logger.error(f"Product API list error: {str(e)}")
        return Response({
            'success': False,
            'error': 'Internal server error'
        }, status=500)

class ProductViewSet(viewsets.ModelViewSet):
    """Product ViewSet örneği"""
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'code', 'description']
    ordering_fields = ['name', 'code', 'price', 'created_at']
    ordering = ['-created_at']
    
    def get_queryset(self):
        queryset = super().get_queryset().select_related('category')
        
        # Custom filters
        category_id = self.request.query_params.get('category_id')
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        
        stock_filter = self.request.query_params.get('stock_filter')
        if stock_filter == 'low':
            queryset = queryset.filter(stock_quantity__lte=models.F('min_stock_level'))
        elif stock_filter == 'zero':
            queryset = queryset.filter(stock_quantity=0)
        
        return queryset
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

# =============================
# 4. UTILITY FUNCTIONS
# =============================

def get_dashboard_stats():
    """Dashboard istatistikleri"""
    stats = {
        'total_products': Product.objects.filter(is_active=True).count(),
        'low_stock_products': Product.objects.filter(
            is_active=True,
            stock_quantity__lte=models.F('min_stock_level')
        ).count(),
        'total_categories': Category.objects.filter(is_active=True).count(),
        'total_stock_value': Product.objects.filter(is_active=True).aggregate(
            total=Sum(models.F('stock_quantity') * models.F('price'))
        )['total'] or Decimal('0')
    }
    return stats

def bulk_update_products(product_ids, update_data):
    """Toplu ürün güncelleme"""
    with transaction.atomic():
        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            for field, value in update_data.items():
                setattr(product, field, value)
            product.save()
        return products.count()

# =============================
# 5. CUSTOM DECORATORS
# =============================

def require_ajax(view_func):
    """AJAX isteği gereksinimi decorator"""
    def wrapper(request, *args, **kwargs):
        if not request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'error': 'AJAX request required'}, status=400)
        return view_func(request, *args, **kwargs)
    return wrapper

def log_action(action_name):
    """İşlem loglama decorator"""
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            start_time = timezone.now()
            try:
                result = view_func(request, *args, **kwargs)
                logger.info(f"Action '{action_name}' completed by {request.user} in {timezone.now() - start_time}")
                return result
            except Exception as e:
                logger.error(f"Action '{action_name}' failed by {request.user}: {str(e)}")
                raise
        return wrapper
    return decorator

# =============================
# 6. CUSTOM MANAGERS
# =============================

class ProductManager(models.Manager):
    """Custom Product Manager"""
    
    def active(self):
        return self.filter(is_active=True)
    
    def low_stock(self):
        return self.filter(
            is_active=True,
            stock_quantity__lte=models.F('min_stock_level')
        )
    
    def by_category(self, category):
        return self.filter(category=category, is_active=True)
    
    def search(self, query):
        return self.filter(
            Q(name__icontains=query) |
            Q(code__icontains=query) |
            Q(description__icontains=query),
            is_active=True
        )

# =============================
# 7. FORM VALIDATION ÖRNEKLERİ
# =============================

from django import forms

class ProductForm(forms.ModelForm):
    """Product form örneği"""
    
    class Meta:
        model = Product
        fields = ['name', 'code', 'category', 'description', 'price', 
                 'stock_quantity', 'min_stock_level', 'image']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'price': forms.NumberInput(attrs={'step': '0.01'}),
        }
    
    def clean_code(self):
        code = self.cleaned_data['code']
        if Product.objects.filter(code=code).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Bu kod zaten kullanılıyor.")
        return code.upper()
    
    def clean_price(self):
        price = self.cleaned_data['price']
        if price <= 0:
            raise forms.ValidationError("Fiyat sıfırdan büyük olmalıdır.")
        return price
    
    def clean(self):
        cleaned_data = super().clean()
        stock_quantity = cleaned_data.get('stock_quantity')
        min_stock_level = cleaned_data.get('min_stock_level')
        
        if stock_quantity is not None and min_stock_level is not None:
            if min_stock_level < 0:
                raise forms.ValidationError("Minimum stok seviyesi negatif olamaz.")
        
        return cleaned_data

# =============================
# 8. CELERY TASK ÖRNEKLERİ
# =============================

from celery import shared_task

@shared_task
def send_low_stock_alert():
    """Düşük stok uyarısı gönder"""
    try:
        low_stock_products = Product.objects.filter(
            is_active=True,
            stock_quantity__lte=models.F('min_stock_level')
        )
        
        if low_stock_products.exists():
            # Email gönderimi veya bildirim
            logger.info(f"Low stock alert sent for {low_stock_products.count()} products")
            return f"Alert sent for {low_stock_products.count()} products"
        
        return "No low stock products found"
        
    except Exception as e:
        logger.error(f"Low stock alert task failed: {str(e)}")
        raise

@shared_task
def export_products_to_excel():
    """Ürünleri Excel'e aktar"""
    try:
        import pandas as pd
        from django.conf import settings
        import os
        
        products = Product.objects.filter(is_active=True).select_related('category')
        
        data = []
        for product in products:
            data.append({
                'Kod': product.code,
                'Ad': product.name,
                'Kategori': product.category.name,
                'Fiyat': float(product.price),
                'Stok': product.stock_quantity,
                'Min Stok': product.min_stock_level,
                'Oluşturulma': product.created_at.strftime('%d.%m.%Y')
            })
        
        df = pd.DataFrame(data)
        file_path = os.path.join(settings.MEDIA_ROOT, 'exports', 'products.xlsx')
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        df.to_excel(file_path, index=False)
        
        logger.info(f"Products exported to Excel: {file_path}")
        return file_path
        
    except Exception as e:
        logger.error(f"Excel export task failed: {str(e)}")
        raise 