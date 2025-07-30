from django.shortcuts import render
from django.views.generic import ListView
# Create your views here.
from .models import Product


class MenuView(ListView) :
    model = Product
    template_name = 'menu.html'
    context_object_name = 'obj'