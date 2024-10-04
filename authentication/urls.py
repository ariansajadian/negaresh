from django.urls import path
from authentication.views.sign import sign_view
from authentication.views.token import token_view

token_urlpatterns = [
    path("token/verify/", token_view.VerifyTokenView.as_view()),
    path("token/refresh/", token_view.RefreshAccessToken.as_view()),
    path("user/data/", token_view.GetDataToken.as_view())
]

urlpatterns = [
    path('register/', sign_view.RegisterUserView.as_view()),
    path('login/', sign_view.LoginUserView.as_view()),
    path('login/google/', sign_view.GoogleLoginView.as_view()),
    path('verify/', sign_view.VerifyEmailCodeView.as_view()),
    path('forgot_password/', sign_view.ForgotPasswordView.as_view()),
]+token_urlpatterns

