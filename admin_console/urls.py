#urls.py

from django.urls import path
from .views import create_user,login_view,protected_view_customer ,logout_view,token_refresh,forgot_password,reset_password,verify_account,otp_login_view,otp_verify_view,reactivate_account,resend_verification,reactivate_verification
from .views import admin_login_view,create_admin,protected_view_admin

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
path('resend-verification/', resend_verification, name='resend_verification'),
path('reactivate-verification/', reactivate_verification, name='reactivate_verification'),
path('activate-account/', reactivate_account, name='reactivate_account'),
path('otp-login/', otp_login_view, name='otp-login'),
path('otp-verify/', otp_verify_view, name='otp-verify'),
path('admin-login/', admin_login_view, name='admin-login'),
path('create-admin/', create_admin, name='create-admin'),

]


