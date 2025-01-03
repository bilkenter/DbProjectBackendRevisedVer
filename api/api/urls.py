from django.contrib import admin
from django.urls import include, path
from users import views

urlpatterns = [
    path('', include('users.urls')),  # Redirects the root to the 'users' app URLs
    path('admin/', admin.site.urls),   # Default admin route
    path('chat/create', views.get_or_create_chat, name='get_or_create_chat'),
    path('chat/<int:car_id>', views.get_chat_messages, name='get_chat_messages'),
    path('chat/send', views.send_message, name='send_message'),
    path('chat/<int:car_id>/stream', views.chat_stream, name='chat_stream'),
]
