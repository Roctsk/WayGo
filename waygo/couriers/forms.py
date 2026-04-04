
# forms.py
from django import forms
from .models import Courier
from django.core.validators import RegexValidator

class CourierRegisterForm(forms.ModelForm):
    email = forms.EmailField(label="Email")
    password = forms.CharField(widget=forms.PasswordInput, label="Пароль")
    phone = forms.CharField(label="Телефон", max_length=13 , validators=[RegexValidator(regex=r'^\+380\d{9}$', message="Введіть рівно 10 цифр")])
    username = forms.CharField(label="Ваша назва")

    class Meta:
        model = Courier
        fields = ("transport",)


class CourierPhotoForm(forms.ModelForm):
    class Meta:
        model = Courier
        fields = ["photo"]