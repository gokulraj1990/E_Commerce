from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import CartItem, Product, Order, OrderItem, WishlistItem
from django.core.exceptions import ObjectDoesNotExist
from user_mgmt.models import CustomerProfile
from django.shortcuts import get_object_or_404
from .serializers import CartItemSerializer, OrderItemSerializer, OrderSerializer, WishListSerializer
from admin_console.utils import send_custom_email
from django.conf import settings
from django.contrib.auth.models import AnonymousUser
import qrcode
import base64
from io import BytesIO
from .payment import process_cashfree_payment


@api_view(['POST'])
def add_to_cart(request):
    user = request.jwt_user
    if isinstance(user, AnonymousUser):
        return Response({"Success": False, "Message": "User is not authenticated"}, status=status.HTTP_403_FORBIDDEN)

    try:
        product_id = request.data.get('product_id')
        quantity = int(request.data.get('quantity', 1))

        product = get_object_or_404(Product, productID=product_id)

        cart_item, created = CartItem.objects.get_or_create(user=user, product=product)
        if not created:
            cart_item.quantity += quantity
        else:
            cart_item.quantity = quantity
        cart_item.save()

        return Response({"Success": True, "Message": "Item added to cart", "Quantity": cart_item.quantity}, status=status.HTTP_201_CREATED)

    except ValueError:
        return Response({"Success": False, "Message": "Invalid quantity"}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"Success": False, "Message": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def remove_from_cart(request, cart_item_id):
    user = request.jwt_user
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
    user = request.jwt_user
    if isinstance(user, AnonymousUser):
        return Response({"Success": False, "Message": "User is not authenticated"}, status=status.HTTP_403_FORBIDDEN)

    try:
        cart_items = CartItem.objects.filter(user=user)
        serializer = CartItemSerializer(cart_items, many=True)

        return Response({"Success": True, "Cart Items": serializer.data}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"Success": False, "Message": str(e)}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
def order_history(request):
    user = request.jwt_user
    if isinstance(user, AnonymousUser):
        return Response({"Success": False, "Message": "User is not authenticated"}, status=status.HTTP_403_FORBIDDEN)

    orders = Order.objects.filter(user=user)
    order_data = []
    for order in orders:
        order_data.append({
            "id": order.order_id,
            "total_amount": order.total_amount,
            "created_at": order.created_at,
            "is_paid": order.is_paid,
            "items": [{"product": item.product.product, "quantity": item.quantity} for item in order.items.all()]
        })

    return Response({"Success": True, "Orders": order_data}, status=status.HTTP_200_OK)


@api_view(['POST'])
def checkout(request):
    user = request.jwt_user

    # Check if the user is authenticated
    if isinstance(user, AnonymousUser):
        return Response({"Success": False, "Message": "User is not authenticated"}, status=status.HTTP_403_FORBIDDEN)

    # Retrieve cart items for the user
    cart_items = CartItem.objects.filter(user=user)
    if not cart_items.exists():
        return Response({"Success": False, "Message": "Cart is empty"}, status=status.HTTP_400_BAD_REQUEST)

    # Attempt to retrieve the customer profile
    try:
        customer_profile = CustomerProfile.objects.get(user=user)
    except ObjectDoesNotExist:
        # If customer profile doesn't exist, create a new profile with address data
        address = request.data.get('address')
        city = request.data.get('city')
        state = request.data.get('state')
        pincode = request.data.get('pincode')

        if not all([address, city, state, pincode]):
            return Response({
                "Success": False,
                "Message": "Please provide address, city, state, and pincode"
            }, status=status.HTTP_400_BAD_REQUEST)

        # Create a new customer profile
        customer_profile = CustomerProfile.objects.create(
            user=user,
            address=address,
            city=city,
            state=state,
            pincode=pincode
        )
    else:
        # If the customer profile exists, check if the address has been updated
        new_address = request.data.get('address')
        new_city = request.data.get('city')
        new_state = request.data.get('state')
        new_pincode = request.data.get('pincode')

        # If any address field is provided and differs from the existing values, update the profile
        if new_address and new_address != customer_profile.address:
            customer_profile.address = new_address
        if new_city and new_city != customer_profile.city:
            customer_profile.city = new_city
        if new_state and new_state != customer_profile.state:
            customer_profile.state = new_state
        if new_pincode and new_pincode != customer_profile.pincode:
            customer_profile.pincode = new_pincode
        
        # Save the updated profile
        customer_profile.save()

    # Calculate the total amount from the cart items
    total_amount = sum(item.product.price * item.quantity for item in cart_items)

    # Create an order
    order = Order.objects.create(
        user=user,
        total_amount=total_amount,
        address=customer_profile.address,
        city=customer_profile.city,
        state=customer_profile.state,
        pincode=customer_profile.pincode
    )
    
    # Delete the cart items after order creation
    cart_items.delete()

    # Return the response with order details
    return Response({
        "Success": True,
        "Message": "Order created, proceed to payment",
        "Order ID": order.order_id,
        "Total Amount": total_amount
    }, status=status.HTTP_201_CREATED)



@api_view(['POST'])
def payment(request, order_id):
    user = request.jwt_user
    if isinstance(user, AnonymousUser):
        return Response({"Success": False, "Message": "User is not authenticated"}, status=status.HTTP_403_FORBIDDEN)

    # Retrieve the order based on order_id
    try:
        order = Order.objects.get(order_id=order_id, user=user)
    except Order.DoesNotExist:
        return Response({"Success": False, "Message": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

    payment_success = process_cashfree_payment(float(order.total_amount), user)

    if payment_success:
        order.is_paid = True
        order.save()

        # Finalize the order (reduce stock, create order items, etc.)
        finalize_order(CartItem.objects.filter(user=user), order, user)

        # Send confirmation email
        subject = 'Order Confirmation'
        message = (
            f'Thank you for your order, {user.firstname}!\n'
            f'Your order ID is: {order.order_id}\n'
            f'Total Amount: {order.total_amount}\n'
            f'Shipping Address: {order.address}, {order.city}, {order.state}, {order.pincode}\n'
        )
        recipient_list = [user.email]
        send_custom_email(subject, message, settings.EMAIL_HOST_USER, recipient_list)

        return Response({
            "Success": True,
            "Message": "Payment successful",
            "Order ID": order.order_id,
            "Order Details": OrderSerializer(order).data
        }, status=status.HTTP_200_OK)
    else:
        return Response({"Success": False, "Message": "Payment failed"}, status=status.HTTP_400_BAD_REQUEST)


def finalize_order(cart_items, order, user):
    for item in cart_items:
        if item.product.stock < item.quantity:
            raise ValueError(f"Insufficient stock for {item.product.productname}. Only {item.product.stock} available.")

        # Reduce the stock of the product
        item.product.stock -= item.quantity
        item.product.save()

        # Create the corresponding order item
        OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity)

    # Clear the user's cart
    cart_items.delete()

@api_view(['POST'])
def add_to_wishlist(request):
    user = request.jwt_user
    if isinstance(user, AnonymousUser):
        return Response({"Success": False, "Message": "User is not authenticated"}, status=status.HTTP_403_FORBIDDEN)

    try:
        product_id = request.data.get('product_id')

        # Fetch the product
        product = get_object_or_404(Product, productID=product_id)

        # Add product to wishlist
        wishlist_item, created = WishlistItem.objects.get_or_create(user=user, product=product)
        if created:
            return Response({"Success": True, "Message": "Item added to wishlist"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"Success": True, "Message": "Item already in wishlist"}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"Success": False, "Message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def remove_from_wishlist(request, product_id):
    user = request.jwt_user
    if isinstance(user, AnonymousUser):
        return Response({"Success": False, "Message": "User is not authenticated"}, status=status.HTTP_403_FORBIDDEN)

    try:
        
        # product_id_data = request.data.get('product_id')

        # # Get the wishlist item
        # print(user,product_id_data)
        wishlist_item = get_object_or_404(WishlistItem, product_id=product_id, user=user)

        # Delete the item from the wishlist
        wishlist_item.delete()

        return Response({"Success": True, "Message": "Item removed from wishlist"}, status=status.HTTP_200_OK)

    except WishlistItem.DoesNotExist:
        return Response({"Success": False, "Message": "Item not found in wishlist"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"Success": False, "Message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
def view_wishlist(request):
    user = request.jwt_user
    if isinstance(user, AnonymousUser):
        return Response({"Success": False, "Message": "User is not authenticated"}, status=status.HTTP_403_FORBIDDEN)

    try:
        # Fetch wishlist items for the authenticated user
        wishlist_items = WishlistItem.objects.filter(user=user)

        # Serialize the wishlist items
        serializer = WishListSerializer(wishlist_items, many=True)

        return Response({"Success": True, "Wishlist Items": serializer.data}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"Success": False, "Message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

#@api_view(['POST'])
# def checkout(request):
#     user = request.jwt_user
#     if isinstance(user, AnonymousUser):
#         return Response({"Success": False, "Message": "User is not authenticated"}, status=status.HTTP_403_FORBIDDEN)

#     cart_items = CartItem.objects.filter(user=user)
#     if not cart_items.exists():
#         return Response({"Success": False, "Message": "Cart is empty"}, status=status.HTTP_400_BAD_REQUEST)

#     customer_profile = CustomerProfile.objects.get(user=user)

#     address = customer_profile.address
#     city = customer_profile.city
#     state= customer_profile.state
#     pincode = customer_profile.pincode

#     total_amount = sum(item.product.price * item.quantity for item in cart_items)
#     order = Order.objects.create(
#         user=user,
#         total_amount=total_amount,
#         address=address,
#         city=city,
#         state=state,
#         pincode=pincode
#     )

#     payment_success = process_cashfree_payment(total_amount,user)

#     # payment_success = simulate_payment(total_amount)

#     if payment_success:
#         order.is_paid = True
#         order.save()

#  # Process each cart item, reduce stock and create order items
#         for item in cart_items:
#             if item.product.stock < item.quantity:
#                 return Response({
#                     "Success": False,
#                     "Message": f"Insufficient stock for {item.product.name}. Only {item.product.stock} available."
#                 }, status=status.HTTP_400_BAD_REQUEST)

#             # Reduce the stock of the product
#             item.product.stock -= item.quantity
#             item.product.save()

#             # Create the corresponding order item
#             OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity)

#         cart_items.delete()

#         subject = 'Order Confirmation'
#         message = (
#             f'Thank you for your order, {user.firstname}!\n'
#             f'Your order ID is: {order.order_id}\n'
#             f'Total Amount: {order.total_amount}\n'
#             f'Shipping Address: {order.address}, {order.city}, {order.state}, {order.pincode}\n'
#         )
#         recipient_list = [user.email]

#         # Send the email using your custom function
#         send_custom_email(subject, message,settings.EMAIL_HOST_USER, recipient_list)

#         return Response({
#             "Success": True,
#             "Message": "Order created and payment successful",
#             "Order ID": order.order_id,
#             "Order Details": OrderSerializer(order).data
#         }, status=status.HTTP_201_CREATED)
#     else:
#         return Response({"Success": False, "Message": "Payment failed"}, status=status.HTTP_400_BAD_REQUEST)


# def simulate_payment(amount):
#     return amount > 0  # Simulate successful payment for positive amounts