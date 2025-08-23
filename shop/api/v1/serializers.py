from ...models import Category, Product, Tag, ProductImage, Comment, Order, OrderItem
from rest_framework import serializers


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name"]


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ["id", "product", "image", "is_main"]
        read_only_fields = ["id", "product"]


class ProductSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    main_image = serializers.SerializerMethodField()
    images = ProductImageSerializer(
        many=True, source="product_images", read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "price",
            "categories",
            "availability",
            "description",
            "tags",
            "main_image",
            "images"
        ]

    def get_main_image(self, obj):
        return obj.get_main_image()


class ProductDetailSerializer(serializers.ModelSerializer):
    ingredients = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="name"
    )

    class Meta:
        model = Product
        fields = ["id", "name", "price", "availability",
                  "ingredients", "stock", "tags"]


class ProductDetailPostSerializer(serializers.Serializer):
    SCORE_CHOICES = [(i, str(i)) for i in range(1, 6)]

    favorite = serializers.BooleanField(required=False)
    order_amount = serializers.IntegerField(required=False)
    comment = serializers.CharField(required=False)
    score = serializers.ChoiceField(choices=SCORE_CHOICES, required=False)


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"


class OrderDetailSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ["id", "order", "product", "quantity", "price_at_purchase"]
