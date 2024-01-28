# project_name/urls.py

from django.contrib import admin
from django.urls import include, path
from django.contrib.auth import views as auth_views
from Website import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('Website/', include('Website.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/register/', views.register, name='register'),
    path('accounts/profile/', views.user_profile, name='user_profile'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),  # Add this line for logout
]
