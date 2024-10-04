from typing import Dict

from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework.status import HTTP_400_BAD_REQUEST

def base_response(*, status_code: int, success: bool = True, result: Dict | None = None, message: str) -> Response:
    return Response(data={"data": result, "message": message, "isSuccess": success, "statusCode": 200}, status=status_code)

def base_response_with_error(
        *, status_code: int, message, success: bool = False,
        error: str | None = None, result: Dict | None = None) -> Response:
    
    return Response(data={"data": result, "message":message,  "isSuccess": success, "statusCode": 200}, status=status_code)

def base_response_with_validation_error(    
        *, error: ValidationError, status_code: int,
        success: bool = False, result: Dict | None = None) -> Response:
    return Response(data={"data": result, "message": error, "isSuccess": success, "statusCode": 200}, status=status_code)
