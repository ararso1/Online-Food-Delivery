from django.urls import path, include
from .views import *


urlpatterns = [
    
    path('', home, name="home"),

   
    path('Food/', Food_usage, name='product'),  

    path('services/', Services, name='Services'),
    path('login_signup/', login_view, name='login_signup'),
    path('Restaurant/', Restaurant, name='Restaurant'),
    path('Navbar/', Navbar, name='Navbar'),
    path('add-product/', add_product, name='add_product'),
    path('product-list/', product_list, name='product_list'),
    path('orders/', orders, name='orders'),
    path('logout/', logout_view, name='logout'),
    
    
]





