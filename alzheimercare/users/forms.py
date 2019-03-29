from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from .models import CustomUser



class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('username', 'email', 'user_type','first_name','last_name','groups')

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email','first_name','last_name')


