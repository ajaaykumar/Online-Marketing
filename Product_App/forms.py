from django import forms
from .models import Product

class ProductForm(forms.ModelForm):

    class Meta:
        fields = ['name', 'title', 'category', 'body', 'image', 'price', 'state', 'city', 'location']
