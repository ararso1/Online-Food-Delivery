from django import forms
from .models import Product, Category

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'category', 'product_price', 'offer_price', 'image1', 'image2', 'image3', 'image4', 'in_stock', 'added_by']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Type here'}),
            'description': forms.Textarea(attrs={'placeholder': 'Type here'}),
            'product_price': forms.NumberInput(attrs={'value': '0'}),
            'offer_price': forms.NumberInput(attrs={'value': '0'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Populate category choices dynamically
        self.fields['category'].queryset = Category.objects.all()
        self.fields['category'].empty_label = "Select Category"

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']