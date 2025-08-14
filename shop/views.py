from django.urls import reverse
from django.views import View
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib import messages
from django.db.models import Avg
from .models import Product, Category, Order, OrderItem, Comment, Cart, CartItem
from .forms import CartAddForm, CommentForm
from django.core.paginator import Paginator
from django.views import View
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Product, Category


class ProductList(View):
    def get(self, request, name=None):
        categories = Category.objects.all()
        if name:
            category = get_object_or_404(Category, name=name)
            products = Product.objects.filter(categories=category)
        else:
            products = Product.objects.all()
        paginator = Paginator(products, 4)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        return render(
            request,
            "index.html",
            {
                "page_obj": page_obj,
                "categories": categories,
            },
        )


class ProductDetailView(DetailView):
    model = Product
    template_name = "shop/products_details.html"
    context_object_name = "product"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        product.refresh_from_db()
        context["form"] = CartAddForm()
        context["comment_form"] = CommentForm(prefix="comment")
        context["comments"] = self.get_comment_queryset()
        context["average_score"] = self.get_average_score()
        return context

    def post(self, request, pk):
        if not request.user.is_authenticated:
            return redirect("accounts:login")

        comment_form = CommentForm(request.POST, prefix="comment")
        product = get_object_or_404(Product, id=pk)

        if comment_form.is_valid():
            text = comment_form.cleaned_data["text"]
            score = comment_form.cleaned_data["score"]
            customer = request.user

            has_purchased = Order.objects.filter(
                customer=customer, order_items__product_name=product.name
            ).exists()

            Comment.objects.create(
                text=text,
                score=score,
                product=product,
                customer=customer,
                has_purchased=has_purchased,
            )

            messages.success(
                request, "کامنت شما ثبت شد و پس از تایید نمایش داده خواهد شد."
            )
        else:
            messages.error(request, "فرم نظر نامعتبر است.")

        return redirect(request.path_info)

    def get_comment_queryset(self):
        return (
            Comment.objects.select_related("customer")
            .filter(
                product=self.object,  # type: ignore
                is_confirmed=True,
            )
            .order_by("-created_at")
        )

    def get_average_score(self):
        comments = self.get_comment_queryset()
        return comments.aggregate(avg_score=Avg("score"))["avg_score"] or 0


class CartAddView(LoginRequiredMixin, View):
    def post(self, request, product_id):
        form = CartAddForm(request.POST)
        product = get_object_or_404(Product, id=product_id)

        if form.is_valid():
            quantity = form.cleaned_data["quantity"]
            cart, _ = Cart.objects.get_or_create(
                customer=request.user, cart_order__isnull=True
            )

            cart_item = CartItem.objects.filter(cart=cart, product=product).first()
            current_quantity_in_cart = cart_item.quantity if cart_item else 0
            total_quantity = current_quantity_in_cart + quantity

            if total_quantity > product.stock:
                messages.error(
                    request,
                    f"تعداد درخواستی بیشتر از موجودی محصول است. موجودی: {product.stock} عدد.",
                )
                return redirect(reverse("shop:product_details", args=[product.id]))  # type: ignore

            if cart_item:
                cart_item.quantity = total_quantity
                cart_item.save()
            else:
                CartItem.objects.create(cart=cart, product=product, quantity=quantity)

            product.stock = product.stock - total_quantity
            product.save()
            messages.success(request, "محصول با موفقیت به سبد خرید اضافه شد.")
        else:
            messages.error(request, "فرم نامعتبر است. لطفاً دوباره تلاش کنید.")

        return redirect(reverse("shop:product_details", args=[product.id]))  # type: ignore


class CartItemsView(LoginRequiredMixin, ListView):
    model = CartItem
    template_name = "shop/cart_items.html"
    context_object_name = "cart_items"

    def get_queryset(self):
        cart = (
            Cart.objects.filter(customer=self.request.user, cart_order__isnull=True)
            .order_by("-created_at")
            .first()
        )
        return (
            cart.cart_items.select_related("product")  # type: ignore
            if cart
            else CartItem.objects.none()
        )  # type: ignore

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = (
            Cart.objects.filter(customer=self.request.user, cart_order__isnull=True)
            .order_by("-created_at")
            .first()
        )
        context["cart"] = cart
        return context


@login_required
@transaction.atomic
def checkout(request):
    cart = (
        Cart.objects.filter(customer=request.user, cart_order__isnull=True)
        .order_by("-created_at")
        .first()
    )

    if not cart or not cart.cart_items.exists():  # type: ignore
        messages.error(request, "سبد خرید شما خالی است.")
        return redirect("shop:cart_items")

    # چک کردن موجودی کافی قبل از ثبت سفارش
    for item in cart.cart_items.select_related("product").all():  # type: ignore
        if item.quantity > item.product.stock:
            messages.error(
                request,
                f"محصول '{item.product.name}' به اندازه کافی موجود نیست. موجودی فعلی: {item.product.stock} عدد.",
            )
            return redirect("shop:cart_items")

    if hasattr(cart, "cart_order") and cart.cart_order:  # type: ignore
        messages.warning(request, "برای این سبد قبلاً سفارش ثبت شده است.")
        return redirect("shop:cart_items")

    order = Order.objects.create(
        customer=request.user, cart=cart, total_price=cart.get_total_price()
    )
    cart.cart_order = order  # type: ignore
    cart.save()

    for item in cart.cart_items.all():  # type: ignore
        OrderItem.objects.create(
            order=order,
            product_name=item.product.name,
            quantity=item.quantity,
            price_at_purchase=item.product.price,
        )

    cart.cart_items.all().delete()  # type: ignore
    Cart.objects.create(customer=request.user)

    messages.success(request, "سفارش شما با موفقیت ثبت شد.")
    return redirect("shop:cart_items")


@login_required
def delete_item(request, pk):
    item = get_object_or_404(CartItem, pk=pk, cart__customer=request.user)
    item.product.stock = item.product.stock + item.quantity
    item.product.save()
    item.delete()
    messages.success(request, "محصول با موفقیت از سبد خرید حذف شد.")
    return redirect("shop:cart_items")
