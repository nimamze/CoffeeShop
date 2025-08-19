from django.urls import path
from .views import ProductListApi, AddFavoriteApi


urlpatterns = [
    path("products/", ProductListApi.as_view(), name="product_list"),
    path(
        "products/<str:name>/",
        ProductListApi.as_view(),
        name="product_list_by_category",
    ),
    path("add-favorite/<int:pk>/", AddFavoriteApi.as_view(), name="add_favorite"),
]
