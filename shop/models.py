from django.db import models
from django.contrib.auth import get_user_model

CustomUser = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name="نام دسته")
    image = models.ImageField(
        upload_to="category_images/", verbose_name="تصویر دسته‌بندی"
    )

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=50, verbose_name="نام ماده اولیه")

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=50, verbose_name="نام محصول")
    description = models.TextField(blank=True, verbose_name="توضیحات")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="قیمت")
    availability = models.BooleanField(default=True, verbose_name="موجود است؟")
    date_added = models.DateTimeField(auto_now_add=True)
    stock = models.PositiveIntegerField(default=10, verbose_name="تعداد موجودی")
    categories = models.ManyToManyField(
        Category, related_name="category_products", verbose_name="دسته‌ها"
    )
    ingredients = models.ManyToManyField(
        Ingredient, related_name="ingredient_products", blank=True
    )

    def __str__(self):
        return self.name

    def get_main_image(self):
        main_img = self.product_images.filter(is_main=True).first()  # type: ignore
        return main_img.image.url if main_img else None


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="product_images"
    )
    image = models.ImageField(upload_to="product_images/")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_main = models.BooleanField(default=False, verbose_name="تصویر اصلی؟")

    def __str__(self):
        return f"تصویر محصول {self.product.name}"


class Favorite(models.Model):
    customer = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="customer_favorites"
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="product_favorites"
    )

    class Meta:
        unique_together = ("customer", "product")

    def __str__(self):
        return f"علاقه‌مندی‌های {self.customer.get_full_name()}"


class Comment(models.Model):
    SCORE_CHOICES = [(i, str(i)) for i in range(1, 6)]

    customer = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="customuser_comments"
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="comments"
    )
    score = models.IntegerField(choices=SCORE_CHOICES, verbose_name="امتیاز")
    text = models.TextField(max_length=500, verbose_name="متن نظر")
    created_at = models.DateTimeField(auto_now_add=True)
    is_confirmed = models.BooleanField(default=False)
    has_purchased = models.BooleanField(default=False)

    def __str__(self):
        return f"نظر {self.customer.get_full_name()} برای {self.product.name}"


class Cart(models.Model):
    customer = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="carts_customer"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"سبد خرید {self.customer.get_full_name()} - #{self.id}"  # type: ignore

    def get_total_price(self):
        return sum(item.get_total_price() for item in self.cart_items.all())  # type: ignore


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="cart_items")
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="product_cart_item"
    )
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} عدد از {self.product.name}"

    def get_total_price(self):
        return self.product.price * self.quantity


class Order(models.Model):
    STATUS_CHOICES = [
        ("pending", "در انتظار تایید"),
        ("confirmed", "تایید شده"),
        ("shipped", "ارسال شده"),
        ("delivered", "تحویل داده شده"),
        ("cancelled", "لغو شده"),
    ]

    customer = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="customuser_orders"
    )
    cart = models.OneToOneField(
        Cart, on_delete=models.CASCADE, related_name="cart_order"
    )
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending",
        verbose_name="وضعیت سفارش",
    )

    def __str__(self):
        return f"سفارش #{self.id} توسط {self.customer.get_full_name()}"  # type: ignore


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="order_items"
    )
    product_name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    price_at_purchase = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} عدد از {self.product_name}"


class Notification(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="customuser_notifications"
    )
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"پیام برای {self.user.username}"


