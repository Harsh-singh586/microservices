from django.urls import path
from . import views

urlpatterns = [
    path('categories/', views.CategoryListCreateView.as_view(), name='category-list-create'),
    path('categories/<int:pk>/', views.CategoryDetailView.as_view(), name='category-detail'),
    path('products/', views.ProductListCreateView.as_view(), name='product-list-create'),
    path('products/<int:pk>/', views.ProductDetailView.as_view(), name='product-detail'),
    path('api/product/<int:product_id>/', views.product_by_id, name='product-by-id'),
    path('api/check-stock/', views.check_stock, name='check-stock'),
    path('api/update-stock/', views.update_stock, name='update-stock'),
]
