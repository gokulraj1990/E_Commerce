from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('Order_Management.urls')),
    path('user_mgmt/', include('user_mgmt.urls')),
    path('cart_mgmt/', include('cart_mgmt.urls')),
    path('order_mgmt/', include('Order_Management.urls')),
    path('product/', include('product_mgmt.urls')),
    path('admin_console/', include('admin_console.urls')),    

]
