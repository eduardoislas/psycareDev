from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from .models import CustomUser
from interview.models import Caregiver



class CustomUserCreationForm(UserCreationForm):
    caregiver = forms.ModelChoiceField(
        empty_label = 'Seleccione...',
        required = False,
        queryset = Caregiver.objects.all(),
        widget = forms.Select(
            attrs = {
                'class' : 'form-control choice-caregiver'
            }
        )
    )
    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('caregiver','username', 'email', 'user_type','first_name','last_name')
    
    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget = forms.HiddenInput()
        self.fields['password2'].widget = forms.HiddenInput()
        


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email','first_name','last_name')


