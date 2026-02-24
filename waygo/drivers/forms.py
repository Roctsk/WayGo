# forms.py
from django import forms
from .models import Driver

class DriverRegisterForm(forms.ModelForm):
    email = forms.EmailField(label="Email")
    password = forms.CharField(widget=forms.PasswordInput, label="Пароль")
    phone = forms.CharField(label="Телефон")
    username = forms.CharField(label="Ваша назва")
    city = forms.CharField(max_length=100, required=True, label="Місто")
    

    class Meta:
        model = Driver
        fields = ["car_model", "car_number",'city']


class DriverPhotoForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ["photo"]