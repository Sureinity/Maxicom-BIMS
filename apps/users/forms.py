from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

class CustomUserCreationForm(UserCreationForm):
    sys_firstname = forms.CharField(max_length=150, required=False)
    sys_lastname = forms.CharField(max_length=150, required=False)

    class Meta:
        model = get_user_model()
        fields = ('username', 'sys_firstname', 'sys_lastname', 'password1', 'password2')
