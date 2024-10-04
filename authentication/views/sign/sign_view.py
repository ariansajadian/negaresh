from rest_framework import views
from authentication.services.auth import AuthManager
from authentication.serializers.request.auth import ForgotPassowordSerializers, UserRegisterSerializer, LoginSerializers, GoogleLoginSerializers, VerifyEmailSerializers
from exceptions.base.response import base_response, base_response_with_error, base_response_with_validation_error
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse, OpenApiExample
from drf_spectacular.types import OpenApiTypes
from exceptions.error.auth.error_exceptions import VerifyCodeDoesNotExist, ValidationError, UserDoesExist, EmailNotExist, PasswordNotExist
from authentication.serializers.response.auth import UserTokenCombineSerializer

class RegisterUserView(views.APIView):
    serializer_class = UserRegisterSerializer
    response_serializer = UserTokenCombineSerializer

    @extend_schema(request=serializer_class)
    def post(self, request):
        serializer_class = self.serializer_class(data=request.data)
        
        if serializer_class.is_valid():
            try:
                serialized_data = serializer_class.validated_data
            
                data = serializer_class.create(serialized_data, request=request)
                response = UserTokenCombineSerializer(data)
            except UserDoesExist:
                return base_response_with_error(result=None, status_code=status.HTTP_403_FORBIDDEN, message='Email is exist')
            return base_response(result=response.data, status_code=status.HTTP_200_OK, message="Sended verify code")
        return base_response_with_validation_error(result=None, error=serializer_class.error_messages, status_code=status.HTTP_400_BAD_REQUEST)
            
class LoginUserView(views.APIView):
    serializer_class = LoginSerializers
    response_serializer = UserTokenCombineSerializer

    @extend_schema(request=serializer_class, responses=response_serializer)
    def post(self, request):
        serializer_class = self.serializer_class(data=request.data)
        
        if serializer_class.is_valid():
            try:
                serialized_data = serializer_class.validated_data
            
                data = AuthManager().login_user(request=request, **serialized_data)
                response = self.response_serializer(data)
            except EmailNotExist:
                return base_response_with_error(result=None, status_code=status.HTTP_404_NOT_FOUND, message='User not found')
            except PasswordNotExist:
                return base_response_with_error(result=None, status_code=status.HTTP_401_UNAUTHORIZED, message='Not correct password')
            if data.get('token'):
                return base_response(result=response.data, status_code=status.HTTP_200_OK, message="Ok")
            return base_response(result=response.data, status_code=status.HTTP_200_OK, message="Sended verify code")

        return base_response_with_validation_error(result=None, error=serializer_class.error_messages, status_code=status.HTTP_400_BAD_REQUEST)
            
class GoogleLoginView(views.APIView):
    serializer_class = GoogleLoginSerializers
    response_serializer = UserTokenCombineSerializer

    @extend_schema(request=serializer_class, responses=response_serializer)
    def post(self, request):
        serializer_class = self.serializer_class(data=request.data)
        
        if serializer_class.is_valid():
            try:
                serialized_data = serializer_class.validated_data
            
                data = AuthManager().login_with_google(**serialized_data)
                response = self.response_serializer(data)
            except ValidationError as obj:
                return base_response_with_error(result=None, status_code=status.HTTP_401_UNAUTHORIZED, message=obj.error)
            return base_response(result=response.data, status_code=status.HTTP_200_OK, message="Ok")
        return base_response_with_validation_error(result=None, error=serializer_class.error_messages, status_code=status.HTTP_400_BAD_REQUEST)
            
class VerifyEmailCodeView(views.APIView):
    serializer_class = VerifyEmailSerializers
    response_serializer = UserTokenCombineSerializer

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='verify_code',
                type=OpenApiTypes.STR,
                required=True  
            ),
            OpenApiParameter(
                name='user_email',
                type=OpenApiTypes.STR,
                required=True  
            )
        ],
        request=serializer_class,
        responses=response_serializer
    )
    def get(self, request):
        data = request.GET
        serializer_class = self.serializer_class(data=data)
        
        if serializer_class.is_valid():
            try:
                serialized_data = serializer_class.validated_data
            
                data = AuthManager().verify_code_email(request=request, **serialized_data)
                response = self.response_serializer(data)
            except VerifyCodeDoesNotExist as obj:
                return base_response_with_error(result=None, status_code=status.HTTP_401_UNAUTHORIZED, message=obj.error_message)
            return base_response(result=response.data, status_code=status.HTTP_200_OK, message="Ok")
        return base_response_with_validation_error(result=None, error=serializer_class.error_messages, status_code=status.HTTP_400_BAD_REQUEST)
            
class ForgotPasswordView(views.APIView):
    serializer_class = ForgotPassowordSerializers
    response_serializer = UserTokenCombineSerializer

    @extend_schema(request=serializer_class)
    def post(self, request):
        serializer_class = self.serializer_class(data=request.data)
        
        if serializer_class.is_valid():
            try:
                serialized_data = serializer_class.validated_data
            
                data = AuthManager().forgot_password(request=request, **serialized_data)
            except EmailNotExist:
                return base_response_with_error(result=None, status_code=status.HTTP_404_NOT_FOUND, message='User not found')
            except PasswordNotExist:
                return base_response_with_error(result=None, status_code=status.HTTP_401_UNAUTHORIZED, message='Not correct password')
            return base_response(result=None, status_code=status.HTTP_200_OK, message="Sended verification code")
        return base_response_with_validation_error(result=None, error=serializer_class.error_messages, status_code=status.HTTP_400_BAD_REQUEST)
            