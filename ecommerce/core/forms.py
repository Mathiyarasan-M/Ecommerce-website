from django import forms
from core.models import *

class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields='__all__'
        widgets = {
            'name':forms.TextInput(attrs={'class':'input'}),
            'catagory':forms.Select(attrs={'class':'input'}),
            'desc':forms.Textarea(attrs={'class':'input'}),
            'original_price':forms.NumberInput(attrs={'class':'input'}),
            'selling_pric':forms.NumberInput(attrs={'class':'input'}),
            'product_available_count':forms.NumberInput(attrs={'class':'input'}),
            'img':forms.FileInput(attrs={'class':'input'}),
        }

class CheckoutForm(forms.Form):
    street_address=forms.CharField(widget=forms.TextInput(attrs={
        'class':'form-control',
        'placeholder':'1234 address',
    }))
    district=forms.CharField(widget=forms.TextInput(attrs={
        'class':'form-control',
        'placeholder':'sivaganga'
    }))
    pin=forms.CharField(widget=forms.TextInput(attrs={
        'class':'form-control',
        'placeholder':'123 456'
    }))