from django.contrib import admin

# Register your models here.
from .models import Product
from .models import Category
from .models import ProductImage
from .models import Ingredient
from .models import Favorite
from .models import Order
from .models import OrderItem

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(ProductImage)
admin.site.register(Ingredient)
admin.site.register(Favorite)
admin.site.register(Order)
admin.site.register(OrderItem)