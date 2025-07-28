from django.urls import path
from .views import ProductImageView

urlpatterns = [
    path('product-images/',ProductImageView.as_view(), name = 'product-image')
]