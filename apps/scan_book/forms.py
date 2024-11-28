from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

class ManualInputBarcodeForm(forms.Form):
    barcode_manual = forms.IntegerField()