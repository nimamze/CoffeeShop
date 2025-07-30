from django.urls import path
from .views import ProductListView, ProductDetailView, ProductUpdateView, DeleteImage
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('products/list/', ProductListView.as_view(), name='product_list'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product_details'),
    path('products/<int:pk>/edit/', ProductUpdateView.as_view(), name='product_edit'),
    path('products/images/delete/', DeleteImage.as_view(), name='product_image_delete'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
