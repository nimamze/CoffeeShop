from django.urls import path
from .views import ProductListApi

app_name = "shop"

urlpatterns = [
    path("products/", ProductListApi.as_view(), name="product_list"),
    path(
        "products/<str:name>/",
        ProductListApi.as_view(),
        name="product_list_by_category",
    ),
]
