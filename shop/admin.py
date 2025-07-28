from django.contrib import admin
from accounts.models import CustomUser
from shop.models import Product,Order,Cart,Category,Favorite,Comment,Ingredient,ProductImage

admin.site.register(CustomUser)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Cart)
admin.site.register(Category)
admin.site.register(Favorite)
admin.site.register(Comment)
admin.site.register(Ingredient)
admin.site.register(ProductImage)