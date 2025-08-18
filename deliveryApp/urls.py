from django.urls import path, include
from .views import *


urlpatterns = [
    
    path('', home, name="home"),
    path('food/', food, name='food'),  
    path('login/', login_view, name='login'),
    path('register/', signup_view, name='register'),
    path('add_Restaurant/',add_Restaurant, name='add_Restaurant'),
    path('contact_us/', contact_us, name='contact_us'),
    path('product_search/',product_search, name='product_search'),
     
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
    
    
    path('seller_dashboard_home/', seller_dashboard_home, name='seller_dashboard_home'),
    path('seller/restaurants/', seller_restaurants, name='seller_restaurants'),
    path('seller/restaurants/edit/<int:pk>/', edit_restaurant, name='edit_restaurant'),
    path('seller/restaurants/delete/<int:pk>/', delete_restaurant, name='delete_restaurant'),
    path('products/edit/<int:pk>/', edit_product, name='edit_product'),
    path('products/delete/<int:pk>/', delete_product, name='delete_product'),
    path('products/update_in_stock/', update_in_stock, name='update_in_stock'),


]





