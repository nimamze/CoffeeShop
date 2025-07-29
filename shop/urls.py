from django.urls import path
from .views import ProductImageView, ProductListView, ProductDetailView, ProductUpdateView

urlpatterns = [
    path('product-images/', ProductImageView.as_view(), name = 'product-image'),
    path('products/list/', ProductListView.as_view(), name='product_list'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product_details'),
    path('products/<int:pk>/edit/',ProductUpdateView.as_view(), name='product_edit' )
]