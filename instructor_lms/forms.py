from django.forms import ModelForm
from front.models import Course,Course_Session
from accounts.models import Staffs
class CreateCourse(ModelForm):
    class Meta:
      model=Course
      fields = ["course_requirement","course_desc","course_why_take"]

class CreateAbout(ModelForm):
  class Meta:
    model=Staffs
    fields = ["about"]


class CreateSession(ModelForm):
    class Meta:
      model=Course_Session
      fields ='__all__'
    




# from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth import login, authenticate
# from django import forms
# from django.contrib.auth.models import User 

# class RegisterForm(UserCreationForm):
#     email=forms.EmailField()
#   #  DOB=forms.DateField()

#     class Meta:
#         model=User
#         fields =["email","username","password1","password2"]
# class LoginForm(UserCreationForm):

#     class Meta:
#       model=User
#       fields = ['username', 'password']