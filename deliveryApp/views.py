from django.shortcuts import render

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages

# python code

def login_view(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'login':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('add_product')
            else:
                messages.error(request, 'Invalid credentials.')

        elif action == 'signup':
            username = request.POST['new_username']
            email = request.POST['email']
            password = request.POST['new_password']

            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already taken.')
            else:
                user = User.objects.create_user(username=username, password=password, email=email)
                login(request, user)
                return redirect('home')

    return render(request, 'login.html')


# food deliveryApp/views.py

def Food_usage(request):
    products = [
        {
            'name': 'Smash Burgers',
            'category': 'Smash Burger with Baconnais Sauce knedir',
            'image': 'images/Foods/Smash Burgers- Knedir Recipes.jpg',
            'price': 35,
            'old_price': 40,
            'rating': 4.5,
        },
        {
            'name': 'classic burger',
            'category': 'Classic American Burger with fried Egg',
            'image': 'images/Foods/Classic American Burger with fried egg.jpg',
            'price': 28,
            'old_price': 30,
            'rating': 4.0,
        },
        {
            'name': 'chili cheese burger',
            'category': 'patches of chili cheese burger',
            'image': 'images/Foods/chilly burger.jpg',
            'price': 90,
            'old_price': 100,
            'rating': 4.0,
        },
        {
            'name': 'Banana 1kg',
            'category': 'Fruits',
            'image': 'images/banana.png',
            'price': 45,
            'old_price': 50,
            'rating': 4.5,
        },
        {
            'name': 'Mango 1kg',
            'category': 'Fruits',
            'image': 'images/mango.png',
            'price': 140,
            'old_price': 150,
            'rating': 4.5,
        },
        {
            'name': 'Cheese 200g',
            'category': 'Dairy',
            'image': 'images/cheese.png',
            'price': 130,
            'old_price': 140,
            'rating': 4.0,
        },
        {
            'name': 'Wheat Flour 5kg',
            'category': 'Grains',
            'image': 'images/wheat_flour.png',
            'price': 230,
            'old_price': 250,
            'rating': 4.5,
        },
        {
            'name': 'Basmati Rice 5kg',
            'category': 'Grains',
            'image': 'images/rice.png',
            'price': 520,
            'old_price': 550,
            'rating': 4.0,
        },
        # Add up to 22 total entries as you wish...
    ]
    return render(request, 'Food.html', {'products': products})



# Create your views here.


def home(request):

    return render(request,"home.html")

def Food(request):
    return render(request, 'Food.html')

def Services(request):
    return render(request, 'Services.html')

def Restaurant(request):
    return render(request, 'Restaurant.html')

def Navbar(request):
    return render(request, 'Navbar.html')

from django.shortcuts import render

def add_product(request):
    return render(request, 'seller/add_product.html')

def product_list(request):
    # In a real application, you would fetch actual product data from a database here
    # For now, it just renders the static HTML.
    return render(request, 'seller/product_list.html')

def orders(request):
    return render(request, 'seller/orders.html') # You'll create this HTML file

def logout_view(request):
    logout(request)
    return redirect('home')
