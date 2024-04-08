from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator

from .models import User

class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200,required=False,widget=forms.TextInput(attrs={'placeholder': 'Your Email'}))
    username = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'placeholder': 'Your username'}))
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1')
        


class EditProfile(forms.ModelForm):
    first_name = forms.CharField(max_length=50,required=False,widget=forms.TextInput(attrs={'placeholder': 'Your First Name'}))
    last_name = forms.CharField(max_length=50,required=False,widget=forms.TextInput(attrs={'placeholder': 'Your Last Name'}))
    username = forms.CharField(max_length=50,required=False,widget=forms.TextInput(attrs={'placeholder': 'Your User Name'}))
    email = forms.EmailField(required=False,widget=forms.TextInput(attrs={'placeholder': 'Your Email'}))
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    phone = forms.CharField(validators=[phone_regex],max_length=17,required=False,widget=forms.TextInput(attrs={'placeholder': 'Your Phone Number'}))

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "phone")
        



class LoginForm(forms.Form):
    username = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'placeholder': 'Your User Name'}))
    password = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Your Password'}))
  
