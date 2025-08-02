
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('',views.ProductList.as_view(),name='product_list'),
    path('category/<str:name>',views.ProductList.as_view(),name='category_filter'),
]
