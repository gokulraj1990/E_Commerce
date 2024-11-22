from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.models import AnonymousUser
from .models import CustomerProfile
from .serializers import CustomerProfileSerializer
from admin_console.permissions import IsAdmin, IsCustomer
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.contrib.auth.hashers import check_password
from admin_console.models import User
from admin_console.serializers import UserRegSerializer
import csv

@api_view(['GET'])
@permission_classes([IsCustomer])
def profile_view(request):
    if isinstance(request.jwt_user, AnonymousUser):
        return Response({'detail': 'Unauthorized'}, status=401)
    try:
        profile = CustomerProfile.objects.get(user=request.jwt_user.id)
        serializer = CustomerProfileSerializer(profile)
        return Response(serializer.data)
    except CustomerProfile.DoesNotExist:
        return Response({'error': 'Profile not found.'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([IsCustomer])
def profile_create(request):
    if isinstance(request.jwt_user, AnonymousUser):
        return Response({'detail': 'Unauthorized'}, status=401)

    # Check if the user already has a profile
    if CustomerProfile.objects.filter(user=request.jwt_user).exists():
        return Response({'error': 'Profile already exists for this user.'}, status=status.HTTP_400_BAD_REQUEST)

    serializer = CustomerProfileSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.jwt_user)
        return Response({'success': 'Profile created successfully'}, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([IsCustomer])
def profile_update(request):
    profile = CustomerProfile.objects.get(user=request.jwt_user.id)
    serializer = CustomerProfileSerializer(profile, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response({'success': 'Profile updated successfully'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([IsCustomer])
def deactivate_account(request):
    try:
        profile = User.objects.get(id=request.jwt_user.id)
        print(profile)
        profile.account_status="Deactivated"
        profile.save()
        return Response({'success': 'Profile deactivated successfully'}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def change_password(request):

    try:
        user = request.jwt_user
        current_password = request.data.get('current_password')
        new_password = request.data.get('new_password')

        if not check_password(current_password, user.password):
            return Response({'detail': 'Incorrect current password'}, status=status.HTTP_400_BAD_REQUEST)

        user.password = new_password
        user.save()

        return Response({'success': 'Password changed successfully'}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(['GET'])
@permission_classes([IsAdmin])
def list_users(request):
    users = User.objects.all()
    serializer = UserRegSerializer(users, many=True)
    return Response({"Success": True, "Users": serializer.data}, status=status.HTTP_200_OK)

@api_view(['PATCH'])
@permission_classes([IsAdmin])
def update_user_status(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({"Success": False, "Message": "User not found."}, status=status.HTTP_404_NOT_FOUND)

    account_status = request.data.get('status')
    if account_status not in dict(User.STATUS_CHOICES).keys():
        return Response({"Success": False, "Message": "Invalid status."}, status=status.HTTP_400_BAD_REQUEST)

    user.account_status = account_status
    user.save()

    return Response({"Success": True, "Message": "User status updated successfully."}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAdmin])
def download_user_list_csv(request):
    # Create a HttpResponse with CSV content-type
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="user_list.csv"'

    # Create a CSV writer
    writer = csv.writer(response)
    headers = ["User ID", "First Name", "Last Name", "Email", "Mobile No", "Role", "Status"]
    writer.writerow(headers)

    # Fetch users
    users = User.objects.all()

    # Write user data to CSV
    for user in users:
        writer.writerow([
            user.id, 
            user.firstname, 
            user.lastname, 
            user.email,          
            user.mobilenumber,   
            user.role, 
            user.status
        ])

    return response





@api_view(['GET'])
@permission_classes([IsAdmin])
def admin_profiles_view(request):
    profiles = CustomerProfile.objects.all()
    serializer = CustomerProfileSerializer(profiles, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAdmin])
def download_profiles_pdf(request):
    # Create a HttpResponse with PDF content-type
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="customer_profiles.pdf"'

    # Create a PDF canvas
    p = canvas.Canvas(response, pagesize=letter)
    width, height = letter

    # Define some basic styles
    title = "Customer Profiles"
    p.setFont("Helvetica-Bold", 15)
    p.drawString(50, height - 50, title)  # Title

    # Draw the table header
    p.setFont("Helvetica-Bold", 12)
    header_y = height - 80
    p.drawString(30, header_y, "User ID")             # User ID
    p.drawString(120, header_y, "Mobile No")      # Mobile Number
    p.drawString(210, header_y, "Address")            # Address
    p.drawString(390, header_y, "City")               # City
    p.drawString(450, header_y, "State")              # State
    p.drawString(550, header_y, "Country")            # Country

    # Draw a line below the header
    p.line(20, header_y - 5, 600, header_y - 5)

    # Fetch profiles
    profiles = CustomerProfile.objects.all()
    serializer = CustomerProfileSerializer(profiles, many=True)

    # Write the data to PDF
    y_position = header_y - 20  # Start position for the first entry
    p.setFont("Helvetica", 10)

    for profile in serializer.data:
        p.drawString(30, y_position, str(profile['user_id']))        # User ID
        p.drawString(120, y_position, profile['mobile_number'])      # Mobile Number
        p.drawString(210, y_position, profile['address'])            # Address
        p.drawString(390, y_position, profile['city'])               # City
        p.drawString(450, y_position, profile['state'])              # State
        p.drawString(550, y_position, profile['country'])            # Country
        
        y_position -= 15  # Move down for the next entry
        
        # Create a new page if the current page is filled
        if y_position < 50:
            p.showPage()
            p.setFont("Helvetica-Bold", 15)
            p.drawString(50, height - 50, title)  # Title for new page
            p.setFont("Helvetica-Bold", 12)
            # Redraw the header for the new page
            header_y = height - 80
            p.drawString(30, header_y, "User ID")
            p.drawString(120, header_y, "Mobile No")
            p.drawString(210, header_y, "Address")
            p.drawString(390, header_y, "City")
            p.drawString(450, header_y, "State")
            p.drawString(550, header_y, "Country")
            p.line(50, header_y - 5, 600, header_y - 5)  # Line under header
            y_position = header_y - 20  # Reset position for new page

    # Finalize the PDF
    p.showPage()
    p.save()

    return response