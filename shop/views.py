from django.shortcuts import render
from django.views import View
from django.shortcuts import get_object_or_404, render, redirect
from django.views import View
from django.views.generic.edit import UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.urls import reverse_lazy
from .models import ProductImage, Product, Category
from django.utils.dateparse import parse_date
from .models import Product,Category

class ProductList(View):
    def get(self,request,name=None):
        products = Product.objects.all()
        categories = Category.objects.all()
        if name is not None:
            category = Category.objects.get(name=name)
            products = Product.objects.filter(categories=category)
        return render(request,'index.html',{'products':products , 'categories':categories})

class ProductDetailView(DetailView):

    model = Product
    template_name = 'shop/products_details.html'
    context_object_name = 'product'


