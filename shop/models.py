from django.db import models
from accounts.models import CustomUser

class Order(models.Model):

    date = models.DateField(auto_now_add=True)
    amount = models.IntegerField()
    customer = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='customer_order')
    cart = models.ForeignKey('Cart',on_delete=models.CASCADE,related_name='cart_order')

    def __str__(self) -> str:
        return f"order at {self.date}"

class Cart(models.Model):
    
    name = models.CharField(max_length=50)

    def __str__(self) -> str:
        return f"cart {self.name} added"

class Category(models.Model):
    
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='category_image/')

    def __str__(self) -> str:
        return f"{self.name}"

class Favorite(models.Model):

    customer = models.OneToOneField(CustomUser,on_delete=models.CASCADE,related_name='customer_favorite')

    def __str__(self) -> str:
        return f"{self.customer.first_name} {self.customer.last_name} favorite added"

class Comment(models.Model):

    score_choices = [('1','1'),('2','2'),('3','3'),('4','4'),('5','5')]
    text = models.TextField(max_length=50)
    score = models.CharField(choices=score_choices)
    product = models.ForeignKey('Product',on_delete=models.CASCADE,related_name='product_comment')
    customer = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='customer_comment')

    def __str__(self) -> str:
        return f"comment {self.text} for user {self.customer.first_name} {self.customer.last_name} added"

class Ingredient(models.Model):

    name = models.CharField(max_length=50)

    def __str__(self) -> str:
        return f"ingredient {self.name} added"


class Product(models.Model):

    name = models.CharField(max_length=50)
    price = models.PositiveIntegerField()
    date = models.DateField(auto_now_add=True)
    availability = models.BooleanField(default=True)
    category = models.ManyToManyField(Category,related_name='category_product')
    order = models.ManyToManyField(Order,related_name='order_product',blank=True)
    ingredient = models.ManyToManyField(Ingredient,related_name='ingredient_product')
    favorite = models.ForeignKey(Favorite,on_delete=models.CASCADE,related_name='favorite_product',null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.name}"
    
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