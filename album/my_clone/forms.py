from django import forms
from django.core.validators import *
from django.core.exceptions import *
from .models import *


class Login(forms.Form):
    login = forms.CharField(max_length=128)
    password = forms.CharField(max_length=128, widget=forms.PasswordInput)


class AddPhotoForm(forms.Form):
    server_path = forms.CharField(max_length=128, required=False)
    disk_file = forms.FileField(required=False)

    def clean(self):
        # if more or less than one was given (XOR)
        if not ((self.cleaned_data['server_path'] and
           not self.cleaned_data['disk_file'])

           or (not self.cleaned_data['server_path']
           and self.cleaned_data['disk_file'])):

            raise forms.ValidationError({'server_path': 'Fill only '
                                                        'one of fields'})

        return self.cleaned_data


class AddUserForm(forms.Form):
    # class-model User -> he's always watching :)
    # https://docs.djangoproject.com/en/1.11/ref/contrib/auth/
    # his fields:
    # username, first_name, last_name, email, password, groups
    # user_permissions, is_staff, is_active, is_superuser,
    # last_login, date_joined
    username = forms.CharField(label='User Login:', max_length=100)
    password = forms.CharField(label='Password:', max_length=100,
                               widget=forms.PasswordInput)
    password_retype = forms.CharField(label='Password Retype:', max_length=100,
                                      widget=forms.PasswordInput)
    # first_name = forms.CharField(label='Imie:', max_length=100)
    # last_name = forms.CharField(label='Nazwisko:', max_length=100)
    email = forms.CharField(label='Email:', max_length=100,
                            validators=[validate_email])


# class UpdateUserForm(forms.Form):
#     first_name = forms.CharField(label='First Name:', max_length=100)
#     last_name = forms.CharField(label='Last Name:', max_length=100)
#     email = forms.CharField(label='Email:', max_length=100,
#                             validators=[validate_email])


class ResetPasswordForm(forms.Form):
    password_old = forms.CharField(label='Old Password:', max_length=100,
                                   widget=forms.PasswordInput)
    password_new1 = forms.CharField(label='New Password:', max_length=100,
                                    widget=forms.PasswordInput)
    password_new2 = forms.CharField(label='New Password Retype:',
                                    max_length=100, widget=forms.PasswordInput)


