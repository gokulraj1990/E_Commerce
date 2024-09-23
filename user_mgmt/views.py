from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import User, Customer
from .serializers import UserSerializer,CustomerSerializer

@api_view(['GET', 'POST'])
def user_list(request):
    if request.method == 'GET':
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def user_detail(request, pk):
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        user.delete()
        return Response({"message":"successfully deleted"},status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'PUT', 'POST'])
def customer_detail(request, pk):
    print(pk)
    try:
        # Retrieve the User object based on the primary key (user_id)
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    # POST request: Create a new Customer
    if request.method == 'POST':
        # Ensure the user doesn't already have a Customer record
        if Customer.objects.filter(user=user).exists():
            return Response({"error": "Customer already exists for this user"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Deserialize the request data for creating a new Customer
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            # Assign the user to the new customer
            serializer.save(user=user)  # Save the customer with the associated user
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # GET request: Fetch customer details
    try:
        customer = Customer.objects.get(user=user)
    except Customer.DoesNotExist:
        return Response({"error": "Customer not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CustomerSerializer(customer)
        return Response(serializer.data)

    # PUT request: Update customer details
    elif request.method == 'PUT':
        serializer = CustomerSerializer(customer, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)