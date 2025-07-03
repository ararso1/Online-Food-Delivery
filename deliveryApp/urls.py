from django.urls import path, include
from .views import *
from . import views


urlpatterns = [
    
    path('', home, name="home"),

    path('product/', product_view, name='product'),
     path('services/', product_view, name='Services'),

]





