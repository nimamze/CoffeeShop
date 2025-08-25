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
    Comment,
)


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("id", "customer", "created_at")
    list_filter = ("created_at",)
    search_fields = ("customer__username",)


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ("id", "cart", "product", "quantity")
    list_filter = ("product",)
    search_fields = ("product__name", "cart__customer__username")


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "price", "date_added")
    search_fields = ("name",)
    list_filter = ("categories", "date_added")
    filter_horizontal = (
        "categories",
        "ingredients",
    )


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ("id", "product", "image")
    search_fields = ("product__name",)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ["id", "customer", "product"]
    search_fields = ("user__username", "product__name")


class ProductCategoryFilter(admin.SimpleListFilter):
    title = "دسته‌بندی محصولات"
    parameter_name = "category"

    def lookups(self, request, model_admin):
        return [(cat.id, cat.name) for cat in Category.objects.all()]  # type: ignore

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(
                order_items__product_name__in=Product.objects.filter(
                    categories__id=self.value()
                ).values_list("name", flat=True)
            ).distinct()
        return queryset


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "customer", "created_at", "total_price", "status")
    list_filter = ("created_at", ProductCategoryFilter)
    search_fields = ("customer__username",)


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("id", "order", "product", "quantity", "price_at_purchase")
    search_fields = ("product", "order__customer__username")


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "product", "customer", "score", "is_confirmed", "created_at")
    list_filter = ("is_confirmed", "score", "created_at")
    search_fields = ("product__name", "customer__username")
    actions = ["confirm_comments"]

    @admin.action(description="تایید نظرات انتخاب‌شده")
    def confirm_comments(self, request, queryset):
        updated = queryset.update(is_confirmed=True)
        self.message_user(request, f"{updated} نظر تایید شد.")


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("user", "message", "created_at", "is_read")
    list_filter = ("is_read", "created_at")
    actions = ["mark_as_read"]

    @admin.action(description="علامت‌گذاری به‌عنوان خوانده‌شده")
    def mark_as_read(self, request, queryset):
        updated = queryset.update(is_read=True)
        self.message_user(
            request, f"{updated} نوتیفیکیشن به‌عنوان خوانده‌شده علامت‌گذاری شد."
        )
