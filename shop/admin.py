from django.contrib import admin

# Register your models here.
from .models import Product
from .models import Category
from .models import ProductImage
from .models import Ingredient

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(ProductImage)
admin.site.register(Ingredient)