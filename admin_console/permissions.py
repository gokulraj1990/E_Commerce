from rest_framework import permissions
from .models import User

class IsAdmin(permissions.BasePermission):
    """
    Custom permission to only allow admin users to access a view.
    """
    def has_permission(self, request, view):
        print(request.jwt_user.role)
        # Check if the user is authenticated and has an admin role
        return isinstance(request.jwt_user, User) and request.is_admin

class IsCustomer(permissions.BasePermission):
    """
    Custom permission to only allow customer users to access a view.
    """
    def has_permission(self, request, view):
        # Check if the user is authenticated and has a customer role
        return isinstance(request.jwt_user, User) and request.is_customer
