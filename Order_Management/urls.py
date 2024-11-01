from django.urls import path
from .views import cancel_order,track_order,update_order,view_order_details,update_tracking

urlpatterns = [
    path('update/<int:orderID>/', update_order, name='update-order'),
    path('cancel/<int:orderID>/', cancel_order, name='cancel-order'),
    path('view/<int:orderID>/', view_order_details, name='view-order-details'),
    path('track/<int:orderID>/', track_order, name='track-order'),
    path('<str:order_id>/update-tracking/', update_tracking, name='update_tracking'),
]
