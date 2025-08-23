from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
import random
from django.contrib.auth.hashers import make_password
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import os
from django.core.mail import send_mail
from .serializers import (
    CustomUserSerializer,
    OtpSerializer,
    ProfileChangeSerializer,
    SelectFavoriteSerializer,
)
from ...models import CustomUser
from shop.models import Favorite, Order, CartItem


class SignUpApi(APIView):
    def post(self, request):
        ser_data = CustomUserSerializer(data=request.data)
        otp = random.randint(1, 100)
        email = request.data.get("email")
        if email:
            send_mail(
                "Your OTP Verify Is:",
                f"{otp}",
                "nimamze3@gmail.com",
                [email],
                fail_silently=False,
            )
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
            return Response(
                {"success": True, "message": "OTP sent to your email."},
                status=status.HTTP_200_OK,
            )
        return Response(
            {"success": False, "message": "Invalid data.", "errors": ser_data.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )

    def get(self, request):
        ser_data = CustomUserSerializer()
        return Response(
            {"success": True, "data": ser_data.data}, status=status.HTTP_200_OK
        )


class SignUpConfirmApi(APIView):
    queryset = CustomUser.objects.all()

    def post(self, request):
        otp_serializer = OtpSerializer(data=request.data)
        if otp_serializer.is_valid():
            otp_in = otp_serializer.validated_data.get("otp")  # type: ignore
            otp_match = request.session.get("info", {}).get("otp_input")
            temp_image_path = request.session.get("info", {}).get("temp_image_path")
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
                    password=user_detail["password"],
                    image=image_file,
                )
                if temp_image_path:
                    default_storage.delete(temp_image_path)
                request.session.pop("info", None)
                return Response(
                    {"success": True, "message": "Account created successfully."},
                    status=status.HTTP_201_CREATED,
                )
            else:
                return Response(
                    {"success": False, "message": "OTP is incorrect."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        return Response(
            {
                "success": False,
                "message": "Invalid OTP data.",
                "errors": otp_serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )


class ProfileApi(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(security=[{"Bearer": []}])
    def get(self, request):
        user = request.user
        content = {
            "username": f"{user.first_name} {user.last_name}",
            "phone": user.phone,
            "favorites": list(
                Favorite.objects.filter(customer=user).values("id", "product_id")
            ),
            "cart_items": list(
                CartItem.objects.filter(cart__customer=user).values(
                    "id", "product_id", "quantity"
                )
            ),
        }
        return Response({"success": True, "data": content}, status=status.HTTP_200_OK)

    @swagger_auto_schema(security=[{"Bearer": []}])
    def delete(self, request):
        serializer = SelectFavoriteSerializer(data=request.data)
        if serializer.is_valid():
            id = serializer.validated_data.get("id")  # type: ignore
            favorite = Favorite.objects.filter(pk=id, customer=request.user).first()
            if favorite:
                favorite.delete()
                return Response(
                    {"success": True, "message": "Favorite removed successfully."},
                    status=status.HTTP_200_OK,
                )
            return Response(
                {"success": False, "message": "Favorite not found."},
                status=status.HTTP_404_NOT_FOUND,
            )
        return Response(
            {"success": False, "message": "Invalid data.", "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )

    @swagger_auto_schema(security=[{"Bearer": []}])
    def patch(self, request):
        serializer = ProfileChangeSerializer(
            instance=request.user, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "success": True,
                    "message": "Profile updated successfully.",
                    "data": serializer.data,
                },
                status=status.HTTP_200_OK,
            )
        return Response(
            {"success": False, "message": "Invalid data.", "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )
