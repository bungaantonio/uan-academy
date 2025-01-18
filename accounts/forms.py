from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-green-500 focus:border-green-500 sm:text-sm',
        'type': 'text',
        'placeholder': 'Digite seu nome de utilizador'
    }))

    password = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-green-500 focus:border-green-500 sm:text-sm',
        'type': 'password',
        'placeholder': 'Digite sua palavra-passe'
    }))


class UserRegistrationForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-green-500 focus:border-green-500 sm:text-sm',
        'type': 'text',
        'placeholder': 'Digite seu nome de utilizador'
    }))

    password1 = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-green-500 focus:border-green-500 sm:text-sm',
        'type': 'password',
        'placeholder': 'Escolha uma palavra-passe forte'
    }))

    password2 = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-green-500 focus:border-green-500 sm:text-sm',
        'type': 'password',
        'placeholder': 'Confirme a sua palavra-passe'
    }))

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
