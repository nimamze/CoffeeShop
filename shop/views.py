from django.shortcuts import get_object_or_404, render, redirect
from django.views import View
from django.views.generic.edit import UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.urls import reverse_lazy
from .models import ProductImage, Product, Category
from .forms import ProductForm
from django.utils.dateparse import parse_date

class ProductListView(ListView):
    model = Product
    template_name = 'shop/products_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        queryset = Product.objects.all()
        category_id = self.request.GET.get('category')
        date = self.request.GET.get('date')

        if category_id and category_id.isdigit():
            queryset = queryset.filter(category__id=category_id)

        if date:
            parsed_date = parse_date(date)
            if parsed_date:
                queryset = queryset.filter(date__date=parsed_date)

        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()

        category_id = self.request.GET.get('category')
        context['selected_category'] = category_id if category_id and category_id.isdigit() else ""

        context['selected_date'] = self.request.GET.get('date') or ""

        return context

class ProductDetailView(DetailView):

    model = Product
    template_name = 'shop/products_details.html'
    context_object_name = 'product'


class ProductUpdateView(UpdateView):

    model = Product
    form_class = ProductForm
    template_name = 'shop/product_edit.html'
    context_object_name = 'product'
    success_url = reverse_lazy('product_list')


class DeleteImage(View):
    template_name = 'shop/image_delete.html'

    def get(self, request, product_id, *args, **kwargs):
        product = get_object_or_404(Product, id=product_id)
        images = ProductImage.objects.filter(product=product)
        return render(request, self.template_name, {
            'images': images,
            'product': product,
        })

    def post(self, request, product_id, *args, **kwargs):
        image_ids = request.POST.getlist('delete_image')
        if image_ids:
            ProductImage.objects.filter(id__in=image_ids, product_id=product_id).delete()
        return redirect('product_edit', pk=product_id)


