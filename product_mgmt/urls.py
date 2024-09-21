from django.urls import path
from .views import addProduct,updateProduct,deleteProduct,rateProduct,getProducts,searchProducts

urlpatterns = [
path('add/',addProduct, name='addProduct'),
path('update/', updateProduct, name='updateProduct'),
path('delete/', deleteProduct, name='deleteProduct'),
path('rate/', rateProduct, name='rateProduct'),
path('get/', getProducts, name='getProducts'),
path('search/', searchProducts, name='searchProducts'),
]
