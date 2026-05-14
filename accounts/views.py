from django.contrib.auth import authenticate

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema

from .serializers import (
    LoginSerializer,
    MessageSerializer,
    RegisterSerializer,
)


class RegisterView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        request=RegisterSerializer,
        responses={201: RegisterSerializer},
        tags=["accounts"],
    )
    def post(self, request):

        serializer = RegisterSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(serializer.data, status=201)


class LoginView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        request=LoginSerializer,
        responses={200: MessageSerializer},
        tags=["accounts"],
    )
    def post(self, request):

        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(
            username=username,
            password=password
        )

        if user is None:
            return Response(
                {"detail": "Invalid credentials"},
                status=401
            )

        refresh = RefreshToken.for_user(user)

        access_token = str(refresh.access_token)

        response = Response({
            "message": "login success"
        })

        response.set_cookie(
            key="access",
            value=access_token,
            httponly=True,
            samesite="None",
            secure=True,
            max_age=60 * 30,
        )

        response.set_cookie(
            key="refresh",
            value=str(refresh),
            httponly=True,
            samesite="None",
            secure=True,
            max_age=60 * 60 * 24 * 7,
        )

        return response


class LogoutView(APIView):

    @extend_schema(
        request=None,
        responses={200: MessageSerializer},
        tags=["accounts"],
    )
    def post(self, request):

        response = Response({
            "message": "logout success"
        })

        response.delete_cookie("access")
        response.delete_cookie("refresh")

        return response
    

