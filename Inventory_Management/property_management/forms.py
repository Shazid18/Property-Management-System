from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class PropertyOwnerSignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Enter your first name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Enter your last name'}),
            'username': forms.TextInput(attrs={'placeholder': 'Enter your username'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Enter your email address'}),
            'password1': forms.PasswordInput(attrs={'placeholder': 'Enter your password'}),
            'password2': forms.PasswordInput(attrs={'placeholder': 'Confirm your password'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove help texts
        for field_name in ['username', 'password1', 'password2']:
            if self.fields[field_name].help_text:
                self.fields[field_name].help_text = ''
        # Remove labels
        # for field_name in self.fields:
        #     self.fields[field_name].label = ''
