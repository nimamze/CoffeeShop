from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import ListView, DetailView, DeleteView
from django.urls import reverse_lazy
from .models import ProductImage, Product, Category
from .forms import ProductImageForm
from .models import Product
from django.shortcuts import render
from django.views.generic import ListView

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
        date = self.request.GET.get('date')
        if category_id:
            queryset = queryset.filter(category__id=category_id)
        if date:
            queryset = queryset.filter(date=date)
        return queryset.distinct()

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['selected_category'] = self.request.GET.get('category')
        context['selected_date'] = self.request.GET.get('date')
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

class DeleteImage(DeleteView):

    template_name = 'image_delete.html'

    def get_queryset(self):
        queryset = ProductImage.objects.all()
        product_id = self.request.GET.get('product_id')
        print(product_id)
        if product_id:
            queryset = queryset.filter(product__id=product_id)
            print(product_id)
        
        return queryset.distinct()
    
    def get(self, request):
        images = self.get_queryset()
        product_id = request.GET.get('product_id')
        return render(request, self.template_name, {'images': images, 'product_id': product_id})
    
    def post(self, request):
        image_ids = request.POST.getlist('delete_image')
        product_id = request.GET.get('product_id')
        ProductImage.objects.filter(id__in=image_ids).delete()
        return redirect('product_edit', pk=product_id)
    
class MenuView(ListView) :
    model = Product
    template_name = 'menu.html'