from django.shortcuts import render
from django.views import View

from .models import Product,Category

# Create your views here.




class ProductList(View):
    def get(self,request,name=None):
        products = Product.objects.all()
        categories = Category.objects.all()
        if name is not None:
            category = Category.objects.get(name=name)
            products = Product.objects.filter(categories=category)
        return render(request,'index.html',{'products':products , 'categories':categories})
