#views.py
import csv
import io
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import ProductSerializer
from .models import Product
from django.db.models import Q

# Create your views here.

@api_view(['POST'])
def addProduct(request):
    try:
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"Success":True, "Message":"Product added successfully"}, status= status.HTTP_201_CREATED)
    except Exception as e:
        return Response({"Success":False, "Message":"Not added", "Errors":str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['PATCH'])
def updateProduct(request, product_id):
    try:
        product = Product.objects.get(productID=product_id)
        serializer = ProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"Success": True, "Message": "Product updated successfully"}, status=status.HTTP_200_OK)
    except Product.DoesNotExist:
        return Response({"Success": False, "Message": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"Success": False, "Message": "Not updated", "Errors": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def deleteProduct(request, product_id):
    try:
        product = Product.objects.get(productID=product_id)
        product.delete()
        return Response({"Success": True, "Message": "Product deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    except Product.DoesNotExist:
        return Response({"Success": False, "Message": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"Success": False, "Message": "Not deleted", "Errors": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def getProducts(request):
    try:
        query = request.data.get('name', '').strip()  # Get the search term from JSON
        if query:
            products = Product.objects.filter(
                Q(name__icontains=query) |
                Q(description__icontains=query) |
                Q(category__icontains=query)
            )
        else:
            products = Product.objects.all()  # Return all products if no query

        serializer = ProductSerializer(products, many=True)
        return Response({"Success": True, "Products": serializer.data}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"Success": False, "Message": "Could not retrieve products", "Errors": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def importProducts(request):
    if 'file' not in request.FILES:
        return Response({"Success": False, "Message": "No file provided."}, status=status.HTTP_400_BAD_REQUEST)

    csv_file = request.FILES['file']

    if not csv_file.name.endswith('.csv'):
        return Response({"Success": False, "Message": "This is not a CSV file."}, status=status.HTTP_400_BAD_REQUEST)

    data_set = csv_file.read().decode('UTF-8')
    io_string = io.StringIO(data_set)
    next(io_string)  # Skip header if present

    for row in csv.reader(io_string, delimiter=','):
        product_data = {
            'name': row[0],
            'description': row[1],
            'price': row[2],
            'stock': row[3],
            'category': row[4],
            'imageUrl': row[5],
        }
        serializer = ProductSerializer(data=product_data)
        if serializer.is_valid(raise_exception=False):
            serializer.save()

    return Response({"Success": True, "Message": "Products imported successfully"}, status=status.HTTP_201_CREATED)