from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal

# Corrected and consolidated Profile model
class Profile(models.Model):
    ROLE_CHOICES = (
        ('customer', 'Customer'),
        ('seller', 'Seller'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='customer')  # <-- add default
    def __str__(self):
        return f"{self.user.username} - {self.role}"
    
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)

    def __str__(self):
        return self.name

class Restaurant(models.Model):
    # This ForeignKey links a restaurant to its owner (the user)
    # owner = models.ForeignKey(User, on_delete=models.CASCADE , null=True, blank=True)
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    discription = models.TextField()
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    image = models.ImageField(upload_to='restaurants/', blank=True, null=True)
    open_time = models.TimeField()
    close_time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    # This ForeignKey links a product to its restaurant.
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, null=True, blank=True)
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    offer_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    # To manage multiple images, a more scalable approach is to create a separate model for images.
    # However, for now, we will keep the current setup.
    image1 = models.ImageField(upload_to='products/', blank=True, null=True)
    image2 = models.ImageField(upload_to='products/', blank=True, null=True)
    image3 = models.ImageField(upload_to='products/', blank=True, null=True)
    image4 = models.ImageField(upload_to='products/', blank=True, null=True)
    in_stock = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name
    
ORDER_STATUS_CHOICES = [
    ("pending", "Pending"),
    ("confirmed", "Confirmed"),
    ("preparing", "Preparing"),
    ("out_for_delivery", "Out for Delivery"),
    ("delivered", "Delivered"),
    ("cancelled", "Cancelled"),
]
class Order(models.Model):
    PAYMENT_CHOICES = [
        ("COD", "Cash On Delivery"),
        ("TRANSFER", "Transfer"),
        ("CARD", "Debit Card"),
    ]
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders", null=True)
    address = models.CharField(max_length=255)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES, default="COD")
    total = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, default="pending")  # simple status
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.pk} by {self.customer.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items", null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    seller = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="sold_items")
    restaurant = models.ForeignKey(Restaurant, on_delete=models.SET_NULL, null=True, blank=True)

    # Snapshots at time of purchase
    product_name = models.CharField(max_length=200)
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default="pending")

    def __str__(self):
        return f"{self.product_name} x{self.quantity} (Order #{self.order_id})"