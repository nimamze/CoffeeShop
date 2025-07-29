from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import ListView, DetailView
from django.urls import reverse_lazy
from .models import ProductImage, Product, Category
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
    def get_queryset(self):
        queryset = Product.objects.all()
        category_id = self.request.GET.get('category')
        if category_id:
            queryset = queryset.filter(category__id=category_id)
        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['selected_category'] = self.request.GET.get('category')
        return context

class ProductDetailView(DetailView):
    model = Product
    template_name ='products_details.html'
    context_object_name = 'product'

class ProductUpdateView(UpdateView):
    model = Product
    fields = ['name', 'price', 'availability', 'category', 'ingredient']
    template_name = 'product_edit.html'
    context_object_name = 'product'
    success_url = reverse_lazy('product_list') 