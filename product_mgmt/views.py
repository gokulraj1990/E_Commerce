#views.py
import csv
import io
from django.contrib.auth.models import AnonymousUser
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from .serializers import ProductSerializer,ReviewSerializer
from .models import Product,Review
from django.db.models import Q
from admin_console.permissions import IsAdmin, IsCustomer
from django.http import HttpResponse,request
from django.db.models import Avg
# Create your views here.



@api_view(['POST'])
@permission_classes([IsAdmin])
def addProduct(request):
    try:
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"Success":True, "Message":"Product added successfully"}, status= status.HTTP_201_CREATED)
    except Exception as e:
        return Response({"Success":False, "Message":"Not added", "Errors":str(e)}, status=status.HTTP_400_BAD_REQUEST)


  
@api_view(['PATCH'])
@permission_classes([IsAdmin])  
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
@permission_classes([IsAdmin])
def deleteProduct(request, product_id):
    try:
        product = Product.objects.get(productID=product_id)
        product.delete()
        return Response({"Success": True, "Message": "Product deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    except Product.DoesNotExist:
        return Response({"Success": False, "Message": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"Success": False, "Message": "Not deleted", "Errors": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAdmin])
def deleteMultipleProducts(request):
    product_ids = request.data.get('product_ids', [])
    if not product_ids:
        return Response({"Success": False, "Message": "No product IDs provided"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        products = Product.objects.filter(productID__in=product_ids)
        deleted_count, _ = products.delete()
        return Response({"Success": True, "Message": f"{deleted_count} products deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        return Response({"Success": False, "Message": "Not deleted", "Errors": str(e)}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
def getProducts(request):
    try:
        query = request.query_params.get('q', '').strip()
        category = request.query_params.get('category', '').strip()
        price_min = request.query_params.get('price_min', None)
        price_max = request.query_params.get('price_max', None)
        stock_min = request.query_params.get('stock_min', None)
        stock_max = request.query_params.get('stock_max', None)

        filters = Q()

        if query:
            filters &= (Q(product__icontains=query) |
                        Q(model__icontains=query) |
                        Q(description__icontains=query))

        if category:
            filters &= Q(category=category)

        # Handle price filtering
        if price_min is not None:
            price_min = float(price_min)  # Convert to float
            filters &= Q(price__gte=price_min)  # Ensure products have price >= price_min
            
        if price_max is not None:
            price_max = float(price_max)  # Convert to float
            filters &= Q(price__lte=price_max)  # Ensure products have price <= price_max

        # Handle stock filtering
        if stock_min is not None:
            stock_min = int(stock_min)  # Convert to int
            filters &= Q(stock__gte=stock_min)  # Ensure stock >= stock_min
            
        if stock_max is not None:
            stock_max = int(stock_max)  # Convert to int
            filters &= Q(stock__lte=stock_max)  # Ensure stock <= stock_max



        # Query the database based on the filters
        products = Product.objects.filter(filters) if filters else Product.objects.all()



        serializer = ProductSerializer(products, many=True)
        return Response({"Success": True, "Products": serializer.data}, status=status.HTTP_200_OK)

    except ValueError as e:
        return Response({"Success": False, "Message": "Invalid input", "Errors": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"Success": False, "Message": "Could not retrieve products", "Errors": str(e)}, status=status.HTTP_400_BAD_REQUEST)





@api_view(['GET'])
def getProductsByCategory(request, category):
    try:
        products = Product.objects.filter(category__icontains=category)
        serializer = ProductSerializer(products, many=True)
        return Response({"Success": True, "Products": serializer.data}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"Success": False, "Message": "Could not retrieve products", "Errors": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_all_products(request):
    try:
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response({'Success': True, 'Products': serializer.data})
    except Exception as e:
        print(f"Error: {e}")
        return Response({'Success': False, 'Message': str(e)}, status=500)

@api_view(['POST'])
@permission_classes([IsAdmin])
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
            'category': row[0],
            'productname': row[1],
            'model': row[2],
            'price': row[3],
            'description': row[4],
            'stock': row[5],
            'imageUrl': row[6]
        }
        serializer = ProductSerializer(data=product_data)
        if serializer.is_valid(raise_exception=False):
            serializer.save()

    return Response({"Success": True, "Message": "Products imported successfully"}, status=status.HTTP_201_CREATED)



@api_view(['GET'])
@permission_classes([IsAdmin])
def download_product_list_csv(request):
    # Create a HttpResponse with CSV content-type
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="product_list.csv"'

    # Create a CSV writer
    writer = csv.writer(response)
    headers = ["productid","productname","model","description","price","stock","category","imageUrl"]
    writer.writerow(headers)

    # Fetch users
    products = Product.objects.all()

    # Write user data to CSV
    for product in products:
        writer.writerow([
            product.productID,
            product.productname,
            product.model,
            product.description,
            product.price,
            product.stock,
            product.category,
            product.imageUrl

        ])

    return response


@api_view(['POST'])
@permission_classes([IsCustomer])
def add_review(request):
    user = request.jwt_user
    if isinstance(user, AnonymousUser):
        return Response({"Success": False, "Message": "User is not authenticated"}, status=status.HTTP_403_FORBIDDEN)

    serializer = ReviewSerializer(data=request.data)
    if serializer.is_valid():
        review = serializer.save(rated_by=user)
        return Response({"Success": True, "Message": "Review added", "Review ID": review.id}, status=status.HTTP_201_CREATED)
    else:
        return Response({"Success": False, "Message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
def list_all_products_with_reviews(request):
    try:
        products = Product.objects.all()
        products_data = []

        for product in products:
            reviews = Review.objects.filter(product_id=product.productID)
            average_rating = reviews.aggregate(Avg('rating'))['rating__avg']
            serialized_reviews = ReviewSerializer(reviews, many=True).data

            products_data.append({
                "Product": ProductSerializer(product).data,
                "Reviews": serialized_reviews,
                "Average Rating": average_rating
            })

        return Response({"Success": True, "Products": products_data}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"Success": False, "Message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def list_reviews_for_product(request, product_id):
    try:
        reviews = Review.objects.filter(product_id=product_id)
        average_rating = reviews.aggregate(Avg('rating'))['rating__avg']
        
        serialized_reviews = ReviewSerializer(reviews, many=True).data

        return Response({
            "Success": True,
            "Reviews": serialized_reviews,
            "Average Rating": average_rating
        }, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"Success": False, "Message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)





@api_view(['POST'])
@permission_classes([IsCustomer])
def add_review(request):
    serializer = ReviewSerializer(data=request.data)
    if serializer.is_valid():
        review = serializer.save(rated_by=request.jwt_user)  # Associate the review with the user
        return Response({"Success": True, "Message": "Review added", "Review ID": review.id}, status=status.HTTP_201_CREATED)
    return Response({"Success": False, "Message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([IsCustomer])
def update_review(request, review_id):
    try:
        review = Review.objects.get(id=review_id, rated_by=request.user)
    except Review.DoesNotExist:
        return Response({"Success": False, "Message": "Review not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = ReviewSerializer(review, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"Success": True, "Message": "Review updated", "Review ID": review.id}, status=status.HTTP_200_OK)
    return Response({"Success": False, "Message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsCustomer])
def delete_review(request, review_id):
    try:
        review = Review.objects.get(id=review_id, rated_by=request.user)
        review.delete()
        return Response({"Success": True, "Message": "Review deleted"}, status=status.HTTP_204_NO_CONTENT)
    except Review.DoesNotExist:
        return Response({"Success": False, "Message": "Review not found"}, status=status.HTTP_404_NOT_FOUND)
