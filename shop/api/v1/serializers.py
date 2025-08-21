from ...models import Category, Product, Tag, ProductImage
from rest_framework import serializers


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name"]


class ProductSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ["id", "name", "price", "categories", "availability", "tags"]


class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "name", "price", "availability", "stock", "tags"]


class ProductDetailPostSerializer(serializers.Serializer):
    favorite = serializers.BooleanField(required=False)
    order_amount = serializers.IntegerField(required=False)

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ["id","product", "image", "is_main"]
        read_only_fields = ["id", "product"]
