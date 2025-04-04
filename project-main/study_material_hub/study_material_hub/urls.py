from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect
from django.contrib.auth import logout

def home_redirect(request):
    return redirect('material_list')  # Redirect '/' to the materials list

# Custom logout view that allows GET requests
def custom_logout(request):
    logout(request)
    return redirect('login')  # Redirect to login page after logout

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_redirect, name='home'),  # Redirect '/' to material list
    path('materials/', include('materials.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    
    # Expose login at /login/ using your custom template
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),

    # Password Reset URLs
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    # Use the custom logout view
    path('logout/', custom_logout, name='logout'),
]

