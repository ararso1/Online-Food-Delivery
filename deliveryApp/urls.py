from django.urls import path, include
from .views import *


urlpatterns = [
    
    path('', home, name="home"),
    path('login/', login_view, name='login'),
    path('register/', register, name='register'),
    path('logout/', logout_view, name='logout'),
    path('food/', food, name='food'),  
    path('add_Restaurant/',add_Restaurant, name='add_Restaurant'),
    path('contact_us/', contact_us, name='contact_us'),
    path('product_search/',product_search, name='product_search'),
     
    path('add-product/', add_product, name='add_product'),
    path('product-list/', product_list, name='product_list'),
    path("place-order/", place_order, name="place_order"),
    path("cart/", cart_page, name="cart"),
    path("my-orders/", my_orders, name="my_orders"),
    
    path('rest_details/<int:pk>/', rest_details, name='rest_details'),  
    path('restaurant/', restaurants, name='restaurant'),
    path('singlepage/<int:pk>/', singlepage, name='singlepage'),  
    # path('cart/', cart, name='cart'),  
    path('update_in_stock/', update_in_stock, name='update_in_stock'),
    path('food/category/<int:category_id>/', food_by_category, name='food_by_category'),
    
    
    path('seller_dashboard/', seller_dashboard, name='seller_dashboard'),
    path('seller/restaurants/', restaurant_list, name='seller_restaurants'),
    path('seller/restaurants/edit/<int:pk>/', edit_restaurant, name='edit_restaurant'),
    path('seller/restaurants/delete/<int:pk>/', delete_restaurant, name='delete_restaurant'),
    path('products/edit/<int:pk>/', edit_product, name='edit_product'),
    path('products/delete/<int:pk>/', delete_product, name='delete_product'),
    path('products/update_in_stock/', update_in_stock, name='update_in_stock'),

    path("seller/orders/",seller_orders, name="seller_orders"),
    path("seller/orders/update-status/",seller_update_order_item_status, name="seller_update_order_item_status"),

]





