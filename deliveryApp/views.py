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
                return redirect('home')
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


# Create your views here.


def home(request):

    return render(request,"home.html")

def product_view(request):
    return render(request, 'Product.html')

def Services(request):
    return render(request, 'Services.html')

def login_user(request):
    return render(request, 'login.html')

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
