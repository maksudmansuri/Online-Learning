from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django import forms
# from account.models import Account
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):
    email=forms.EmailField()
  #  DOB=forms.DateField()

    class Meta:
        model=User
        fields =["email","username","password1","password2"]
class LoginForm(UserCreationForm):

    class Meta:
      model=User
      fields = ['email', 'password']