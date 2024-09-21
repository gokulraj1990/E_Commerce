from django.urls import path
from .views import createOrder, updateOrder, cancelOrder, viewOrderDetails, trackOrder

urlpatterns = [
    path('orders/create/', createOrder, name='create-order'),
    path('orders/update/<int:orderID>/', updateOrder, name='update-order'),
    path('orders/cancel/<int:orderID>/', cancelOrder, name='cancel-order'),
    path('orders/view/<int:orderID>/', viewOrderDetails, name='view-order-details'),
    path('orders/track/<int:orderID>/', trackOrder, name='track-order'),
]
