from django.urls import path
from .views import add_to_cart, remove_from_cart, view_cart

urlpatterns = [
    path('add/', add_to_cart, name='add_to_cart'),
    path('remove/<int:cart_item_id>/', remove_from_cart, name='remove_from_cart'),
    path('view/', view_cart, name='view_cart'),
]
