#views.py

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import render
from .serializers import ProductSerializer
from .models import Product

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

@api_view(['PATCH'])
def rateProduct(request, product_id):
    try:
        product = Product.objects.get(productID=product_id)
        new_rating = request.data.get('rating')
        if new_rating is not None:
            product.rate_product(new_rating)
            return Response({"Success": True, "Message": "Product rated successfully"}, status=status.HTTP_200_OK)
        else:
            return Response({"Success": False, "Message": "Rating not provided"}, status=status.HTTP_400_BAD_REQUEST)
    except Product.DoesNotExist:
        return Response({"Success": False, "Message": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"Success": False, "Message": "Not rated", "Errors": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def getProducts(request):
    try:
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response({"Success": True, "Products": serializer.data}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"Success": False, "Message": "Could not retrieve products", "Errors": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def searchProducts(request):
    query = request.GET.get('query', '')
    try:
        products = Product.search_products(query)
        serializer = ProductSerializer(products, many=True)
        return Response({"Success": True, "Products": serializer.data}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"Success": False, "Message": "Search failed", "Errors": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
