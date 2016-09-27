from django import forms
from django.contrib.auth.models import User

from .models import Person, Permission, Role

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ( 'username', 'email', 'password')

class PersonForm(forms.ModelForm):

    class Meta:
        model = Person
        fields = ( 'disp_title', 'disp_given', 'disp_family', 'photo')


