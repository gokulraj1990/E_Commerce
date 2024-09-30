from django.urls import path
from .views import addProduct, updateProduct, deleteProduct, getProducts, importProducts,deleteMultipleProducts,getProductsByCategory,get_all_products

urlpatterns = [

    path('add/', addProduct, name='add_product'),
    path('update/<int:product_id>/', updateProduct, name='update_product'),
    path('delete/<int:product_id>/', deleteProduct, name='delete_product'),
    path('delete-multiple/', deleteMultipleProducts, name='delete_multiple_products'),
    path('get/', getProducts, name='get_products'),
    path('get/all/', get_all_products, name='get_all_products'),
    path('get/category/<str:category>/', getProductsByCategory, name='get_products_by_category'),
    path('import/', importProducts, name='import_products'),

]
