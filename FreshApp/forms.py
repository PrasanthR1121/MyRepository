from django import forms
from .models import *
from django.contrib.auth.models import User

class UserProfileForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ("username", "password", "email")

class PortfolioForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ("profile_pic", "portfolio_url")
        exclude = ('user', )