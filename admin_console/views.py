#views.py
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import AuthenticationFailed
from .models import User
from .serializers import UserRegSerializer
from .validation import cust_validation
from django.contrib.auth.hashers import check_password
from rest_framework.decorators import api_view
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.decorators import api_view, permission_classes
from .permissions import IsAdmin, IsCustomer




@api_view(['GET'])
@permission_classes([IsCustomer])
def protected_view_customer(request):
    if isinstance(request.jwt_user, AnonymousUser):
        return Response({'detail': 'Unauthorized'}, status=401)

    try:
        # Retrieve the user instance from the database
        user_instance = User.objects.get(id=request.jwt_user.id)
        
        full_name = f"{user_instance.firstname} "
        
        return Response({
            'message': f"Welcome, {full_name}!",
        })
    
    except User.DoesNotExist:
        return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    

@api_view(['GET'])
@permission_classes([IsAdmin])
def protected_view_admin(request):
    if isinstance(request.jwt_user, AnonymousUser):
        return Response({'detail': 'Unauthorized'}, status=401)

    try:
        # Retrieve the user instance from the database
        user_instance = User.objects.get(id=request.jwt_user.id)
        
        full_name = f"{user_instance.firstname}"

        
        return Response({
            'message': f"Welcome, {full_name}!",
        })
    
    except User.DoesNotExist:
        return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def token_refresh(request):
    # Get the refresh token from the request's cookies
    token = request.COOKIES.get('jwt_refresh')
    
    if not token:
        return Response({'detail': 'Refresh token not provided'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Refresh the access token
        refresh_token = RefreshToken(token)
        new_access_token = str(refresh_token.access_token)
        new_refresh_token = str(refresh_token)  # Ensure a new refresh token is generated
        
        response = Response()
        
        # Set the cookies for the new tokens
        response.set_cookie(key='jwt_access', value=new_access_token, httponly=True, secure=False)  # Set secure=True if using HTTPS
        response.set_cookie(key='jwt_refresh', value=new_refresh_token, httponly=True, secure=False)  # Set secure=True if using HTTPS
        
        response_data = {
            'access_token': new_access_token,
            'refresh_token': new_refresh_token
        }
        
        response.data = response_data
        
        return response
    
    except TokenError:
        return Response({'detail': 'Invalid refresh token'}, status=status.HTTP_400_BAD_REQUEST)
        

@api_view(['POST'])
def login_view(request):
    try:
        email = request.data.get('email')
        password = request.data.get('password')
        
        # Retrieve user by email
        user = User.objects.filter(email=email).first()
        
        if user is None:
            raise AuthenticationFailed("User Not Found")
        
        # Check password
        if not check_password(password, user.password):
            raise AuthenticationFailed("Incorrect Password")
        
        # Create JWT token
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        # Create response with token and set cookies
        response = Response()
        response.set_cookie(key='jwt_access', value=access_token, httponly=True)
        response.set_cookie(key='jwt_refresh', value=refresh_token, httponly=True)

        # Include role and user_id in the response
        response.data = {
            "Message": "Successfully Logged in",
            "role": user.role,  # Add user role to the response
            "user_id": str(user.id),  # Add user ID to the response
            "access_token": access_token,  # Optionally include access token
            "refresh_token": refresh_token  # Optionally include refresh token
        }

        return response

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def logout_view(request):
    response=Response()
    response.delete_cookie('jwt_refresh')
    response.delete_cookie('jwt_access')
    response.data={"Message":"Successfully Logged out"}
    return response

@api_view(['POST'])
def create_user(request):
    try:
        # Validate and serialize user data
        valid = cust_validation(request.data)
        # Ensure the role is set to CUSTOMER by default
        request.data['role'] = User.CUSTOMER  
        # Validate and serialize user data
        serializer = UserRegSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"Success": True, "Message": "User created successfully"}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({"Success": False, "Message": "Not created", "Errors": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    