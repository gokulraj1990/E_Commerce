#middleware.py
from django.contrib.auth.models import AnonymousUser
from django.utils.deprecation import MiddlewareMixin
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import TokenError
from .models import User_Reg


class JWTAuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        token = request.COOKIES.get('jwt_access')
        if not token:
            request.jwt_user = AnonymousUser()
            return

        try:
            access_token = AccessToken(token)
            user_id = access_token['user_id']
            user = User_Reg.objects.get(id=user_id)
            request.jwt_user = user
        except TokenError as e:
            request.jwt_user = AnonymousUser()
        except User_Reg.DoesNotExist as e:
            request.jwt_user = AnonymousUser()
