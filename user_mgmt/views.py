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

    serializer = CustomerProfileSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save(user=request.jwt_user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([IsCustomer])
def profile_update(request):
    profile = CustomerProfile.objects.get(user=request.jwt_user.id)
    serializer = CustomerProfileSerializer(profile, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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