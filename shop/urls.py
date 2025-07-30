from django.urls import path
from .views import ProductListView, ProductDetailView, ProductUpdateView, DeleteImage

urlpatterns = [
    path('products/list/', ProductListView.as_view(), name='product_list'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product_details'),
    path('products/<int:pk>/edit/', ProductUpdateView.as_view(), name='product_edit' ),
    path('products/images/delete/', DeleteImage.as_view(), name= "product_image_delete"),
]