#urls.py

from django.urls import path
from .views import create_user,login_view,protected_view_admin,protected_view_customer ,logout_view,token_refresh,forgot_password,reset_password,verify_account,otp_login_view,otp_verify_view


urlpatterns = [
path('create/', create_user, name='create_user'),
path('login/', login_view, name='login_view'),
path('customerview/', protected_view_customer, name='customer_protected_view'),
path('adminview/', protected_view_admin, name='admin_protected_view'),
path('logout/', logout_view, name='logout_view'),
path('token/refresh/', token_refresh, name='token_refresh'),
path('forgotpassword/', forgot_password, name='forgot_password'),
path('reset-password/', reset_password, name='reset_password'),
path('verify-account/', verify_account, name='verify_account'),
path('otp-login/', otp_login_view, name='otp-login'),
path('otp-verify/', otp_verify_view, name='otp-verify'),
]


