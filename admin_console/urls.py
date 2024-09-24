#urls.py

from django.urls import path
from .views import create_user,login_view,protected_view,logout_view,token_refresh


urlpatterns = [
path('create/', create_user, name='create_user'),
path('login/', login_view, name='login_view'),
path('view/', protected_view, name='protected_view'),
path('logout/', logout_view, name='logout_view'),
path('token/refresh/', token_refresh, name='token_refresh')

]


