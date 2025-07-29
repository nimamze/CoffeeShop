from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.views.generic import ListView, DetailView
from django.urls import reverse_lazy
from .models import ProductImage, Product
from .forms import ProductImageForm

# Create your views here.
class ProductImageView(CreateView):
    model = ProductImage
    form_class = ProductImageForm
    template_name = 'product_image_form.html'
    success_url = reverse_lazy('home')

class ProductListView(ListView):
    model = Product
    template_name = 'products_list.html'
    context_object_name = 'products'

class ProductDetailView(DetailView):
    model = Product
    template_name ='products_details.html'
    context_object_name = 'product'