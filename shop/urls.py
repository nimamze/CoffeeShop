
from django.contrib import admin
from django.urls import path
from accounts.views import ProfileView,UpdateProfileView,UserFavoritesView,add_to_favorites,UserOrdersView,UserOrderDetailView
from shop.views import ProductList,ProductDetailView

urlpatterns = [
    path('',ProductList.as_view(),name='product_list'),
    path('category/<str:name>',ProductList.as_view(),name='category_filter'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product_details'),
    path('addFavorite/',add_to_favorites,name='add_to_favorites')
]
