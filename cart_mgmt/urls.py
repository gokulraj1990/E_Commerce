from django.urls import path
from .views import add_to_cart, remove_from_cart, view_cart, checkout, process_payment, order_history

urlpatterns = [
    path('add/', add_to_cart, name='add_to_cart'),  # URL to add an item to the cart
    path('remove/<int:cart_item_id>/', remove_from_cart, name='remove_from_cart'),  # URL to remove an item from the cart
    path('view/', view_cart, name='view_cart'),  # URL to view all items in the cart
    path('checkout/', checkout, name='checkout'),  # URL to initiate checkout
    path('payment/<int:order_id>/', process_payment, name='process_payment'),  # URL to process payment for an order
    path('order-history/', order_history, name='order_history'),  # URL to view the user's order history
]
  