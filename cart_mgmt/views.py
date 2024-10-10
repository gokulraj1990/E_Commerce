from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import CartItem, Product
from django.shortcuts import get_object_or_404
from .serializers import CartItemSerializer
from django.contrib.auth.models import AnonymousUser

@api_view(['POST'])
def add_to_cart(request):
    user = request.jwt_user  # Use the user from the middleware
    if isinstance(user, AnonymousUser):
        return Response({"Success": False, "Message": "User is not authenticated"}, status=status.HTTP_403_FORBIDDEN)

    try:
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity', 1)

        product = get_object_or_404(Product, productID=product_id)

        cart_item, created = CartItem.objects.get_or_create(user=user, product=product)
        if not created:
            cart_item.quantity += quantity
        cart_item.save()

        return Response({"Success": True, "Message": "Item added to cart"}, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response({"Success": False, "Message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def remove_from_cart(request, cart_item_id):
    user = request.jwt_user  # Use the user from the middleware
    if isinstance(user, AnonymousUser):
        return Response({"Success": False, "Message": "User is not authenticated"}, status=status.HTTP_403_FORBIDDEN)

    try:
        cart_item = get_object_or_404(CartItem, id=cart_item_id, user=user)
        cart_item.delete()

        return Response({"Success": True, "Message": "Item removed from cart"}, status=status.HTTP_204_NO_CONTENT)

    except Exception as e:
        return Response({"Success": False, "Message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def view_cart(request):
    user = request.jwt_user  # Use the user from the middleware
    if isinstance(user, AnonymousUser):
        return Response({"Success": False, "Message": "User is not authenticated"}, status=status.HTTP_403_FORBIDDEN)

    try:
        cart_items = CartItem.objects.filter(user=user)
        serializer = CartItemSerializer(cart_items, many=True)

        return Response({"Success": True, "Cart Items": serializer.data}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"Success": False, "Message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
