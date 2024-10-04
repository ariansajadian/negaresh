from rest_framework import serializers
from authentication.services.auth import AuthManager, User

class UserRegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=128)
    first_name = serializers.CharField(max_length=30, required=False)
    last_name = serializers.CharField(max_length=30, required=False)

    def __init__(self, *args, **kwargs):
        self.state =  kwargs.pop('field', None)
        super().__init__(*args, **kwargs)

    def create(self, validated_data, request):
        return AuthManager().create_base_user(request=request ,**validated_data)
    
    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.content)
        instance.last_name = validated_data.get('last_name', instance.created)
        instance.save()
        return instance
    
    def to_representation(self, instance):
        res = super().to_representation(instance)
        if self.state in res:
            res.pop('password', None)
        return res

class LoginSerializers(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=128)

class GoogleLoginSerializers(UserRegisterSerializer):
    password = None

class VerifyEmailSerializers(serializers.Serializer):
    verify_code = serializers.CharField(max_length=72)
    user_email = serializers.CharField(max_length=255)

class ForgotPassowordSerializers(serializers.Serializer):
    email = serializers.EmailField()

