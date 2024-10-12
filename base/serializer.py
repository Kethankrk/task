from rest_framework import serializers
from django.contrib.auth.models import User

class LoginSerializer(serializers.ModelSerializer):
    # cpassword=serializers.CharField()
    class Meta:
        model=User
        fields=["username","email","password"]
    

