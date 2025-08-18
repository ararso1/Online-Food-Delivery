from django.shortcuts import render

from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import ProductForm
from .models import *
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.core.files.storage import FileSystemStorage


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
        username = request.POST['new_username']  # ✅ matches input name
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
      # ✅ matches 'confirm_password'
        role = request.POST.get('role')  # 'seller' or 'customer'

        if password1 != password2:
            messages.error(request, "Passwords do not match")
        elif User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
        elif User.objects.filter(email=email).exists():
            messages.error(request, "Email already used")
        elif role not in ['seller', 'customer']:
            messages.error(request, "Please select a role")
        else:
            user = User.objects.create_user(username=username, email=email, password=password1)
            messages.success(request, "Account created successfully.")

            # Redirect based on role
            if role == 'seller':
                return redirect('add_product')  # Your seller dashboard URL name
            else:
                return redirect('home')


    return render(request, 'register.html')

# food deliveryApp/views.py

def food(request):
    foods = Product.objects.filter(in_stock=True)  # Fetch all products
    catergory = Category.objects.filter()  # Fetch all categories
    return render(request, 'food.html', {'foods': foods,'categories': catergory })

def home(request):
    restaurants = Restaurant.objects.all()[:4]
    foods = Product.objects.all()[:4]  # Fetch first 4 products
    category = Category.objects.all()[:6]  # Fetch all categories if needed
    return render(request, 'home.html', {'restaurants': restaurants, 'foods': foods , 'categories': category })

# products/views.py

@login_required(login_url='/accounts/login/')
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES) # request.FILES is crucial for images
        if form.is_valid():
            form.save() # Saves the product and uploaded images
            return redirect('product_list') # Redirect to product list after success
    else:
        form = ProductForm()
    
    context = {'form': form}
    return render(request, 'seller/add_product.html', context)

@login_required(login_url='/login/')
def product_list(request):
    products = Product.objects.all()  # Fetch all products
    print(products[1].image1.url,)
    return render(request, 'seller/product_list.html', {'products': products})


def add_Restaurant(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        address = request.POST.get('address')
        discription = request.POST.get('discription')
        phone_number = request.POST.get('phone_number')
        open_time = request.POST.get('open_time')
        close_time = request.POST.get('close_time')
        image = request.FILES.get('image')

        Restaurant.objects.create(
            name=name,
            address=address,
            discription=discription,
            phone_number=phone_number,
            open_time=open_time,
            close_time=close_time,
            image=image
        )
        return redirect('restaurant')  # Redirect to list or dashboard after saving

    return render(request, 'seller/add_Restaurant.html')

def orders(request):
    return render(request, 'seller/orders.html') 

def contact_us(request):
    return render(request, 'contact_us.html') 

def seller_dashboard_home(request):
    return render(request, 'seller/seller_dashboard_home.html') 



def logout_view(request):
    logout(request)
    return redirect('home')

def rest_details(request, pk):
    restaurant = get_object_or_404(Restaurant, pk=pk)
    foods = Product.objects.filter(restaurant=restaurant)
    return render(request, 'rest_details.html', {'restaurant': restaurant, 'foods': foods})

def restaurant_list(request):
    restaurants = Restaurant.objects.all()
    return render(request, 'restaurant.html', {'restaurants': restaurants})

def singlepage(request, pk):
    food = get_object_or_404(Product, pk=pk)
    category = food.category
    related_foods = Product.objects.filter(category=category).exclude(pk=pk)[:4]  # Fetch related products
    return render(request, 'singlepage.html', {'food': food, 'related_foods': related_foods})

def cart(request):
    return render(request, 'cart.html')

# products/views.py

@require_POST
def update_in_stock(request):
    product_id = request.POST.get('product_id')
    in_stock = request.POST.get('in_stock') == 'true' # Convert string to boolean
    product = get_object_or_404(Product, pk=product_id)
    product.in_stock = in_stock
    product.save()
    return JsonResponse({'status': 'success'})


""" def fetch_restaurant_data(request):
    restaurant = Restaurant.objects.all()
    print(restaurant)
    return render(request, 'restaurant.html', {'restaurant': restaurant}) """
    
def food_by_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    foods = Product.objects.filter(category=category)
    return render(request, 'food_by_category.html', {'foods': foods, 'category': category})

def seller_restaurants(request):
    restaurants = Restaurant.objects.all()  # Optionally, filter by logged-in user if needed
    return render(request, 'seller/restaurant_list.html', {'restaurants': restaurants})

def edit_restaurant(request, pk):
    restaurant = get_object_or_404(Restaurant, pk=pk)

    if request.method == 'POST':
        restaurant.name = request.POST.get('name')
        restaurant.address = request.POST.get('address')
        restaurant.discription = request.POST.get('discription')
        restaurant.phone_number = request.POST.get('phone_number')
        restaurant.open_time = request.POST.get('open_time')
        restaurant.close_time = request.POST.get('close_time')
        if request.FILES.get('image'):
            restaurant.image = request.FILES.get('image')
        restaurant.save()
        return redirect('seller_restaurants')

    return render(request, 'seller/edit_restaurant.html', {'restaurant': restaurant})

def delete_restaurant(request, pk):
    restaurant = get_object_or_404(Restaurant, pk=pk)
    restaurant.delete()
    return redirect('seller_restaurants')

def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.name = request.POST.get('name')
        product.product_price = request.POST.get('product_price')
        product.category_id = request.POST.get('category')
        if request.FILES.get('image1'):
            product.image1 = request.FILES.get('image1')
        product.save()
        return redirect('product_list')
    categories = Category.objects.all()
    return render(request, 'seller/edit_product.html', {'product': product, 'categories': categories})

def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.delete()
    return redirect('product_list')

from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def update_in_stock(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        in_stock = request.POST.get('in_stock') == 'true'
        product = get_object_or_404(Product, id=product_id)
        product.in_stock = in_stock
        product.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=400)

from django.http import JsonResponse
from .models import Product  # or whatever your product model is

def product_search(request):
    query = request.GET.get('q', '')
    products = Product.objects.all()
    if query:
        products = products.filter(name__icontains=query)
    products = products.order_by('name')  # <-- This orders alphabetically by name

    # If returning JSON for AJAX:
    data = [
        {
            'id': p.id,
            'name': p.name,
            'price': p.price,
            # add other fields as needed
        }
        for p in products
    ]
    return JsonResponse({'products': data})