from django import forms

class ManualInputBarcodeForm(forms.Form):
    barcode_manual = forms.IntegerField()
