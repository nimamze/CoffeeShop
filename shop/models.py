from django.db import models
from accounts.models import Customer


class Cart(models.Model):

    name = models.CharField(max_length=50)
    def __str__(self):
        return f"Cart: {self.name}"


class Order(models.Model):

    date = models.DateField(auto_now_add=True)
    amount = models.IntegerField()
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='customer_orders')
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_orders')

    def __str__(self):
        return f"Order {self.pk} at {self.date}"


class Category(models.Model):
    
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='category_images/')
    def __str__(self):
        return self.name


class Ingredient(models.Model):

    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name


class Product(models.Model):

    name = models.CharField(max_length=50)
    price = models.PositiveIntegerField()
    date = models.DateField(auto_now_add=True)
    availability = models.BooleanField(default=True)
    category = models.ManyToManyField(Category, related_name='category_products')
    ingredient = models.ManyToManyField(Ingredient, related_name='ingredient_products')
    order = models.ManyToManyField(Order, related_name='products', blank=True)

    def __str__(self):
        return self.name


class ProductImage(models.Model):

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_image')
    image = models.ImageField(upload_to='product_images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_main = models.BooleanField(default=False)

    # def delete(self, using = ..., keep_parents = ...):
    #     self.image.delete()
    #     return super().delete(using, keep_parents)

    def __str__(self):
        return f"product image for {self.product.name} added"

class Favorite(models.Model):

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='customer_favorites')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_favorited')
    def __str__(self):
        return f"{self.customer.first_name} {self.customer.last_name} favorited {self.product.name}"


class Comment(models.Model):

    SCORE_CHOICES = [(i, str(i)) for i in range(1, 6)]
    text = models.TextField(max_length=50)
    score = models.IntegerField(choices=SCORE_CHOICES)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_comments')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='customer_comments')

    def __str__(self):
        return f"{self.customer.first_name}'s comment on {self.product.name}"
