from django.shortcuts import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.db.models import Q
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import permission_classes
from shop.models import (
    Category,
    Product,
    Favorite,
    Cart,
    CartItem,
    ProductImage,
    Order,
    OrderItem,
    Comment,
)
from .serializers import (
    CategorySerializer,
    ProductSerializer,
    ProductDetailSerializer,
    ProductDetailPostSerializer,
    ProductImageSerializer,
    CommentSerializer,
)
from django.shortcuts import get_object_or_404


class ProductListApi(APIView):
    def get(self, request, name=None):
        categories = Category.objects.all()
        category_data = CategorySerializer(categories, many=True).data

        products = Product.objects.all()
        q = Q()

        if name:
            q |= Q(categories__name__icontains=name)

        tags = request.query_params.getlist("tags")
        if tags:
            for tag in tags:
                q |= Q(tags__name__icontains=tag)

        search_terms = request.query_params.getlist("search")
        if search_terms:
            for term in search_terms:
                q |= Q(name__icontains=term) | Q(description__icontains=term)

        if q:
            products = products.filter(q).distinct()

        paginator = PageNumberPagination()
        paginator.page_size = int(request.query_params.get("page_size", 5))
        result_page = paginator.paginate_queryset(products, request)

        product_data = ProductSerializer(result_page, many=True).data
        return paginator.get_paginated_response(
            {
                "categories": category_data,
                "products": product_data,
            }
        )


class ProductDetailApi(APIView):
    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        comments = Comment.objects.filter(product=product, is_confirmed=True)

        product_serializer = ProductDetailSerializer(product)
        data1 = product_serializer.data
        comment_serializer = CommentSerializer(comments, many=True)
        data2 = comment_serializer.data

        combined_data = {"product_detail": data1, "comments": data2}
        return Response(combined_data, status=status.HTTP_200_OK)

    @swagger_auto_schema(security=[{"Bearer": []}])
    @permission_classes([IsAuthenticated])
    def post(self, request, pk):
        serializer = ProductDetailPostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        fav = data.get("favorite")  # type: ignore
        order_amount = data.get("order_amount")  # type: ignore
        comment = data.get("comment")  # type: ignore
        score = data.get("score")  # type: ignore
        user = request.user
        product = get_object_or_404(Product, pk=pk)

        if fav:
            Favorite.objects.get_or_create(customer=user, product=product)
            return Response(
                    {"message": "product added to favorite successfully"},
                    status=status.HTTP_200_OK,
                )

        if comment and score:
            has_purchased = Order.objects.filter(
                customer=user,
                order_items__product=product.id,  # type: ignore
            ).exists()

            Comment.objects.create(
                text=comment,
                score=score,
                product=product,
                customer=user,
                has_purchased=has_purchased,
            )
            return Response(
                    {"message": "comment added successfully"},
                    status=status.HTTP_200_OK,
                )

        if order_amount and order_amount > 0:
            if product.availability:
                if product.stock < order_amount:
                    return Response(
                        {"message": "Cannot order more than product stock"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                product.stock -= order_amount
                if product.stock == 0:
                    product.availability = False
                cart, created = Cart.objects.get_or_create(
                    customer=user, is_active=True
                )
                CartItem.objects.create(
                    cart=cart, product=product, quantity=order_amount
                )

                product.save()
                return Response(
                    {"message": "product added to cart successfully?"},
                    status=status.HTTP_200_OK,
                )
            return Response(
                {"message": "sorry this product has been finished"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(
            {"message": "please enter a positive order amount!"},
            status=status.HTTP_400_BAD_REQUEST,
        )


class ProductImageEditApi(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        images = ProductImage.objects.filter(product=product)
        serializer = ProductImageSerializer(images, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        serializer = ProductImageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(product=product)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, pk):
        image_id = request.data.get("image_id")
        if not image_id:
            return Response(
                {"error": "Image id is required"}, status=status.HTTP_400_BAD_REQUEST
            )
        image = get_object_or_404(ProductImage, pk=image_id, product_id=pk)
        image.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProductOrder(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            user_cart = Cart.objects.get(customer=request.user, is_active=True)
        except Cart.DoesNotExist:
            return Response(
                {"message": "Your active cart could not be found or is empty."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if not user_cart.cart_items.exists():  # type: ignore
            return Response(
                {"message": "your cart is empty"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            if user_cart.cart_order.status == "pending":  # type: ignore
                return Response(
                    {
                        "message": "admin has not verified your previous order state yet and it's on pending"
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except:
            pass
        order = Order.objects.create(
            customer=request.user,
            cart=user_cart,
            total_price=user_cart.get_total_price(),
        )
        user_cart.cart_order = order  # type: ignore
        user_cart.save()

        for item in user_cart.cart_items.all():  # type: ignore
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price_at_purchase=item.product.price,
            )
        user_cart.cart_items.all().delete()  # type: ignore
        user_cart.is_active = False
        user_cart.save()
        return Response(
            {"message": "your have ordered!"}, status=status.HTTP_201_CREATED
        )

    # item = get_object_or_404(CartItem, pk=pk, cart__customer=request.user)
    # item_name = item.product.name
    # item.product.stock = item.product.stock + item.quantity
    # item.product.save()
    # item.delete()
    # return Response(
    #     {"message": f"{item_name} has been deleted from your cart"},
    #     status=status.HTTP_200_OK,
    # )
