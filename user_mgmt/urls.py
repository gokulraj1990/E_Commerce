from django.urls import path
from . import views

urlpatterns = [
    path('user/<int:user_id>/', views.user_details, name='user_details'),
    path('customer/<int:user_id>/', views.customer_profile, name='customer_profile'),
]
