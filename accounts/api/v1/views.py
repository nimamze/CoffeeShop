from rest_framework.response import Response
from .serializers import (
    CustomUserSerializer,
    OtpSerializer,
    ProfileChangeSerializer,
    SelectFavoriteSerializer,
)
from rest_framework import status
from ...models import CustomUser
from rest_framework.views import APIView
import random
from django.contrib.auth.hashers import make_password
from shop.models import Favorite, Order, CartItem
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import os
from django.core.mail import send_mail


class SignUpApi(APIView):
    def post(self, request):
        ser_data = CustomUserSerializer(data=request.data)
        otp = random.randint(1, 100)
        send_mail(
            "OTP",
            f"{otp}",
            "nimamze3@gmail.com",
            [request.POST.get("email")],
            fail_silently=False,
        )
        print(otp)
        if ser_data.is_valid():
            user_info = ser_data.validated_data.copy()  # type: ignore
            uploaded_file = user_info.pop("image", None)
            temp_path = None
            if uploaded_file:
                temp_path = default_storage.save(
                    f"temp/{uploaded_file.name}", ContentFile(uploaded_file.read())
                )
            user_info["password"] = make_password(user_info.get("password"))
            request.session["info"] = {
                "user_info": user_info,
                "otp_input": otp,
                "temp_image_path": temp_path,
            }
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        ser_data = CustomUserSerializer()
        return Response(ser_data.data)


class SignUpConfirmApi(APIView):
    queryset = CustomUser.objects.all()

    def post(self, request):
        otp_serializer = OtpSerializer(data=request.data)
        if otp_serializer.is_valid():
            otp_in = otp_serializer.validated_data.get("otp")  # type: ignore
            otp_match = request.session["info"]["otp_input"]
            temp_image_path = request.session.get("info").get("temp_image_path")
            image_file = None
            if temp_image_path and default_storage.exists(temp_image_path):
                with default_storage.open(temp_image_path, "rb") as f:
                    image_file = ContentFile(
                        f.read(), name=os.path.basename(temp_image_path)
                    )
            if otp_in == otp_match:
                user_detail = request.session["info"]["user_info"]
                CustomUser.objects.create(
                    phone=user_detail["phone"],
                    email=user_detail["email"],
                    first_name=user_detail["first_name"],
                    last_name=user_detail["last_name"],
                    password=(user_detail["password"]),
                    image=image_file,
                )
                if temp_image_path:
                    default_storage.delete(temp_image_path)
                request.session.pop("info", None)
                return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class ProfileApi(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(security=[{"Bearer": []}])
    def get(self, request):
        user = request.user
        content = {
            "username": f"first name is {user.first_name} - last name is {user.last_name} and phon is {user.phone}",
            "favorites": Favorite.objects.filter(customer__pk=user.pk).values(),
            "order": Order.objects.filter(customer__pk=user.pk).values(),
            "cart_items": CartItem.objects.filter(cart__customer__pk=user.pk).values(),
        }
        return Response(content, status=status.HTTP_200_OK)

    @swagger_auto_schema(security=[{"Bearer": []}])
    def delete(self, request):
        serializer = SelectFavoriteSerializer(data=request.data)
        if serializer.is_valid():
            id = serializer.validated_data.get("id")  # type: ignore
            favorite = Favorite.objects.filter(pk=id, customer=request.user).first()
            if favorite:
                favorite.delete()
                return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(security=[{"Bearer": []}])
    def patch(self, request):
        serializer = ProfileChangeSerializer(
            instance=request.user, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
