from django import forms
from .models import TaxiOrder

class TaxiOrderForm(forms.ModelForm):
    class Meta:
        model = TaxiOrder
        fields = ("pickup_address", "destination_address","comment")
        widgets = {
            'pickup_address': forms.TextInput(attrs={'class':'form-control','placeholder':'Наприклад, вул. Хрещатик, 22'}),
            'destination_address': forms.TextInput(attrs={'class':'form-control','placeholder':'Наприклад, вул. Сумська, 10'}),
            'comment': forms.Textarea(attrs={'class':'form-control','rows':2, 'placeholder':'Наприклад, біля АТБ'}),
        }