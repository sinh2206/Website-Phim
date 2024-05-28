from django import forms
from django.contrib.auth.models import User

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

class UserPasswordChangeForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), label="New Password")

    class Meta:
        model = User
        fields = ['password']
