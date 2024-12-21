
from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('create_vehicle_ad/', views.create_vehicle_ad, name='create_vehicle_ad'),  # New path for vehicle ad creation
    path('get_all_cars/', views.get_all_cars, name='get_all_cars'),  # Add this line
]