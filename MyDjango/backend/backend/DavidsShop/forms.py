from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from django.forms import ModelForm, ModelChoiceField 
from .models import APIUser, Order

class UserSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = APIUser

    def save(self):
        user = super().save(commit=False)
        user.is_admin = False
        user.save()
        return user

class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Your username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Your password'}))

class OrderForm(ModelForm):
    ShippingCountry = forms.CharField(label="Shipping Address", widget=forms.TextInput(attrs={'placeholder':'Country'}))
    ShippingAddress1 = forms.CharField(label="", widget=forms.TextInput(attrs={'placeholder':'Address line 1'}))
    ShippingAddress2 = forms.CharField(label="", widget=forms.TextInput(attrs={'placeholder':'Address line 2'}))
    ShippingAddressZip = forms.CharField(label="", widget=forms.TextInput(attrs={'placeholder':'Zip Code'}))
    class Meta:
        model = Order
        fields = ["ShippingCountry", "ShippingAddress1", "ShippingAddress2", "ShippingAddressZip"]