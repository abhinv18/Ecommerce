from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
class SignupForm(UserCreationForm):
    class Meta:
        model=User
        fields=['username','password1','password2','email','first_name','last_name']

from django import forms

class LoginForm(forms.Form):
    username=forms.CharField(max_length=30)
    password=forms.CharField(widget=forms.PasswordInput)

from shop.models import Category, Product

class CategoryForm(forms.ModelForm):
   class Meta:
       model=Category
       fields="__all__"




class ProductForm(forms.ModelForm):
   class Meta:
       model=Product
       fields = ['name', 'description', 'price', 'stock', 'category', 'image']


class StockForm(forms.ModelForm):
   class Meta:
       model=Product
       fields = ['stock']

