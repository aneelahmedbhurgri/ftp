from django import forms
from django.db.models import fields
from .models import *

class UploadFileForm(forms.Form):
    file = forms.FileField()

class AuthUserForm(forms.ModelForm):
    Password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = AuthUser
        fields = ['Name','Email']

class AuthRegForm(forms.ModelForm):
    Password = forms.CharField(widget=forms.PasswordInput())
    SecurityCode = forms.CharField(widget=forms.PasswordInput(),label='Security Code')
    class Meta:
        model = AuthUser
        fields = ['Name','Email']