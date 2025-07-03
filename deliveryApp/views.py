from django.shortcuts import render

# Create your views here.


def home(request):

    return render(request,"home.html")

def product_view(request):
    return render(request, 'Product.html')

def Services(request):
    return render(request, 'Services.html')
