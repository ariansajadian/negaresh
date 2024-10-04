from authentication.models import User
from exceptions.error.auth.error_exceptions import ValidationError, UserDoesExist, PasswordNotExist, EmailNotExist, VerifyCodeDoesNotExist
from authentication.utils.oauth2.auth import GoogleAuthUtils
from django.conf import settings
from authentication.services.token import generate_token
import uuid
from rest_framework import mixins
from django.utils.crypto import get_random_string
from django.http import HttpRequest
from typing import Dict
from authentication.pkg.email.base import EmailBase
from django.core.mail import send_mail

class AuthManager:
    def __init__(self, user= User) -> None:
        self.user = user
    
    def create_base_user(self, request, email, password, first_name=None, last_name=None):
        user_obj = self.get_user_by_email(email=email)
        if user_obj:
            raise UserDoesExist 
        created_user = self.user.objects.create_user(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        verify_code = get_random_string(length=72)
        self.code_email_verification(request=request, email=email, verify_code=verify_code, state='forgot', user=created_user)
        send_mail(
            subject='',
            message=verify_code,
            recipient_list=[created_user.email],
            from_email=settings.EMAIL_HOST_USER
        )
        return {
            'user_info':created_user
        }

    def get_user_by_email(self, email):
        user_obj = self.user.objects.filter(email=email).first()
        return user_obj
    
    def login_user(self, request, email, password):
        user_obj = self.email_password_validation(
            email=email, 
            password=password
        )
        
        token = generate_token(user=user_obj)

        if not user_obj.is_active:
        
            verify_code = get_random_string(length=72)
            
            self.code_email_verification(request=request, email=email, verify_code=verify_code, state='signin', user=user_obj)
            send_mail(
                subject='',
                message=verify_code,
                recipient_list=[user_obj.email],
                from_email=settings.EMAIL_HOST_USER
            )
            return {
                'user_info': user_obj
            }
        
        return {
            'user_info': user_obj, 
            'token': token
        }
    
    @staticmethod
    def code_email_verification(request: HttpRequest, verify_code: str, email: str,  state: str, user: User) -> None:
        session_info = request.session.get(email)

        if session_info:
            del request.session[email]

        data = request.session[email] = {
            'user_info': user.email, 
            'verify_code': verify_code,
            'state': state
        }

    def login_with_google(self, email, first_name=None, last_name=None):
        random_password = self.random_password(len_pass=8)

        user_obj = self.get_user_by_email(email=email)

        if user_obj:
            token = generate_token(user=user_obj)
            return {
                'user_info': user_obj, 
                'token': token
            }
        
        created_user = self.create_base_user(
            email=email, 
            password=random_password, 
            first_name=first_name, 
            last_name=last_name
        )   
        user_obj = self.user_activator(user=created_user.get('user_info'))

        token = generate_token(user=user_obj)
        return {
            'user_info': user_obj, 
            'token': token
        }
    
    def verify_code_email(self, request: HttpRequest, verify_code: str, user_email: str):
        session_info = request.session.get(user_email)
        if not session_info:
            raise VerifyCodeDoesNotExist(error_message='Invali data')
        
        if session_info.get('verify_code') != verify_code:
            raise VerifyCodeDoesNotExist(error_message='Verify code does not exist')
        
        if session_info.get('state') == 'forgot':
            random_pass = self.random_password(len_pass=8)
            user_obj = self.update_password(email=session_info.get('user_info'), new_password=random_pass)
            activated_user = self.user_activator(user=user_obj)
            del session_info
            send_mail(
                subject='',
                message=random_pass,
                recipient_list=[user_obj.email],
                from_email=settings.EMAIL_HOST_USER
            )
            return {
                'user_info': user_obj, 
                'token': generate_token(user=user_obj)
            }
        
        else:
            user_obj = self.get_user_by_email(email=session_info.get('user_info'))
            activated_user = self.user_activator(user=user_obj)
            del session_info
            return {
                'user_info': activated_user, 
                'token': generate_token(user=activated_user)
            }
    
    def forgot_password(self, request, email):
        user_obj = self.get_user_by_email(email=email)
        if not user_obj:
            raise EmailNotExist
        verify_code = get_random_string(length=72)
        self.code_email_verification(request=request, email=email, verify_code=verify_code, state='forgot', user=user_obj)
        send_mail(
            subject='',
            message=verify_code,
            recipient_list=[user_obj.email],
            from_email=settings.EMAIL_HOST_USER
        )
        
    @staticmethod
    def user_activator(user: User):
        if not user.is_active:
            user.is_active = True
            user.save()
            return user

    @staticmethod
    def random_password(len_pass):
        password = str(uuid.uuid4())[:len_pass]
        return password
    
    def update_password(self, email: str, new_password: str):
        user = self.get_user_by_email(email=email)
        if not user:
            pass
        user.set_password(new_password)
        user.save()
        return user
    
    def email_password_validation(self, email, password):
        user_obj = self.get_user_by_email(email=email)
        if not user_obj:
            raise EmailNotExist
        if not user_obj.check_password(password):
            raise PasswordNotExist
        
        return user_obj
        
    
    
    
    
        
