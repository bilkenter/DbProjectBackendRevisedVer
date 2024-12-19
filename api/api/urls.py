from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('users.urls')),  # Redirects the root to the 'users' app URLs
    path('admin/', admin.site.urls),   # Default admin route
]
