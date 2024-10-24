from django.urls import path
from .views import profile_view, profile_create, profile_update,change_password,deactivate_account
from .views import list_users,update_user_status,download_user_list_csv,admin_profiles_view,download_profiles_pdf

urlpatterns = [
    path('profile/', profile_view, name='api_profile_view'),
    path('profile/create/', profile_create, name='api_profile_create'),
    path('profile/update/', profile_update, name='api_profile_update'),
    path('profile/deactivate/', deactivate_account, name='deactivate_account'),
    path('profile/all/', admin_profiles_view, name='admin_profiles_view'),
    path('profile/change_password/', change_password, name='change_password'),    
    path('profile/download/', download_profiles_pdf, name='download_profiles_pdf'), 
    path('users/', list_users, name='list_users'),
    path('users/update-status/<uuid:user_id>/', update_user_status, name='update_user_status'),
    path('users/download/', download_user_list_csv, name='download_user_list_csv'), 

]
