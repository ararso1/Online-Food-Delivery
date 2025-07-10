from django.urls import path, include
from .views import *


urlpatterns = [
    
    path('', home, name="home"),
    path('food/', food, name='food'),  
    path('login/', login_view, name='login'),
    path('register/', signup_view, name='register'),
    path('Restaurant/', Restaurant, name='Restaurant'),
    path('Navbar/', Navbar, name='Navbar'),
    path('add-product/', add_product, name='add_product'),
    path('product-list/', product_list, name='product_list'),
    path('orders/', orders, name='orders'),
    path('logout/', logout_view, name='logout'),  
    path('rest_details/', rest_details, name='rest_details'),  
    path('restaurant/', restaurant, name='restaurant'),
    path('singlepage/', singlepage, name='singlepage'),  
    path('cart/', cart, name='cart'),  
    
    
]





