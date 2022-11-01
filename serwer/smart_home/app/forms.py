from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms  
from django.core.exceptions import ValidationError  
from django.forms.fields import EmailField  



class CreateUserForm(UserCreationForm):
    username = forms.CharField(min_length=5, max_length=150, widget = forms.TextInput(attrs={'placeholder':'Login'}))  
    
    email = forms.EmailField(widget = forms.EmailInput(attrs={'placeholder':'Email'}))
    
    password1 = forms.CharField(widget = forms.TextInput(attrs={'placeholder':'Hasło',
                                                                'type':'password'}))
      
    password2 = forms.CharField(widget = forms.TextInput(attrs={'placeholder':'Powtórz hasło',
                                                                'type':'password'})) 
    
    first_name = forms.CharField(widget= forms.TextInput(attrs={'placeholder':'Imię'}),required=False)
    
    last_name = forms.CharField(widget= forms.TextInput(attrs={'placeholder':'Nazwisko'}),required=False)
    
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Urzytkowniek już istnieje") 
        return username
        
    
    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if len(password1) <8: 
            raise forms.ValidationError("Hasło jest za krótkie.") 
        return password1
    
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 != password2: 
            raise forms.ValidationError("Hasła nie są takie same.") 
        return password2

        
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Email jest już zajęty')
        return email