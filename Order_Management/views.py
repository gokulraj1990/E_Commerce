from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from cart_mgmt.models import Order, OrderItem
from cart_mgmt.serializers import OrderSerializer

@api_view(['PUT'])
def update_order(request, order_id):
    try:
        order = Order.objects.get(order_id=order_id)
    except Order.DoesNotExist:
        return Response({"message": "Order not found."}, status=status.HTTP_404_NOT_FOUND)

    serializer = OrderSerializer(order, data=request.data)
    if serializer.is_valid():
        serializer.save()  # Save the updated order
        return Response({
            "message": "Order updated successfully!",
            "order": serializer.data
        }, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def cancel_order(request, order_id):
    try:
        order = Order.objects.get(order_id=order_id)
        order.delete()  # Delete the order
        return Response({"message": "Order canceled successfully!"}, status=status.HTTP_204_NO_CONTENT)
    except Order.DoesNotExist:
        return Response({"message": "Order not found."}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def view_order_details(request, order_id):
    try:
        order = Order.objects.get(order_id=order_id)
        serializer = OrderSerializer(order)
        return Response(serializer.data)
    except Order.DoesNotExist:
        return Response({"message": "Order not found."}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def track_order(request, order_id):
    try:
        order = Order.objects.get(order_id=order_id)
        return Response({
            "order_id": order.order_id,
            "is_paid": order.is_paid,
            "total_amount": str(order.total_amount),
            "status": "Paid" if order.is_paid else "Pending",
            "tracking_number": order.tracking_number,  # Include tracking number
            "tracking_status": order.tracking_status,  # Include tracking status
            "created_at": order.created_at.isoformat(),
            "address": order.address,
            "city": order.city,
            "state": order.state,
            "pincode": order.pincode
        })
    except Order.DoesNotExist:
        return Response({"message": "Order not found."}, status=status.HTTP_404_NOT_FOUND)

@api_view(['PATCH'])
def update_tracking(request, order_id):
    try:
        order = Order.objects.get(order_id=order_id)
    except Order.DoesNotExist:
        return Response({"message": "Order not found."}, status=status.HTTP_404_NOT_FOUND)

    tracking_number = request.data.get("tracking_number")
    tracking_status = request.data.get("tracking_status")

    if tracking_number:
        order.tracking_number = tracking_number
    if tracking_status:
        order.tracking_status = tracking_status

    order.save()

    return Response({
        "message": "Tracking information updated successfully!",
        "order_id": order.order_id,
        "tracking_number": order.tracking_number,
        "tracking_status": order.tracking_status
    }, status=status.HTTP_200_OK)
