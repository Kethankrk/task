from rest_framework.views import APIView, Response, Request
from .serializer import (
    SignupSerializer,
    LoginSerializer,
    PasswordResetSerializer,
    UserDetailsSerializer,
)
from django.contrib.auth import authenticate, login, logout
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User


class SignupView(APIView):
    permission_classes = []
    authentication_classes = []

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if not serializer.is_valid():
            print(serializer.errors)
            return Response(serializer.errors, status=400)
        user = serializer.save()
        user = authenticate(
            username=user.username, password=request.data.get("password")
        )
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({"token": str(refresh.access_token)})
        return Response({"message": "success"})


class LoginView(APIView):
    permission_classes = []
    authentication_classes = []

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            print(serializer.errors)
            return Response(serializer.errors, status=400)
        username = serializer.validated_data["username"]
        password = serializer.validated_data["password"]
        user = authenticate(username=username, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({"token": str(refresh.access_token)})
        return Response({"message": "failed"}, status=400)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTTokenUserAuthentication]

    def get(self, request: Request):
        user = request.user
        if user is not None:
            logout(request)

        return Response({"message": "Logout successfull"})


class PasswrodResetView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTTokenUserAuthentication]

    def post(self, request: Request):
        serializer = PasswordResetSerializer(data=request.data)
        if not serializer.is_valid():
            print(serializer.errors)
            return Response(serializer.errors, status=400)

        current_pass = serializer.validated_data["current_password"]
        password = serializer.validated_data["password"]
        cpassword = serializer.validated_data["cpassword"]
        user: User = request.user
        user = User.objects.filter(pk=user.pk).first()
        user = authenticate(username=user.get_username(), password=current_pass)

        if user is None:
            print("Incorrect password")
            return Response({"message": "Incorrect current password"}, status=400)

        if password != cpassword:
            print("pass and cpass not valid")
            return Response(
                {"message": "password and confirm password mismatch"}, status=400
            )

        user.set_password(password)
        user.save()
        logout(request)
        return Response({"message": "success"})


class HomeView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTTokenUserAuthentication]

    def get(self, request):
        users = User.objects.all()
        return Response(UserDetailsSerializer(users, many=True).data)
