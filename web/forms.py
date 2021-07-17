from django import forms
from django.contrib.auth import get_user_model
from django.forms.widgets import PasswordInput, TextInput
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()

class UserRegistrationForm(UserCreationForm):
    # email = forms.EmailField(label='Email', widget=TextInput(attrs={'class':'form-control'}))
    # password1 = forms.CharField(label='Password', widget=PasswordInput(attrs={'class':'form-control'}))
    # password2 = forms.CharField(label='Confirm Password', widget=PasswordInput(attrs={'class':'form-control'}))

    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']
        widgets = {
            'email':forms.EmailInput(attrs={'class':'form-control'}),
            'password1':forms.TextInput(attrs={'class':'form-control'}),
            'password2':forms.TextInput(attrs={'class':'form-control'})
        }

    # def clean_email(self):
    #     email = self.cleaned_data.get('email')
    #     password = self.cleaned_data.get('password')
    #     password2 = self.cleaned_data.get('password2')
    #     email_qs = User.objects.filter(email=email)
    #     if email_qs:
    #         raise forms.ValidationError('Email already registered!')
    #     if password != password2:
    #         raise forms.ValidationError("Passwords didn't mathced")
    #     return email

