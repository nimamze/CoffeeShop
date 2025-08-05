
from django.contrib import admin
from django.urls import path
from accounts.views import ProfileView,UpdateProfileView,UserFavoritesView,add_to_favorites,UserOrdersView,UserOrderDetailView
from .views import ProductList,ProductDetailView,CartAddView,CartItemsView
from .views import checkout,delete_item


urlpatterns = [
    path('',ProductList.as_view(),name='product_list'),
    path('category/<str:name>',ProductList.as_view(),name='category_filter'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product_details'),
    path('addFavorite/',add_to_favorites,name='add_to_favorites'),
    path('cart/add/<int:product_id>/', CartAddView.as_view(), name='cart_add'),
    path('cart/items/', CartItemsView.as_view(), name='cart_items'),
    path('cart/checkout/', checkout, name='cart_checkout'),
    path('cart/delete/<int:pk>/',delete_item,name='delete_item')
]
