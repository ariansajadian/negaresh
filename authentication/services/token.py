from typing import Dict

from django.conf import settings
from django.http import HttpRequest

from rest_framework_simplejwt.tokens import Token

from authentication.pkg.encryption import encrypt, decrypt
from authentication.pkg.Token.token import (generate_access_token_with_claims, get_token_claims,
                             generate_refresh_token_with_claims, validate_token)

from authentication.models import User

USER_ID = "id"
USERNAME = "email"
IS_ACTIVE = "is_active"
IS_ADMIN = "is_admin"

refresh_token_claims = {
    USER_ID: 0,
}

access_token_claims = {
    USER_ID: 0,
    USERNAME: "",
    IS_ACTIVE: False,
    IS_ADMIN: False,
}

user_to_map = {
    USER_ID: 0,
    USERNAME: "",
    IS_ACTIVE: "",
    IS_ADMIN: "",
}

def get_refresh_token_claims(**kwargs) -> Dict:
    claims = refresh_token_claims
    for key in claims:
        claims[key] = kwargs[key]
    
    return claims

def get_access_token_claims(**kwargs) -> Dict:
    claims = access_token_claims
    for key in claims:
        claims[key] = kwargs[key]

    return claims

def encrypt_token(token: Token) -> str:
    return encrypt(data=str(token), key=settings.ENCRYPT_KEY)

def decrypt_token(token: str) -> str:
    return decrypt(encrypted=token.encode(), key=settings.ENCRYPT_KEY)

def verify_token(*, request: HttpRequest, token: str) -> bool:
    try:
        token_string = decrypt_token(token=token)
        
        token = validate_token(string_token=token_string)
    except ValueError:
        return False

    return True

def validate_refresh_token(token: Token):
    if token["token_type"] != "refresh":
        raise ValueError("Invalid refresh token")

def refresh_access_token(request: HttpRequest, refresh_token: str) -> str:
    refresh_token_str = decrypt_token(token=refresh_token)

    token = validate_token(string_token=refresh_token_str)

    user = User.objects.get(id=token[USER_ID])

    claims = get_access_token_claims(**user.__dict__)

    return generate_access_token_with_claims(claims=claims, encrypt_func=encrypt_token)

def get_user_by_access_token(token: Token) -> User:
    claims = user_to_map
    get_token_claims(token=token, claims=claims)

    return User(
        **user_to_map
    )

def generate_token(user: User) -> Dict: 
    refresh_token = generate_refresh_token_with_claims(
        claims=get_refresh_token_claims(id=user.id), encrypt_func=encrypt_token)

    access_token = generate_access_token_with_claims(
        claims=get_access_token_claims(**user.__dict__),
        encrypt_func=encrypt_token)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
    }