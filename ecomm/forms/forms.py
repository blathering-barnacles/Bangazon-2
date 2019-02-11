from django.contrib.auth.models import User
from django import forms
from ecomm.models import Product, Customer

# class EditSettings(forms.Form):
#   lastName = forms.CharField(label='lastName', max_length=20)
#   phone = forms.IntegerField(label='phone', max_length=10)
#   address = forms.CharField(label='address', max_length=20)

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'first_name', 'last_name',)

class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ('title', 'productType', 'description', 'price', 'quantity', 'location',)

# class SearchForm(forms.ModelForm)

#     class