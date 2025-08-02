from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

CustomUser = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name='نام دسته')
    image = models.ImageField(upload_to='category_images/', verbose_name='تصویر دسته‌بندی')

    def __str__(self):
        return self.name
    



class Ingredient(models.Model):
    name = models.CharField(max_length=50, verbose_name='نام ماده اولیه')

    def __str__(self):
        return self.name



class Product(models.Model):
    name = models.CharField(max_length=50, verbose_name='نام محصول')
    description = models.TextField(blank=True, verbose_name='توضیحات')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='قیمت')
    availability = models.BooleanField(default=True, verbose_name='موجود است؟')
    date_added = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField(Category, related_name='products', verbose_name='دسته‌ها')
    ingredients = models.ManyToManyField(Ingredient, related_name='products', blank=True)

    def __str__(self):
        return self.name
    
    def get_main_image(self):
        main_img = self.images.filter(is_main=True).first()
        return main_img.image.url if main_img else None



class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='product_images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_main = models.BooleanField(default=False, verbose_name='تصویر اصلی؟')

    def __str__(self):
        return f"Image of {self.product.name}"



class Favorite(models.Model):
    customer = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='favorites')
    products = models.ManyToManyField(Product, related_name='favorited_by', blank=True)

    def __str__(self):
        return f"Favorites of {self.customer.get_full_name()}"


class Comment(models.Model):
    SCORE_CHOICES = [(i, str(i)) for i in range(1, 6)]

    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='comments')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    score = models.IntegerField(choices=SCORE_CHOICES, verbose_name='امتیاز')
    text = models.TextField(max_length=500, verbose_name='متن نظر')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.customer.get_full_name()} on {self.product.name}"


class Cart(models.Model):
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='carts')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart #{self.id} for {self.customer.get_full_name()}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"


class Order(models.Model):
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='orders')
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE, related_name='order')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} by {self.customer.get_full_name()}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product_name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    price_at_purchase = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.product_name}"





























