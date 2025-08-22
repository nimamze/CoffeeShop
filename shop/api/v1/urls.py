from django.urls import path
from .views import ProductListApi, ProductDetailApi, ProductImageEditApi


urlpatterns = [
    path("products/", ProductListApi.as_view(), name="product_list_api"),
    path(
        "products/<str:name>/",
        ProductListApi.as_view(),
        name="product_list_by_category_api",
    ),
    path("product/<int:pk>/", ProductDetailApi.as_view(), name="product_api"),
    path(
        "product/<int:pk>/edit-image/",
        ProductImageEditApi.as_view(),
        name="product_image_api",
    ),
]
