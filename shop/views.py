from django.urls import reverse
from django.views import View
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import ListView, DetailView
from .models import Product, Category, Order, OrderItem, Comment, Cart, CartItem
from .forms import CartAddForm, CommentFrom
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib import messages
from django.db.models import Avg


class ProductList(View):
    def get(self, request, name=None):
        products = Product.objects.all()
        categories = Category.objects.all()
        if name is not None:
            category = Category.objects.get(name=name)
            products = Product.objects.filter(categories=category)
        return render(
            request, "index.html", {"products": products, "categories": categories}
        )


class ProductDetailView(DetailView):
    model = Product
    template_name = "shop/products_details.html"
    context_object_name = "product"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = CartAddForm()
        context["comment_form"] = CommentFrom(prefix="comment")
        context["comments"] = self.get_comment_queryset()
        context["average_score"] = self.get_average_score()
        return context

    def post(self, request, pk):
        if not request.user.is_authenticated:
            return redirect("login")

        comment_form = CommentFrom(request.POST, prefix="comment")
        if comment_form.is_valid():
            text = comment_form.cleaned_data["text"]
            score = comment_form.cleaned_data["score"]
            product = get_object_or_404(Product, id=pk)
            customer = request.user
            has_purchased = Order.objects.filter(
                customer=customer, items__product_name=product.name
            ).exists()

            Comment.objects.create(
                text=text,
                score=score,
                product=product,
                customer=customer,
                has_purchased=has_purchased,
            )

            messages.success(
                request, "کامنت شما ثبت شد. پس از تأیید توسط ادمین نمایش داده خواهد شد."
            )
        else:
            messages.error(request, "فرم کامنت نامعتبر است.")

        return redirect(request.path_info)

    def get_comment_queryset(self):
        comments = (
            Comment.objects.select_related("customer")
            .filter(product=self.object, is_confirmed=True)  # type: ignore
            .order_by("-created_at")
        )
        return comments

    def get_average_score(self):
        comments = self.get_comment_queryset()
        avg = comments.aggregate(avg_score=Avg("score"))["avg_score"] or 0
        return avg


class CartAddView(LoginRequiredMixin, View):
    def post(self, request, product_id):
        form = CartAddForm(request.POST)
        product = get_object_or_404(Product, id=product_id)

        if form.is_valid():
            quantity = form.cleaned_data["quantity"]

            cart = (
                Cart.objects.filter(customer=request.user)
                .order_by("-created_at")
                .first()
            )
            if not cart:
                cart = Cart.objects.create(customer=request.user)

            cart_item, created = CartItem.objects.get_or_create(
                cart=cart, product=product, defaults={"quantity": quantity}
            )
            if created:
                messages.success(request, " با موفقیت به سبد خرید اضافه شد.")
            else:
                cart_item.quantity += quantity
                cart_item.save()
                messages.success(request, " با موفقیت به سبد خرید اضافه شد.")

        else:
            messages.error(request, "فرم نامعتبر است. لطفاً مجدداً تلاش کنید.")

        return redirect(reverse("product_details", args=[product.id]))


class CartItemsView(LoginRequiredMixin, ListView):
    model = CartItem
    template_name = "shop/cart_items.html"
    context_object_name = "cart_items"

    def get_queryset(self):
        cart = (
            Cart.objects.filter(customer=self.request.user)
            .order_by("-created_at")
            .first()
        )
        return cart.items.select_related("product") if cart else CartItem.objects.none()  # type: ignore

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = (
            Cart.objects.filter(customer=self.request.user)
            .order_by("-created_at")
            .first()
        )
        context["cart"] = cart
        return context


@login_required
@transaction.atomic
def checkout(request):
    cart = (
        Cart.objects.filter(customer=request.user, order__isnull=True)
        .order_by("-created_at")
        .first()
    )

    if not cart:
        cart = Cart.objects.create(customer=request.user)

    if not cart.items.exists():  # type: ignore
        messages.error(request, "سبد خرید شما خالی است.")
        return redirect("cart_items")

    if hasattr(cart, "order"):
        messages.warning(request, "برای این سبد قبلاً سفارش ثبت شده است.")
        return redirect("cart_items")

    order = Order.objects.create(
        customer=request.user, cart=cart, total_price=cart.get_total_price()
    )

    for item in cart.items.all():  # type: ignore
        OrderItem.objects.create(
            order=order,
            product_name=item.product.name,
            quantity=item.quantity,
            price_at_purchase=item.product.price,
        )

    cart.items.all().delete()  # type: ignore

    Cart.objects.create(customer=request.user)

    messages.success(request, "سفارش شما با موفقیت ثبت شد.")
    return redirect("cart_items")


@login_required
def delete_item(request, pk):
    item = get_object_or_404(CartItem, pk=pk, cart__customer=request.user)
    item.delete()
    messages.success(request, "آیتم با موفقیت از سبد خرید حذف شد.")
    return redirect("cart_items")
