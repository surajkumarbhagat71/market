from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import EmailValidator
from django.contrib.auth.models import User
from .models import *


class User_RegistationForm(UserCreationForm):
    email = forms.EmailField(label='email',validators=[EmailValidator],error_messages={"invalid":'This is invalid email address'})
    first_name = forms.CharField(label='First Name')
    last_name = forms.CharField(label='Last Name')

    class Meta:
        model = User
        fields = ['username','first_name','last_name','email']


class AddressForm(forms.ModelForm):
    class Meta:
        model = UserAddress
        exclude = ('user',)


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = '__all__'


class ItemBrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = '__all__'


class ItemCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'

