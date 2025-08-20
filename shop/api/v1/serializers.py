from ...models import Category, Product
from rest_framework import serializers


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]


class ProductSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ["id", "name", "price", "categories", "availability"]


class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "name", "price", "availability", "stock"]


class ProductDetailPostSerializer(serializers.Serializer):
    favorite = serializers.BooleanField(required=False)
    order_amount = serializers.IntegerField(required=False)
