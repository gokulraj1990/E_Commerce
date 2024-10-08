from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Order
from .serializers import OrderSerializer

@api_view(['POST'])
def createOrder(request):
    serializer = OrderSerializer(data=request.data)
    if serializer.is_valid():
        order = serializer.save()  # Save the order
        return Response({
            "message": "Order created successfully!",
            "order": serializer.data
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def updateOrder(request, orderID):
    try:
        order = Order.objects.get(orderID=orderID)
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
def cancelOrder(request, orderID):
    try:
        order = Order.objects.get(orderID=orderID)
        order.delete()  # Delete the order
        return Response({"message": "Order canceled successfully!"}, status=status.HTTP_204_NO_CONTENT)
    except Order.DoesNotExist:
        return Response({"message": "Order not found."}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def viewOrderDetails(request, orderID):
    try:
        order = Order.objects.get(orderID=orderID)
        serializer = OrderSerializer(order)
        return Response(serializer.data)
    except Order.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def trackOrder(request, orderID):
    try:
        order = Order.objects.get(orderID=orderID)
        return Response({"orderID": order.orderID, "status": order.status})
    except Order.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
