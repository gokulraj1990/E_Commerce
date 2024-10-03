


#Logic to receive confirmation email

    # is_active = models.BooleanField(default=False)
    # verification_token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

# @api_view(['POST'])
# def create_user(request):
#     try:
#         valid = cust_validation(request.data)
#         request.data['role'] = User.CUSTOMER  
#         serializer = UserRegSerializer(data=request.data)
#         if serializer.is_valid(raise_exception=True):
#             user = serializer.save()
#             # Send verification email
#             send_verification_email(user)
#             return Response({"Success": True, "Message": "User created successfully. Please check your email to verify your account."}, status=status.HTTP_201_CREATED)
#     except Exception as e:
#         return Response({"Success": False, "Message": "Not created", "Errors": str(e)}, status=status.HTTP_400_BAD_REQUEST)

# def send_verification_email(user):
#     verification_link = f"{settings.FRONTEND_URL}/verify-email/{user.verification_token}/"
#     send_custom_email(
#         'Verify your email address',
#         f'Please click the link to verify your email: {verification_link}',
#         settings.EMAIL_HOST_USER,
#         [user.email],
#         fail_silently=False,
#     )


# @api_view(['GET'])
# def verify_email(request, token):
#     try:
#         user = User.objects.get(verification_token=token)
#         user.is_active = True
#         user.verification_token = None  # Optionally reset the token
#         user.save()
#         return Response({'detail': 'Email verified successfully. You can now log in.'}, status=status.HTTP_200_OK)
#     except User.DoesNotExist:
#         return Response({'detail': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)



# @api_view(['POST'])
# def login_view(request):
#     try:
#         email = request.data.get('email')
#         password = request.data.get('password')
        
#         user = User.objects.filter(email=email).first()
        
#         if user is None:
#             raise AuthenticationFailed("User Not Found")

#         if not user.is_active:
#             raise AuthenticationFailed("Please verify your email address before logging in.")

#         if not check_password(password, user.password):
#             raise AuthenticationFailed("Incorrect Password")
        
#         refresh = RefreshToken.for_user(user)
#         access_token = str(refresh.access_token)
#         refresh_token = str(refresh)

#         response = Response()
#         response.set_cookie(key='jwt_access', value=access_token, httponly=True)
#         response.set_cookie(key='jwt_refresh', value=refresh_token, httponly=True)

#         response.data = {
#             "Message": "Successfully Logged in",
#             "role": user.role,
#             "user_id": str(user.id),
#             "access_token": access_token,
#             "refresh_token": refresh_token
#         }

#         return response

#     except Exception as e:
#         return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
