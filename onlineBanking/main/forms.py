from django import forms
from .models import CustomUser,Account,Transaction
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django.contrib.auth.hashers import make_password
from django.forms.widgets import Input,PasswordInput
from typing import Any

class SignupForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username','email','address','phone','password1','password2']
        widgets = {
            'username': Input(attrs={
                'type': 'text',
                'placeholder': 'Username',
                'name': 'username',
            }),
            'password1': PasswordInput(attrs={
                'placeholder': 'enter your password',
                'name': 'password1',
            }),
            'password2': PasswordInput(attrs={
                'placeholder': 'enter your password',
                'name': 'password1',
            })
        }
    
    def clean_username(self,*args,**kwargs):
        username: str = self.cleaned_data.get("username")

        return username.upper()

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ['username','email','address','phone',]
        widgets = {
            'username': Input(attrs={
                'type': 'text',
                'placeholder': 'Username',
                'name': 'username',
            }),
        }

class TransactionForm(forms.Form):
    from_account = forms.CharField(max_length=12,required=True,disabled=True)
    to_account = forms.CharField(max_length=12,required=True)
    money_transfer = forms.DecimalField(max_digits=10,decimal_places=3,required=True)
    detail = forms.CharField(max_length=255,empty_value="transfer money")
    
