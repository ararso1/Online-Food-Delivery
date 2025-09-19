from django.shortcuts import render
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate, login, logout as auth_logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import ProductForm
from .models import *
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.core.files.storage import FileSystemStorage
import json
from django.contrib import messages
from .models import Profile
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_exempt
from decimal import Decimal
import json
from django.db.models import Sum
from django.http import JsonResponse, HttpResponseBadRequest
from django.utils import timezone
from django.db import transaction
from django.views.decorators.csrf import ensure_csrf_cookie
from django.urls import reverse

def user_is_seller(user) -> bool:
    return Profile.objects.filter(user=user, role="seller").exists()

def require_seller(request):
    if not user_is_seller(request.user):
        messages.error(request, "Seller access required.")
        return redirect("home")  # or your login/landing page
    return None

# login and registration views
def register(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        role = request.POST.get('role')
        print(name, email, password, role)
        if User.objects.filter(username=email).exists():
            messages.error(request, "User already exists.")
            return render(request, 'register.html')

        user = User.objects.create_user(username=email, email=email, password=password, first_name=name)
        Profile.objects.create(user=user, role=role)

        messages.success(request, "Account created successfully!")
        
        # --- Corrected Redirection Logic ---
        if role == 'seller':
            return redirect('seller_dashboard')  # Redirect to the seller's dashboard
        elif role == 'customer':
            return redirect('home')  # Redirect to the customer's home page
        else:
            # Handle unexpected role values, perhaps by showing an error
            messages.error(request, 'Invalid user role selected.')
            return redirect('register')

    return render(request, 'register.html')

def login_view(request):
    if request.method == 'POST':
        email = (request.POST.get('email') or '').strip().lower()
        password = request.POST.get('password') or ''
        user = None

        # Find the user by email (case-insensitive), then authenticate with username+password
        try:
            user_obj = User.objects.get(email__iexact=email)
            user = authenticate(request, username=user_obj.username, password=password)
        except User.DoesNotExist:
            user_obj = None

        if user is not None:
            if not user.is_active:
                messages.error(request, "Your account is inactive.")
                return render(request, 'login.html', {'email': email})

            login(request, user)
            messages.success(request, "Login successful!")

            # Respect ?next= if present
            next_url = request.GET.get('next') or request.POST.get('next')
            if next_url:
                return redirect(next_url)

            # Role-based redirect
            role = None
            try:
                role = user.profile.role  # OneToOne: User -> Profile
            except Profile.DoesNotExist:
                role = None  # No profile yet

            if role == 'seller':
                return redirect('seller_dashboard')
            elif role == 'customer':
                return redirect('home')  # or 'customer_dashboard'
            else:
                # Fallback if no profile/role set
                return redirect('home')

        # Invalid credentials
        messages.error(request, "Invalid email or password.")
        return render(request, 'login.html', {'email': email})

    # GET
    return render(request, 'login.html')

def logout_view(request):
    auth_logout(request)
    return redirect('home')

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


def orders(request):
    return render(request, 'seller/orders.html') 

def contact_us(request):
    return render(request, 'contact_us.html') 

def _ensure_seller(user):
    # Guard: allow only logged-in users with role 'seller'
    try:
        return Profile.objects.filter(user=user, role="seller").exists()
    except Profile.DoesNotExist:
        return False
    
@login_required
def seller_dashboard(request):
    if not _ensure_seller(request.user):
        # Optionally redirect non-sellers to home (or show 403)
        return redirect("home")

    user = request.user
    
    products_qs = Product.objects.filter(added_by=user)
    restaurants_qs = Restaurant.objects.filter(added_by=user)

    total_products = products_qs.count()
    in_stock = products_qs.filter(in_stock=True).count()
    out_stock = total_products - in_stock
    total_restaurants = restaurants_qs.count()

    # Optional: if you have Order / OrderItem models, compute them;
    # otherwise safely default to 0.
    total_orders = 0
    total_revenue = Decimal("0.00")
    try:
        from .models import Order  # if exists
        seller_orders = Order.objects.filter(restaurant__added_by=user)
        total_orders = seller_orders.count()
        total_revenue = seller_orders.aggregate(total=Sum("total_amount"))["total"] or Decimal("0.00")
    except Exception:
        pass

    # Chart: products added per month (last 6 months)
    labels, product_counts = [], []
    # anchor on the first day of the current month
    month_anchor = timezone.now().date().replace(day=1)

    # helper to step months backward without extra deps
    def add_months(d, m):
        y, mo = d.year + (d.month + m - 1) // 12, (d.month + m - 1) % 12 + 1
        day = 1
        return d.replace(year=y, month=mo, day=day)

    for i in range(5, -1, -1):
        month_start = add_months(month_anchor, -i)
        next_month = add_months(month_start, 1)
        count = products_qs.filter(created_at__date__gte=month_start,
                                   created_at__date__lt=next_month).count()
        labels.append(month_start.strftime("%b %Y"))
        product_counts.append(count)

    recent_products = products_qs.order_by("-created_at")[:5]

    context = {
        "total_products": total_products,
        "in_stock": in_stock,
        "out_stock": out_stock,
        "total_restaurants": total_restaurants,
        "total_orders": total_orders,
        "total_revenue": total_revenue,
        "recent_products": recent_products,
        # JSON for Chart.js
        "chart_labels": json.dumps(labels),
        "chart_values": json.dumps(product_counts),
    }
    return render(request, "seller/seller_dashboard.html", context)

# def seller_dashboard(request):
#     return render(request, 'seller/seller_dashboard.html') 

def logout_view(request):
    logout(request)
    return redirect('home')

def rest_details(request, pk):
    restaurant = get_object_or_404(Restaurant, pk=pk)
    foods = Product.objects.filter(restaurant=restaurant)
    return render(request, 'rest_details.html', {'restaurant': restaurant, 'foods': foods})

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


    
def food_by_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    foods = Product.objects.filter(category=category)
    return render(request, 'food_by_category.html', {'foods': foods, 'category': category})

def restaurants(request):
    restaurants = Restaurant.objects.all()  # Optionally, filter by logged-in user if needed
    return render(request, 'Restaurant.html', {'restaurants': restaurants})

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
            # 'price': p.price,
            # add other fields as needed
        }
        for p in products
    ]
    return JsonResponse({'products': data})

# orders/views.py

PAYMENT_MAP = {
    "Cash On Delivery": "COD",
    "Transfer": "TRANSFER",
    "Debit Card": "CARD",
}

@ensure_csrf_cookie
def cart_page(request):
    # Render your cart template (the one with the JS below)
    return render(request, "cart.html")

def _is_customer(user):
    try:
        return user.profile.role == "customer"
    except Profile.DoesNotExist:
        return True

def _server_price(product: Product) -> Decimal:
    return product.offer_price or product.product_price

@require_POST
@transaction.atomic
def place_order(request):
    # Return 401 JSON if not logged in (so fetch can redirect)
    if not request.user.is_authenticated:
        login_url = f"{reverse('login')}?next={reverse('deliveryApp:cart')}"
        return JsonResponse({"success": False, "not_authenticated": True, "login_url": login_url}, status=401)

    if not _is_customer(request.user):
        return JsonResponse({"success": False, "error": "Only customers can place orders."}, status=403)

    try:
        data = json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError:
        return HttpResponseBadRequest("Invalid JSON payload.")

    items = data.get("items", [])
    address = (data.get("address") or "Default Address").strip()
    payment_label = (data.get("payment_method") or "Cash On Delivery").strip()
    payment_map = {"Cash On Delivery": "COD", "Transfer": "TRANSFER", "Debit Card": "CARD"}
    payment_method = payment_map.get(payment_label, "COD")

    if not items:
        return JsonResponse({"success": False, "error": "Cart is empty."}, status=400)

    order = Order.objects.create(
        customer=request.user,
        address=address,
        payment_method=payment_method,
        total=Decimal("0.00"),
        status="pending",
    )

    server_total = Decimal("0.00")

    for raw in items:
        raw_id = raw.get("id", None)

        # Prefer a straight int() cast; then fallback to digit extraction
        product_id = None
        try:
            product_id = int(raw_id)
        except (TypeError, ValueError):
            s = str(raw_id or "")
            digits = "".join(ch for ch in s if ch.isdigit())
            if digits:
                product_id = int(digits)

        if not isinstance(product_id, int):
            transaction.set_rollback(True)
            return JsonResponse({"success": False, "error": f"Invalid product id: {raw_id}"}, status=400)

        product = Product.objects.select_related("restaurant", "added_by").filter(pk=product_id).first()
        if not product:
            transaction.set_rollback(True)
            return JsonResponse({"success": False, "error": f"Product not found: {product_id}"}, status=404)

        if not product.in_stock:
            transaction.set_rollback(True)
            return JsonResponse({"success": False, "error": f"Out of stock: {product.name}"}, status=400)

        qty = max(1, int(raw.get("quantity", 1)))
        price = _server_price(product)
        subtotal = price * Decimal(qty)

        OrderItem.objects.create(
            order=order,
            product=product,
            seller=product.added_by,
            restaurant=product.restaurant,
            product_name=product.name,
            product_price=price,
            quantity=qty,
            subtotal=subtotal,
        )
        server_total += subtotal

    order.total = server_total.quantize(Decimal("0.01"))
    order.save(update_fields=["total"])

    return JsonResponse({
        "success": True,
        "order_id": order.id,
        "total": str(order.total),
        "items_count": order.items.count(),
    })

@login_required(login_url="/login/")
def add_product(request):
    # Require seller role
    if (resp := require_seller(request)) is not None:
        return resp

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)  # keep FILES for images
        if form.is_valid():
            product = form.save(commit=False)
            product.added_by = request.user  # <-- enforce ownership
            product.save()
            messages.success(request, "Product created.")
            return redirect("product_list")
    else:
        form = ProductForm()

    return render(request, "seller/add_product.html", {"form": form})


@login_required(login_url="/login/")
def product_list(request):
    # Require seller role
    if (resp := require_seller(request)) is not None:
        return resp

    # Only show current seller's products
    products = (
        Product.objects.filter(added_by=request.user)
        .select_related("restaurant", "category")
        .order_by("-created_at")
    )

    # (Avoid indexing like products[1] – it crashes when < 2 items)
    return render(request, "seller/product_list.html", {"products": products})


@login_required(login_url="/login/")
def add_Restaurant(request):
    # Require seller role
    if (resp := require_seller(request)) is not None:
        return resp

    if request.method == "POST":
        name = request.POST.get("name")
        address = request.POST.get("address")
        discription = request.POST.get("discription")
        phone_number = request.POST.get("phone_number")
        open_time = request.POST.get("open_time")
        close_time = request.POST.get("close_time")
        image = request.FILES.get("image")

        Restaurant.objects.create(
            name=name,
            address=address,
            discription=discription,
            phone_number=phone_number,
            open_time=open_time,
            close_time=close_time,
            image=image,
            added_by=request.user,  # <-- enforce ownership
        )
        messages.success(request, "Restaurant created.")
        return redirect("seller_restaurants")  # keep consistent with your sidebar

    return render(request, "seller/add_Restaurant.html")


@login_required(login_url="/login/")
def restaurant_list(request):
    # Only show current seller's restaurants
    restaurants = Restaurant.objects.filter(added_by=request.user).order_by("-created_at")
    return render(request, "seller/restaurant_list.html", {"restaurants": restaurants})

@login_required(login_url="/login/")
def my_orders(request):
    """
    Current user's orders, newest first. We also compute:
      - qty_sum: total quantity across items
      - first_item: to show a thumbnail/name/category like your mock
    """
    orders = (
        Order.objects.filter(customer=request.user)
        .prefetch_related("items__product__category")
        .order_by("-created_at")
    )

    enriched = []
    for o in orders:
        items = list(o.items.all())
        qty_sum = sum(i.quantity for i in items)
        first_item = items[0] if items else None
        enriched.append({
            "order": o,
            "qty_sum": qty_sum,
            "first_item": first_item,
        })

    return render(request, "my_orders.html", {"orders": enriched})

@login_required(login_url="/login/")
def seller_orders(request):
    if not user_is_seller(request.user):
        return render(request, "seller/not_allowed.html", status=403)

    items = (
        OrderItem.objects
        .filter(seller=request.user)
        .select_related("order", "product", "product__category", "order__customer")
        .order_by("-order__created_at", "-id")
    )
    return render(request, "seller/seller_orders.html", {
        "items": items,
        "status_choices": ORDER_STATUS_CHOICES,
    })

@require_POST
@login_required(login_url="/login/")
def seller_update_order_item_status(request):
    if not user_is_seller(request.user):
        return JsonResponse({"ok": False, "error": "Forbidden"}, status=403)

    item_id = request.POST.get("item_id")
    new_status = request.POST.get("status", "").strip()

    valid_keys = {k for k, _ in ORDER_STATUS_CHOICES}
    if not item_id or new_status not in valid_keys:
        return HttpResponseBadRequest("Invalid parameters")

    item = get_object_or_404(OrderItem, id=item_id, seller=request.user)
    item.status = new_status
    item.save(update_fields=["status"])

    # Roll up parent order.status based on all items
    order = item.order
    statuses = list(order.items.values_list("status", flat=True))

    if all(s == "delivered" for s in statuses):
        order.status = "delivered"
    elif all(s == "cancelled" for s in statuses):
        order.status = "cancelled"
    elif any(s == "out_for_delivery" for s in statuses):
        order.status = "out_for_delivery"
    elif any(s == "preparing" for s in statuses):
        order.status = "preparing"
    elif any(s == "confirmed" for s in statuses):
        order.status = "confirmed"
    else:
        order.status = "pending"
    order.save(update_fields=["status"])

    return JsonResponse({"ok": True, "order_status": order.status})