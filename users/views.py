from django.http import HttpResponse
from rest_framework import status
from rest_framework.response import Response
from .serializers import UserSerializer
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from django.core.mail import send_mail
from django.contrib.auth.models import User


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

            print("Sending email to:",user.email)

            #send tokens via email
            try:
                send_mail(
                    subject="Welcome to Polls App - Registration Successfull.",
                    message= f"""
                    Hi {user.username},
                    Thanks for registering in Polls App!
                    Below are your authentication tokens. These allow you to access protected parts of the application:

                    Access Token :
                    {access_token}

                    Refresh Token :
                    {refresh}

                    Keep these tokens secure and do not share them with anyone.

                    Happy voting!
                    """,
                    from_email= "likhitha0622@gmail.com",
                    recipient_list=[user.email],
                    fail_silently=False,
                )

            except:
                return Response("Error sending email", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            # Return a success response with the tokens
            return Response({
                "message":"User created successfully.",
                "access_token":access_token,
                "refresh_token":str(refresh)
            },status=status.HTTP_201_CREATED)

        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
            