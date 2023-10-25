from django import forms
from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.hashers import make_password
from django.forms.widgets import Input,PasswordInput
from typing import Any

class SignupForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username','name','email','address','phone','password1','password2']
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
    
    def save(self, commit: bool = ...) -> Any:
        form = super().save(commit=False)
        form.password = make_password(self.cleaned_data.get('password'))
        
        if commit:
            form.save()

        return form


