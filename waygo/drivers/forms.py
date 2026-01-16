# forms.py
from django import forms
from .models import Driver

class DriverRegisterForm(forms.ModelForm):
    email = forms.EmailField(label="Email")
    password = forms.CharField(widget=forms.PasswordInput, label="Пароль")
    phone = forms.CharField(label="Телефон")

    class Meta:
        model = Driver
        fields = ["car_model", "car_number"]
