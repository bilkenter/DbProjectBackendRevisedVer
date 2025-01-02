
from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('create_vehicle_ad/', views.create_vehicle_ad, name='create_vehicle_ad'),  # New path for vehicle ad creation
    path('get_all_cars/', views.get_all_cars, name='get_all_cars'),  # Add this line
    path('get_all_users/', views.get_all_users, name='get_all_users'),  # Add this line
    path('get_seller_ads/', views.get_seller_ads, name='get_seller_ads'),  # Add this line
    path('delete_ad/', views.delete_ad, name='delete_ad'),  # Add this line
    path('get_user_data/', views.get_user_data, name='get_user_data'),  # Add this line

]
