from django import forms
from django.db.models import fields
from web.models import RRUser
from .models import *
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField

User = get_user_model()
competitions = Competition.objects.filter(is_open=True)
COMP_CHOICES = [('x', 'Select Competition')]

for i in range(len(competitions)):
    COMP_CHOICES.append((str(i), competitions[i].title))

class ContenderRegistrationForm(forms.Form):
    
    competition = forms.ModelChoiceField(label="Competiton", queryset=Competition.objects.all(), widget=forms.Select(attrs={'class':'form-select', 'name':'comprtition'}))
    smule_name = forms.CharField(label='Smule Name', widget=forms.TextInput(attrs={'class':'form-control', 'name':'smule-name'}))
    line_name = forms.CharField(label='Line Name', widget=forms.TextInput(attrs={'class':'form-control', 'name':'line-name'}))
    image = forms.FileField(label='Photo', widget=forms.FileInput(attrs={'class':'form-control', 'name':'image'}))

class UserRegistrationForm(forms.ModelForm):
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput(attrs={'class':'form-control'}))
    
    class Meta:
        model = RRUser
        fields = ['email', 'password']
        widgets = {
            'email':forms.TextInput(attrs={'class':'form-control'}),
            'password':forms.PasswordInput(attrs={'class':'form-control', 'type':'password'}),
            'password2':forms.PasswordInput(attrs={'class':'form-control', 'type':'password'})
        }
        labels = {
            'email':'Email',
            'password':'Password',
            'password2':'Confirm Password'
        }

        def clean_email(self):
            email = self.cleaned_data.get('email')
            qs = User.objects.filter(email=email)
            if qs.exits():
                raise forms.ValidationError("email is taken")
            return email

        def clean(self):
            cleaned_data = super().clean()
            password = cleaned_data.get('password')
            password2 = cleaned_data.get('password2')
            if password2 is not None and password != password2:
                self.add_error('password2', 'Your passwords must match')
            return cleaned_data

class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['link']
        widgets = {
            'link':forms.URLInput(attrs={'class':'form-control'})
        }
    comps = forms.ChoiceField(label="Competitons", choices=COMP_CHOICES, widget=forms.Select(attrs={'class':'form-control'}))
    