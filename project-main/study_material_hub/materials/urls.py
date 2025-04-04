from django.urls import path
from . import views  # ✅ Import the full views module

urlpatterns = [
    path('upload/', views.upload_material, name='upload_material'),
    path('list/', views.material_list, name='material_list'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('delete/<int:material_id>/', views.delete_material, name='delete_material'),
    path('download/<int:material_id>/', views.download_material, name='download_material'),  # ✅ Fixed import
    path('profile/',views.user_profile, name='user_profile'),

]




