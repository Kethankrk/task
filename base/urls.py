from django.urls import path,include
from .views import SignupView

urlpatterns = [
    path("login/",SignupView.as_view())
   
    
]
