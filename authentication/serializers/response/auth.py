from rest_framework import serializers
from authentication.serializers.request.auth import UserRegisterSerializer
from authentication.serializers.request.token import RefreshAccessTokenSerializer

class UserTokenCombineSerializer(serializers.Serializer):
    user_info = UserRegisterSerializer(read_only=True, field='password')
    token = RefreshAccessTokenSerializer(read_only=True)

