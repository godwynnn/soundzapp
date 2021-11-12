from django import forms

from django.contrib.auth.models import  User
from django.contrib.auth.forms import UserCreationForm
from django.db.models import fields
from .models import *
from django.template.defaultfilters import filesizeformat
from django.conf import settings
from django.utils.translation import ugettext_lazy as _



class CreateUserForm(UserCreationForm):
    first_name=forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Enter First Name'}))
    last_name=forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Enter Last Name'}))
    username=forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Enter Username'}))
    email=forms.EmailField(widget=forms.TextInput(attrs={'placeholder':'Enter email'}))
    password1=forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Enter Password'}))
    password2=forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Confirm Password'}))
    class Meta:
        model=User
        fields= ['first_name','last_name','username','email','password1','password2']


class BeatForm(forms.ModelForm):
    class Meta:
        model=Beat
        fields="__all__"
        exclude=['date_added','slug']

    def clean_content(self):
        pass
