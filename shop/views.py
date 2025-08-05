from django.shortcuts import render
from django.views import View
from django.shortcuts import get_object_or_404, render, redirect
from django.views import View
from django.views.generic.edit import UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.urls import reverse_lazy
from .models import ProductImage, Product, Category,Order,OrderItem,Comment
from django.utils.dateparse import parse_date
from .models import Product,Category,Cart,CartItem
from .forms import CartAddForm , CommentFrom
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib import messages
from django.db.models import Avg

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CartAddForm() 
        context['comment_form'] = CommentFrom(prefix='comment') 
        context['comments'] = self.get_comment_queryset()
        context['average_score'] = self.get_average_score()
        return context
    
    def post(self, request, pk):
        if not request.user.is_authenticated:
            return redirect('login')
        
        comment_form = CommentFrom(request.POST, prefix='comment')
        if comment_form.is_valid():
            text = comment_form.cleaned_data['text']
            score = comment_form.cleaned_data['score']
            product = get_object_or_404(Product, id=pk)
            customer = request.user
            has_purchased = Cart.objects.filter(customer=customer,items__product=product).exists()

            comment = Comment.objects.create(text= text, score = score, product=product, customer=customer, has_purchased=has_purchased)
            comment.save()
        return redirect(request.path_info)
    
    def get_comment_queryset(self):
        comments = Comment.objects.select_related('customer').filter(product=self.object, is_confirmed=True).order_by('-created_at')
        return comments

    def get_average_score(self):
        comments = self.get_comment_queryset()
        avg = comments.aggregate(avg_score=Avg('score'))['avg_score'] or 0
        return avg


class CartAddView(LoginRequiredMixin, View):
    def post(self, request, product_id):
        form = CartAddForm(request.POST)
        product = get_object_or_404(Product, id=product_id)

        if form.is_valid():
            quantity = form.cleaned_data['quantity']

            # گرفتن آخرین سبد خرید کاربر یا ساختن یکی جدید
            cart = Cart.objects.filter(customer=request.user).order_by('-created_at').first()
            if not cart:
                cart = Cart.objects.create(customer=request.user)

            # افزودن محصول به سبد
            cart_item, created = CartItem.objects.get_or_create(
                cart=cart,
                product=product,
                defaults={'quantity': quantity}
            )
            if not created:
                cart_item.quantity += quantity
                cart_item.save()

        return redirect('product_list')


class CartItemsView(LoginRequiredMixin, ListView):
    model = CartItem
    template_name = 'shop/cart_items.html'
    context_object_name = 'cart_items'

    def get_queryset(self):
        cart = Cart.objects.filter(customer=self.request.user).order_by('-created_at').first()
        return cart.items.select_related('product') if cart else CartItem.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = Cart.objects.filter(customer=self.request.user).order_by('-created_at').first()
        context['cart'] = cart
        return context


@login_required
@transaction.atomic
def checkout(request):
    
    cart = Cart.objects.filter(customer=request.user, order__isnull=True).order_by('-created_at').first()
    
    if not cart:
        cart = Cart.objects.create(customer=request.user)
    
    if not cart.items.exists():
        messages.error(request, "سبد خرید شما خالی است.")
        return redirect('cart_items')
    
    if hasattr(cart, 'order'):
        messages.warning(request, "برای این سبد قبلاً سفارش ثبت شده است.")
        return redirect('cart_items')
    
    order = Order.objects.create(
        customer=request.user,
        cart=cart,
        total_price=cart.get_total_price()
    )
    
    for item in cart.items.all():
        OrderItem.objects.create(
            order=order,
            product_name=item.product.name,
            quantity=item.quantity,
            price_at_purchase=item.product.price
        )
    
    cart.items.all().delete()

    
    Cart.objects.create(customer=request.user)

    messages.success(request, "سفارش شما با موفقیت ثبت شد.")
    return redirect('cart_items')

@login_required
def delete_item(request,pk):
    item = get_object_or_404(CartItem, pk=pk, cart__customer=request.user)
    item.delete()
    messages.success(request, "آیتم با موفقیت از سبد خرید حذف شد.")
    return redirect('cart_items')  