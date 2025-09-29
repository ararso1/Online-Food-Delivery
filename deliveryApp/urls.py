from django.urls import path
from .views import *

urlpatterns = [
    # ===== AUTHENTICATION =====
    path('login/', login_view, name='login'),
    path('register/', register, name='register'),
    path('logout/', logout_view, name='logout'),
    
    # ===== PUBLIC PAGES =====
    path('', home, name="home"),
    path('food/', food, name='food'),
    path('food/category/<int:category_id>/', food_by_category, name='food_by_category'),
    path('restaurant/', restaurants, name='restaurant'),
    path('contact_us/', contact_us, name='contact_us'),
    path('rest_details/<int:pk>/', rest_details, name='rest_details'),
    path('singlepage/<int:pk>/', singlepage, name='singlepage'),
    
    # ===== CUSTOMER FEATURES =====
    path('cart/', cart_page, name="cart"),
    path('place-order/', place_order, name="place_order"),
    path('my-orders/', my_orders, name="my_orders"),
    path('orders/delete/<int:order_id>/', delete_order, name='delete_order'),
    
    # ===== SELLER DASHBOARD =====
    path('seller_dashboard/', seller_dashboard, name='seller_dashboard'),
    
    # ===== SELLER PRODUCT MANAGEMENT =====
    path('add-product/', add_product, name='add_product'),
    path('product-list/', product_list, name='product_list'),
    path('products/edit/<int:pk>/', edit_product, name='edit_product'),
    path('products/delete/<int:pk>/', delete_product, name='delete_product'),
    path('products/update_in_stock/', update_in_stock, name='update_in_stock'),
    
    # ===== SELLER RESTAURANT MANAGEMENT =====
    path('add_Restaurant/', add_Restaurant, name='add_Restaurant'),
    path('seller/restaurants/', restaurant_list, name='seller_restaurants'),
    path('seller/restaurants/edit/<int:pk>/', edit_restaurant, name='edit_restaurant'),
    path('seller/restaurants/delete/<int:pk>/', delete_restaurant, name='delete_restaurant'),
    
    # ===== SELLER ORDER MANAGEMENT =====
    path('seller/orders/', seller_orders, name="seller_orders"),
    path('seller/orders/update-status/', seller_update_order_item_status, name="seller_update_order_item_status"),
]