from django.urls import path
from .views import profile_view, profile_create, profile_update,admin_profiles_view,download_profiles_pdf,change_password,deactivate_account


urlpatterns = [
    path('profile/', profile_view, name='api_profile_view'),
    path('profile/create/', profile_create, name='api_profile_create'),
    path('profile/update/', profile_update, name='api_profile_update'),
    path('profile/deactivate/', deactivate_account, name='deactivate_account'),
    path('profile/all/', admin_profiles_view, name='admin_profiles_view'),
    path('profile/change_password/', change_password, name='change_password'),    
    path('profile/download/', download_profiles_pdf, name='download_profiles_pdf'),
]
