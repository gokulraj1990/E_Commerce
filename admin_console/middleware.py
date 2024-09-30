from django.contrib.auth.models import AnonymousUser
from django.utils.deprecation import MiddlewareMixin
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import TokenError
from .models import User

class JWTAuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        token = request.COOKIES.get('jwt_access')
        if not token:
            request.jwt_user = AnonymousUser()
            return

        try:
            access_token = AccessToken(token)
            user_id = access_token['user_id']
            user = User.objects.get(id=user_id)
            request.jwt_user = user
            request.user_role = user.role
            
            # Role flags
            request.is_admin = (user.role == 'Admin')
            request.is_customer = (user.role == 'Customer')

        except (TokenError, User.DoesNotExist):
            request.jwt_user = AnonymousUser()






















# #middleware.py
# from django.contrib.auth.models import AnonymousUser
# from django.utils.deprecation import MiddlewareMixin
# from rest_framework_simplejwt.tokens import AccessToken
# from rest_framework_simplejwt.exceptions import TokenError
# from .models import User


# class JWTAuthenticationMiddleware(MiddlewareMixin):
#     def process_request(self, request):
#         token = request.COOKIES.get('jwt_access')
#         if not token:
#             request.jwt_user = AnonymousUser()
#             return

#         try:
#             access_token = AccessToken(token)
#             user_id = access_token['user_id']
#             user = User.objects.get(id=user_id)
#             request.jwt_user = user
#         except TokenError as e:
#             request.jwt_user = AnonymousUser()
#         except User.DoesNotExist as e:
#             request.jwt_user = AnonymousUser()