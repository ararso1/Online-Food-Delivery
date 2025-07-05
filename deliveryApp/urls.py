from django.urls import path, include
from .views import *


urlpatterns = [
    
    path('', home, name="home"),

    path('product/', product_view, name='product'),
    path('services/', Services, name='Services'),
    path('login_signup/', login_view, name='login_signup'),
    path('add-product/', add_product, name='add_product'),
    path('product-list/', product_list, name='product_list'),
    path('orders/', orders, name='orders'),
    
]





