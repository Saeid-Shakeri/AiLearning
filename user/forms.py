from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator

from .models import User

class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')
    username = forms.CharField(max_length=100, help_text='Required')
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')



class EditProfile(forms.ModelForm):
    first_name = forms.CharField(max_length=50,required=False)
    last_name = forms.CharField(max_length=50,required=False)
    username = forms.CharField(max_length=50,required=False)
    email = forms.EmailField(required=False)
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    phone = forms.CharField(validators=[phone_regex],max_length=17,required=False)

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "phone")



class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)

