from django.urls import path
from .views import cancel_order,track_order,update_order,view_order_details

urlpatterns = [
    path('orders/update/<int:orderID>/', update_order, name='update-order'),
    path('orders/cancel/<int:orderID>/', cancel_order, name='cancel-order'),
    path('orders/view/<int:orderID>/', view_order_details, name='view-order-details'),
    path('orders/track/<int:orderID>/', track_order, name='track-order'),
]
