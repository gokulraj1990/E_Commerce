#urls.py

from django.urls import path
from .views import create_user,login_view,protected_view_admin,protected_view_customer ,logout_view,token_refresh


urlpatterns = [
path('create/', create_user, name='create_user'),
path('login/', login_view, name='login_view'),
path('customerview/', protected_view_customer, name='protected_view'),
path('adminview/', protected_view_admin, name='protected_view'),
path('logout/', logout_view, name='logout_view'),
path('token/refresh/', token_refresh, name='token_refresh')

]


