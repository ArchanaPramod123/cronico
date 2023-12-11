
# adminhome/forms.py
from django import forms
from .models import Product, ProductImages

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

class ProductImagesForm(forms.ModelForm):
    class Meta:
        model = ProductImages
        fields = '__all__'
