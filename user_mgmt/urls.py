from django.urls import path
from .views import user_detail,customer_detail,user_list

urlpatterns = [
    path('users/', user_list, name='user-list'), # List all users or add a new user (POST)
    path('users/<int:pk>/', user_detail, name='user-detail'),# Get, update, or delete a specific user
    path('customers/<int:pk>/', customer_detail, name='customer-detail'),# Get or update customer details
]
