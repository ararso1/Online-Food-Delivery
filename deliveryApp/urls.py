from django.urls import path, include
from .views import *


urlpatterns = [
    
    path('', home, name="home"),

   
    path('Food/', Food_usage, name='product'),  
    path('login/', login_view, name='login'),
    path('register/', signup_view, name='register'),
    path('Restaurant/', Restaurant, name='Restaurant'),
    path('Navbar/', Navbar, name='Navbar'),
    path('add-product/', add_product, name='add_product'),
    path('product-list/', product_list, name='product_list'),
    path('orders/', orders, name='orders'),
    path('logout/', logout_view, name='logout'),
    path('chanole/', chanole, name='chanole'),  
    path('sishu/', sishu, name='sishu'),  
    path('hebesha/', hebesha, name='hebesha'),  
    path('pizzahut/', pizzahut, name='pizzahut'),  
    path('smashburger/', smashburger, name='smashburger'),  
    
    
]





