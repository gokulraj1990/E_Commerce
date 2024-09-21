from django.urls import path
from .views import addProduct,updateProduct,deleteProduct,rateProduct,getProducts,searchProducts

urlpatterns = [
path('product/add/',addProduct, name='addProduct'),
path('product/update/', updateProduct, name='updateProduct'),
path('product/delete/', deleteProduct, name='deleteProduct'),
path('product/rate/', rateProduct, name='rateProduct'),
path('product/get/', getProducts, name='getProducts'),
path('product/search/', searchProducts, name='searchProducts'),
]