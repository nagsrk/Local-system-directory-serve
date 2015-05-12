from django import forms
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        abstract = True
        fields = ('username', 'email', 'password', 'IP_Address_1', 'IP_Address_2')
        exclude = ('username.help_text')
