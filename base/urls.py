from django.urls import path, include
from .views import SignupView, LoginView, HomeView, LogoutView, PasswrodResetView

urlpatterns = [
    path("signup/", SignupView.as_view()),
    path("login/", LoginView.as_view()),
    path("logout/", LogoutView.as_view()),
    path("reset/", PasswrodResetView.as_view()),
    path("users/", HomeView.as_view()),
]
