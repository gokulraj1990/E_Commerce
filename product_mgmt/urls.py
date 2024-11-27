from django.urls import path
from .views import getProducts, importProducts,getProductsByCategory,get_all_products
from .views import addProduct,updateProduct,deleteProduct,deleteMultipleProducts,importProducts,download_product_list_csv
from .views import add_review,delete_review,update_review,list_all_products_with_reviews,list_reviews_for_product


urlpatterns = [

    path('add/', addProduct, name='add_product'),
    path('update/<str:product_id>/', updateProduct, name='update_product'),
    path('delete/<str:product_id>/', deleteProduct, name='delete_product'),
    path('delete-multiple/', deleteMultipleProducts, name='delete_multiple_products'),
    path('get/', getProducts, name='get_products'),
    path('get/all/', get_all_products, name='get_all_products'),
    path('get/category/<str:category>/', getProductsByCategory, name='get_products_by_category'),
    path('import/', importProducts, name='import_products'),
    path('download_list/', download_product_list_csv, name='download_product_list_csv'),
    path('products_with_review/', list_all_products_with_reviews, name='list_all_products_with_reviews'),
    path('products/<int:product_id>/reviews/', list_reviews_for_product, name='list_reviews_for_product'),
    path('reviews/add/', add_review, name='add-review'),  
    path('reviews/update/<int:review_id>/', update_review, name='update-review'), 
    path('reviews/delete/<int:review_id>/', delete_review, name='delete-review'),  
]
