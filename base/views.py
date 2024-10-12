from rest_framework.views import APIView, Response, Request
from .serializer import SignupSerializer, LoginSerializer, PasswordResetSerializer
from django.contrib.auth import authenticate, login, logout
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication


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
            login(request, user)
            print("cookie set")
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
            login(request, user)
            print("cookie set")
            return Response({"message": "success"})
        return Response({"message": "failed"})


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication]

    def get(self, request: Request):
        user = request.user
        if user is not None:
            logout(request)

        return Response({"message": "Logout successfull"})


class PasswrodResetView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication]

    def get(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        current_pass = serializer.validated_data["current_password"]
        password = serializer.validated_data["password"]
        cpassword = serializer.validated_data["cpassword"]

        user = authenticate(username=request.user.username, password=current_pass)

        if user is None:
            return Response({"message": "Incorrect current password"}, status=400)

        if password != cpassword:
            return Response(
                {"message": "password and confirm password mismatch"}, status=400
            )

        user.set_password(password)
        user.save()
        logout(request)
        return Response({"message": "success"})


class HomeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message": "Sercure message"})
