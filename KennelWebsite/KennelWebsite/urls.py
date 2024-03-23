#urls.py
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.contrib.auth import views as auth_views
from Website.views import RegisterView, ProfileView, UpdateUsernameView, UpdatePasswordView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('Website/', include('Website.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/register/', RegisterView.as_view(), name='register'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('user/profile/', ProfileView.as_view(), name='profile'),
    path('user/update-username/', UpdateUsernameView.as_view(), name='update_username'),
    path('user/update-password/', UpdatePasswordView.as_view(), name='update_password'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)