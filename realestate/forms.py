from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class Contact(forms.Form):
    name = forms.CharField()
    email = forms.EmailField()
    message = forms.CharField()
