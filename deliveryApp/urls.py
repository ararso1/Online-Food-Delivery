from django.urls import path, include
from .views import *


urlpatterns = [
    
    path('', home, name="home"),
    path('food/', food, name='food'),  
    path('login/', login_view, name='login'),
    path('register/', signup_view, name='register'),
    
    path('add-product/', add_product, name='add_product'),
    path('product-list/', product_list, name='product_list'),
    path('orders/', orders, name='orders'),
    path('logout/', logout_view, name='logout'),  
    path('rest_details/<int:pk>/', rest_details, name='rest_details'),  
    path('restaurant/', restaurant_list, name='restaurant'),
    path('singlepage/<int:pk>/', singlepage, name='singlepage'),  
    path('cart/', cart, name='cart'),  
    path('update_in_stock/', update_in_stock, name='update_in_stock'),
    path('food/category/<int:category_id>/', food_by_category, name='food_by_category'),
    
]





