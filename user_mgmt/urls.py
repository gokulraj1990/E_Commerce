from django.urls import path
from .views import profile_view, profile_create, profile_update,admin_profiles_view,download_profiles_pdf

urlpatterns = [
    path('profile/', profile_view, name='api_profile_view'),
    path('profile/create/', profile_create, name='api_profile_create'),
    path('profile/update/', profile_update, name='api_profile_update'),
    path('profiles/all/', admin_profiles_view, name='admin_profiles_view'),
    path('profiles/download/', download_profiles_pdf, name='download_profiles_pdf'),
]
