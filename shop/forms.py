from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    
    class Meta:
        model = Product
        fields = ['name', 'price', 'availability', 'category', 'ingredient']
        widgets = {
            'category': forms.CheckboxSelectMultiple(),
            'ingredient': forms.CheckboxSelectMultiple(),
        }
