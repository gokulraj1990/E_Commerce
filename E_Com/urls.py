from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('Order_Management.urls')),
    path('user_management/', include('user_mgmt.urls')),
    path('product/', include('product_mgmt.urls')),
    

]
