from django.contrib import admin
from .models import (
    Product,
    Category,
    ProductImage,
    Ingredient,
    Favorite,
    Order,
    OrderItem,
    Cart,
    CartItem,
    Notification,
    Comment
)

admin.site.register(Cart)
admin.site.register(CartItem)

class ProductCategoryFilter(admin.SimpleListFilter):
    title = 'دسته‌بندی محصولات'
    parameter_name = 'category'

    def lookups(self, request, model_admin):
        return [(cat.id, cat.name) for cat in Category.objects.all()] # type: ignore

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(cart__items__product__categories__id=self.value()).distinct()
        return queryset

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_filter = ['categories', 'date_added']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_filter = ['created_at', ProductCategoryFilter]

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'created_at', 'is_read')
    list_filter = ('is_read',)
    actions = ['mark_as_read']

    @admin.action(description='علامت‌گذاری به‌عنوان خوانده‌شده')
    def mark_as_read(self, request, queryset):
        updated = queryset.update(is_read=True)
        self.message_user(request, f"{updated} نوتیفیکیشن به‌عنوان خوانده‌شده علامت‌گذاری شد.")



admin.site.register(Category)
admin.site.register(ProductImage)
admin.site.register(Ingredient)
admin.site.register(Favorite)
admin.site.register(OrderItem)
admin.site.register(Comment)