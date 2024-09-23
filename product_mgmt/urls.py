from django.urls import path
from .views import addProduct, updateProduct, deleteProduct, getProducts, importProducts

urlpatterns = [
    path('add/', addProduct, name='addProduct'),
    path('update/<str:product_id>/', updateProduct, name='updateProduct'), 
    path('delete/<str:product_id>/', deleteProduct, name='deleteProduct'),  
    path('get/', getProducts, name='getProducts'),
    path('import-products/', importProducts, name='import_products'),
]
