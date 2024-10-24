from django.contrib.auth.models import AnonymousUser
from django.utils.deprecation import MiddlewareMixin
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import TokenError
from .models import User, Admin  # Import both models

class JWTAuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        token = request.COOKIES.get('jwt_access')
        if not token:
            request.jwt_user = AnonymousUser()
            request.is_admin = False
            request.is_customer = False
            return

        try:
            # Decode the access token
            access_token = AccessToken(token)
            user_id = access_token['user_id']
            
            # Attempt to get the user from the User model first
            try:
                user = User.objects.get(id=user_id)
                request.jwt_user = user
                request.is_admin = False
                request.is_customer = (user.role == 'Customer')
            except User.DoesNotExist:
                # If not found, check the Admin model
                try:
                    admin = Admin.objects.get(id=user_id)
                    request.jwt_user = admin
                    request.is_admin = True
                    request.is_customer = False
                except Admin.DoesNotExist:
                    # If neither found, set as anonymous
                    request.jwt_user = AnonymousUser()
                    request.is_admin = False
                    request.is_customer = False

        except TokenError:
            request.jwt_user = AnonymousUser()
            request.is_admin = False
            request.is_customer = False









































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
#             request.user_role = user.role
#             # Role flags
#             request.is_admin = (user.role == 'Admin')
#             request.is_customer = (user.role == 'Customer')

#         except (TokenError, User.DoesNotExist):
#             request.jwt_user = AnonymousUser()






















# from rest_framework_simplejwt.tokens import AccessToken, RefreshToken, TokenError
# from django.utils.deprecation import MiddlewareMixin
# from django.contrib.auth.models import AnonymousUser
# from django.http import JsonResponse
# from django.contrib.auth import get_user_model

# User = get_user_model()

# class JWTAuthenticationMiddleware(MiddlewareMixin):
#     def process_request(self, request):
#         # Get the access and refresh tokens from cookies (assuming you store them in cookies)
#         access_token = request.COOKIES.get('jwt_access')
#         refresh_token = request.COOKIES.get('jwt_refresh')

#         if not access_token:
#             request.jwt_user = AnonymousUser()
#             return
        
#         try:
#             # Try to decode the access token
#             token = AccessToken(access_token)
#             user_id = token['user_id']
#             user = User.objects.get(id=user_id)
#             request.jwt_user = user
#             request.user_role = user.role
            
#             # Set role flags for easy access later
#             request.is_admin = (user.role == 'Admin')
#             request.is_customer = (user.role == 'Customer')

#         except TokenError:
#             # Access token has expired or is invalid
#             if refresh_token:
#                 try:
#                     # Try refreshing the access token using the refresh token
#                     new_access_token = self._refresh_access_token(refresh_token)
                    
#                     # Set the new access token in the request
#                     request.COOKIES['jwt_access'] = new_access_token
                    
#                     # Decode the new access token and get the user
#                     token = AccessToken(new_access_token)
#                     user_id = token['user_id']
#                     user = User.objects.get(id=user_id)
#                     request.jwt_user = user
#                     request.user_role = user.role

#                     # Set role flags again after refreshing the token
#                     request.is_admin = (user.role == 'Admin')
#                     request.is_customer = (user.role == 'Customer')

#                 except TokenError:
#                     # If refresh token is also invalid or expired, consider user as anonymous
#                     request.jwt_user = AnonymousUser()

#             else:
#                 # No refresh token available, so the user is considered anonymous
#                 request.jwt_user = AnonymousUser()
        
#         except User.DoesNotExist:
#             request.jwt_user = AnonymousUser()

#     def _refresh_access_token(self, refresh_token):
#         """
#         Helper method to refresh the access token using the refresh token.
#         """
#         try:
#             refresh = RefreshToken(refresh_token)
#             new_access_token = refresh.access_token
#             return str(new_access_token)

#         except TokenError as e:
#             raise TokenError('Refresh token is invalid or expired.')