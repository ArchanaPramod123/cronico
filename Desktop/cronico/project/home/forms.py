from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms

class SignUpForm(UserCreationForm):
    class Meta:
        model= User
        fields=['username','first_name','last_name','email']

class AddToCartForm(forms.Form):
    quantity = forms.IntegerField(min_value=1, initial=1)

    