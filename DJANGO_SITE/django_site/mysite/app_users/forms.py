from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class ExtendUserCreationForm(UserCreationForm):
    first_name = forms.CharField(required=True, max_length=50, help_text='Firstname')
    last_name = forms.CharField(required=False, max_length=50, help_text='Lastname')
    email = forms.EmailField(required=True, help_text='Email')
    city = forms.CharField(required=True, max_length=20, help_text='City')
    phone = forms.CharField(required=False, help_text='Phone')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'password1', 'password2', 'phone', 'email')


class CardForm(forms.Form):
    number = forms.CharField(min_length=16, max_length=16, help_text='Card number')
    exp_month = forms.CharField(min_length=1, max_length=2, help_text='Card expiry month')
    exp_year = forms.CharField(min_length=4, max_length=4, help_text='Card expiry year')
    cvc = forms.CharField(min_length=3, max_length=3, help_text='CVC code')
