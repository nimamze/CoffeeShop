from rest_framework.response import Response
from .serializers import (
    CustomUserSerializer,
    OtpSerializer,
    ProfileChangeSerializer,
    SelectFavoriteSerializer,
)
from rest_framework import status
from .models import CustomUser
from rest_framework.views import APIView
import random
from django.contrib.auth.hashers import make_password
from shop.models import Favorite, Order
from rest_framework.permissions import IsAuthenticated


class SignUpApi(APIView):
    def post(self, request):
        ser_data = CustomUserSerializer(data=request.data)
        otp = random.randint(1, 100)
        print(otp)
        if ser_data.is_valid():
            request.session["info"] = {
                "user_info": {
                    "phone": ser_data.validated_data["phone"],  # type: ignore
                    "email": ser_data.validated_data["email"],  # type: ignore
                    "password": ser_data.validated_data["password"],  # type: ignore
                    "first_name": ser_data.validated_data["first_name"],  # type: ignore
                    "last_name": ser_data.validated_data["last_name"],  # type: ignore
                },
                "otp_input": otp,
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
            if otp_in == otp_match:
                user_detail = request.session["info"]["user_info"]
                CustomUser.objects.create(
                    phone=user_detail["phone"],
                    email=user_detail["email"],
                    first_name=user_detail["first_name"],
                    last_name=user_detail["last_name"],
                    password=make_password(user_detail["password"]),
                )
                return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class ProfileApi(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        content = {
            "username": f"first name is {user.first_name} - last name is {user.last_name} and phon is {user.phone}",
            "favorites": Favorite.objects.filter(customer__pk=user.pk).values(),
            "order": Order.objects.filter(customer__pk=user.pk).values(),
        }
        return Response(content, status=status.HTTP_200_OK)

    def delete(self, request):
        serializer = SelectFavoriteSerializer(data=request.data)
        if serializer.is_valid():
            id = serializer.validated_data.get("id")  # type: ignore
            favorite = Favorite.objects.filter(pk=id, customer=request.user).first()
            if favorite:
                favorite.delete()
                return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        serializer = ProfileChangeSerializer(
            instance=request.user, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
