from authentication.models import User

from rest_framework.views import APIView
from rest_framework import status
from authentication.serializers.request.token import TokenSerializer, RefreshAccessTokenSerializer
from authentication.services.token import verify_token, refresh_access_token
from exceptions.base.response import base_response, base_response_with_error, base_response_with_validation_error
from exceptions.error.auth.error_exceptions import NotFound
from drf_spectacular.utils import extend_schema
from authentication.services.auth import AuthManager

class VerifyTokenView(APIView):
    serializer_class = TokenSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            token_verified = verify_token(request=request, token=serializer.validated_data["token"])

            if not token_verified:
                return base_response_with_error(status_code=status.HTTP_406_NOT_ACCEPTABLE, message="Token is not verified")
                                                

            return base_response(result=token_verified ,status_code=status.HTTP_200_OK, message='')

        return base_response_with_validation_error(error=serializer.errors)
    
class RefreshAccessToken(APIView):
    serializer_class = RefreshAccessTokenSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            try:
                access_token = refresh_access_token(request=request, refresh_token=serializer.validated_data["refresh_token"])
            except ValueError:
                return base_response_with_error(status_code=status.HTTP_406_NOT_ACCEPTABLE, message="Not accept")
                                  
            except User.DoesNotExist:
                return base_response_with_error(status_code=status.HTTP_404_NOT_FOUND, message="Not found")

            return base_response(status_code=status.HTTP_200_OK, message='',
                                 result={"access_token": access_token})
        return base_response_with_validation_error(error=serializer.errors)
    
class GetDataToken(APIView):
    @extend_schema()
    def get(self, request):
        try:
            user_data =  AuthManager().get_user_by_email(email=request.user.email)
            if not user_data:
                raise NotFound
            
        except NotFound:
            return base_response_with_error(status_code=status.HTTP_404_NOT_FOUND, message="User not found")
        return base_response(result={"id": user_data.pk, "email":user_data.email, "first_name": user_data.first_name, "last_name": user_data.last_name , "is_active": user_data. is_active}, 
                             status_code=status.HTTP_200_OK, message="")
