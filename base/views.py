from rest_framework.views import APIView,Response
from .serializer import LoginSerializer


class SignupView(APIView):
    def post(self,request):
        serializer=LoginSerializer(data=request.data)
        if not serializer.is_valid():
            print(serializer.errors)
            return Response(serializer.errors)
        serializer.save()
        return Response({"message":"success"})
        


