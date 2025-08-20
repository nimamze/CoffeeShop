from django.shortcuts import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from shop.models import Category, Product
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import CategorySerializer, ProductSerializer, ProductDetailSerializer
from .filters import ProductFilter
from ...models import Product, Favorite
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import permission_classes


class ProductListApi(APIView):
    def get(self, request, name=None):
        categories = Category.objects.all()
        category_data = CategorySerializer(categories, many=True).data
        if name:
            category = get_object_or_404(Category, name=name)
            products = Product.objects.filter(categories=category)
        else:
            products = Product.objects.all()
        filtered_products = ProductFilter(request.GET, queryset=products).qs
        paginator = PageNumberPagination()
        paginator.page_size = 4
        result_page = paginator.paginate_queryset(filtered_products, request)
        product_data = ProductSerializer(result_page, many=True).data
        return paginator.get_paginated_response(
            {
                "categories": category_data,
                "products": product_data,
            }
        )


class ProductDetailApi(APIView):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        serializer = ProductDetailSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(security=[{"Bearer": []}])
    @permission_classes([IsAuthenticated])
    def post(self, request, pk):
        user = request.user
        product = Product.objects.get(pk=pk)
        Favorite.objects.create(customer=user, product=product)
        return Response(status=status.HTTP_200_OK)
