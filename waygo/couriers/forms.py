
# forms.py
from django import forms
from .models import Courier

class CourierRegisterForm(forms.ModelForm):
    email = forms.EmailField(label="Email")
    password = forms.CharField(widget=forms.PasswordInput, label="Пароль")
    phone = forms.CharField(label="Телефон")

    class Meta:
        model = Courier
        fields = ("transport",)
