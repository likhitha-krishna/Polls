from django.http import HttpResponse
from rest_framework import status
from rest_framework.response import Response
from .serializers import UserSerializer
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView

class UserRegistrationView(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserSerializer

    def post(self,request):
        serializer = UserSerializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.save()

            # Generate JWT tokens for the new user
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            return Response({
                "message":"User created successfully.",
                "access_token":access_token,
                "refresh_token":str(refresh)
            },status=status.HTTP_201_CREATED)

        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)