from django.shortcuts import render, redirect
from django.views.generic.edit import UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.urls import reverse_lazy
from .models import ProductImage, Product, Category


class ProductListView(ListView):

    model = Product
    template_name = 'shop/products_list.html'
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
        category_id = self.request.GET.get('category')
        if category_id and category_id.isdigit():
            context['selected_category'] = category_id 
        else:
            context['selected_category'] = ""

        context['selected_date'] = self.request.GET.get('date')
        return context


class ProductDetailView(DetailView):

    model = Product
    template_name = 'shop/products_details.html'
    context_object_name = 'product'


class ProductUpdateView(UpdateView):

    model = Product
    fields = ['name', 'price', 'availability', 'category', 'ingredient']
    template_name = 'shop/product_edit.html'
    context_object_name = 'product'
    success_url = reverse_lazy('product_list')


class DeleteImage(DeleteView):
    
    template_name = 'shop/image_delete.html'
    def get_queryset(self):
        queryset = ProductImage.objects.all()
        product_id = self.request.GET.get('product_id')
        if product_id:
            queryset = queryset.filter(product__id=product_id)
        return queryset.distinct()

    def get(self, request, *args, **kwargs):
        images = self.get_queryset()
        product_id = request.GET.get('product_id')
        return render(request, self.template_name, {'images': images, 'product_id': product_id})

    def post(self, request, *args, **kwargs):
        image_ids = request.POST.getlist('delete_image')
        product_id = request.GET.get('product_id')
        if image_ids:
            ProductImage.objects.filter(id__in=image_ids).delete()
        return redirect('product_edit', pk=product_id)

