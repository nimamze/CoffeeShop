from django.urls import path
from accounts.views import add_to_favorites
from .views import (
    ProductList,
    ProductDetailView,
    CartAddView,
    CartItemsView,
    checkout,
    delete_item,
)

app_name = "shop"

urlpatterns = [
    path("", ProductList.as_view(), name="product_list"),
    path("category/<str:name>/", ProductList.as_view(), name="category_filter"),
    path("products/<int:pk>/", ProductDetailView.as_view(), name="product_details"),
    path("favorites/add/", add_to_favorites, name="add_to_favorites"),
    path("cart/add/<int:product_id>/", CartAddView.as_view(), name="cart_add"),
    path("cart/items/", CartItemsView.as_view(), name="cart_items"),
    path("cart/checkout/", checkout, name="cart_checkout"),
    path("cart/delete/<int:pk>/", delete_item, name="delete_item"),
]
