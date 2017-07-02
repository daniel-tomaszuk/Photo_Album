from django import forms
from django.core.validators import *
from django.core.exceptions import *
from .models import *

class AddPhotoForm(forms.Form):
    server_path = forms.CharField(max_length=128, required=False)
    disk_file = forms.FileField(required=False)


    # def clean(self):
    #     # if not ((self.cleaned_data['server_path'] and not self.cleaned_data['disk_file'])
    #     #         or (not self.cleaned_data['server_path'] and self.cleaned_data['disk_file'])):
    #
    #     # raise ValidationError({'pub_date': _('Draft entries may not have a publication date.')})
    #
    #
    #     raise forms.ValidationError({'server_path': ('Error')})

    # return self.cleaned_data

class Login(forms.Form):
    login = forms.CharField(max_length=128)
    password = forms.CharField(max_length=128, widget=forms.PasswordInput)

