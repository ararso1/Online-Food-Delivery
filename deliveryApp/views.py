from django.shortcuts import render

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User
from django.contrib import messages
# python code

""" def login_view(request):
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
 """

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            auth_login(request, user)
            return redirect('add_product')  # Change as needed
        else:
            messages.error(request, 'Invalid credentials')
    return render(request, 'login.html')

def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 != password2:
            messages.error(request, "Passwords do not match")
        elif User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
        elif User.objects.filter(email=email).exists():
            messages.error(request, "Email already used")
        else:
            User.objects.create_user(username=username, email=email, password=password1)
            messages.success(request, "Account created successfully. Please login.")
            return redirect('login')
    return render(request, 'register.html')

# food deliveryApp/views.py

def food(request):
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
            'name': 'Chicken Burger',
            'category': 'Crispy Chicken Burger with Cheese and Lettuce',
            'image': 'images/Foods/chickn.jpg',
            'price': 45,
            'old_price': 50,
            'rating': 4.5,
        },
        {
            'name': 'pepperoni pizza',
            'category': 'Pepperoni Pizza with Extra Cheese',
            'image': 'images/Foods/Pepperoni Pizza .jpg',
            'price': 140,
            'old_price': 150,
            'rating': 4.5,
        },
        {
            'name': 'gourmet pizza',
            'category': 'Gourmet Pizza with Fresh Ingredients',
            'image': 'images/Foods/Healthy Pizza .jpg',
            'price': 130,
            'old_price': 140,
            'rating': 4.0,
        },
        {
            'name': 'cheese pizza',
            'category': 'Cheese Pizza with Extra Toppings',
            'image': 'images/Foods/cheese.jpg',
            'price': 230,
            'old_price': 250,
            'rating': 4.5,
        },
        {
            'name': 'chicken pizza',
            'category': 'Chicken Pizza with Spicy Sauce',
            'image': 'images/Foods/chicken pizza.jpg',
            'price': 520,
            'old_price': 550,
            'rating': 4.0,
        },
        {
            'name': 'chicken Noodles',
            'category': 'Chicken Noodles with Vegetables',
            'image': 'images/Foods/.jpg',
            'price': 520,
            'old_price': 550,
            'rating': 4.0,
        },
        {
            'name': ' Beef Noodle',
            'category': 'Tomato Egg and Beef Noodle Soup',
            'image': 'images/Foods/beef nooddle.jpg',
            'price': 520,
            'old_price': 550,
            'rating': 4.0,
        },
        {
            'name': 'Firfir',
            'category': 'Firir with egg and Injera',
            'image': 'images/Foods/firfir.jpg',
            'price': 520,
            'old_price': 550,
            'rating': 4.0,
        },
        {
            'name': 'Kitfo',
            'category': 'Kitfo with Gomen and Ayib',
            'image': 'images/Foods/kitfo.jpg',
            'price': 520,
            'old_price': 550,
            'rating': 4.0,
        },
        {
            'name': 'Tibs',
            'category': 'Tibs with Injera',
            'image': 'images/Foods/tibs.jpg',
            'price': 520,
            'old_price': 550,
            'rating': 4.0,
        },
        {
            'name': 'sushi',
            'category': 'Sushi with Salmon and Avocado',
            'image': 'images/Foods/sushi.jpg',
            'price': 520,
            'old_price': 550,
            'rating': 4.0,
        },
    
        # Add up to 22 total entries as you wish...
    ]
    return render(request, 'food.html', {'products': products})



# Create your views here.
# In a real application, you would fetch actual product data from a database here
# For now, it just renders the static HTML.

def home(request):
    return render(request,"home.html")

def Restaurant(request):
    return render(request, 'Restaurant.html')
def Navbar(request):
    return render(request, 'Navbar.html')
def add_product(request):
    return render(request, 'seller/add_product.html')
def product_list(request):
    return render(request, 'seller/product_list.html')
def orders(request):
    return render(request, 'seller/orders.html') 
def logout_view(request):
    logout(request)
    return redirect('home')
def rest_details(request):
    return render(request, 'rest_details.html')
def restaurant(request):
    return render(request, 'restaurant.html')
def singlepage(request):
    return render(request, 'singlepage.html')
def cart(request):
    return render(request, 'cart.html')


