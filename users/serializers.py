from rest_framework import serializers
from django.contrib.auth.models import User
from django.core.validators import RegexValidator


# Define the validator
username_validator = RegexValidator(
    regex="^[a-zA-Z _]+$",
    message="Username can only contain letters,spaces and underscore."
)

class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(validators=[username_validator])
    class Meta :
        model = User
        fields = ["username","email","password"]

        def validate_username(self,value):
            if User.objects.filter(username=value).exists():
                return serializers.ValidationError("Username already exists.")
            return value
            
        def validate_email(self,value):
            if User.objects.filter(email=value).exists():
                return serializers.ValidationError("email already exists.")
            return value
        
        # def validate_password(self,value):
        #     if len(value)<8:
        #         return serializers.ValidationError("Password must be at least 8 characters.")
        #     if value.isdigit():
        #         return serializers.ValidationError("Password cannot be fully numeric")
        #     return value

        def create(self,validated_data):
            # Automatically hashes password
            user = User.objects.create_user(
                username=validated_data['username'],
                email=validated_data['email'],
                password=validated_data['password']
            )
            return user
            
        
            