from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .models import ProductImage
from .forms import ProductImageForm

# Create your views here.
class ProductImageView(CreateView):
    model = ProductImage
    form_class = ProductImageForm
    template_name = 'product_image_form.html'
    success_url = reverse_lazy('home')