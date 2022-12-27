from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms  

class CreateUserForm(UserCreationForm):
    username = forms.CharField(widget = forms.TextInput(attrs={ 'class':'Register__div__input',
                                                                'placeholder':' ',
                                                                'type':'login'}),label="Login",
                                                                min_length=5, max_length=150, )  

    
    password1 = forms.CharField(widget = forms.TextInput(attrs={'class':'Register__div__input',
                                                                'placeholder':' ',
                                                                'type':'password'}),label="Hasło")
      
    password2 = forms.CharField(widget = forms.TextInput(attrs={'class':'Register__div__input',
                                                                'placeholder':' ',
                                                                'type':'password'}),label="Powtórz hasło") 
    
    email = forms.EmailField(widget = forms.EmailInput(attrs={'class':'Register__div__input',
                                                              'placeholder':' '}),label="Email")
    
    first_name = forms.CharField(widget= forms.TextInput(attrs={'class':'Register__div__input',
                                                                'placeholder':' '}),required=False,label="Imię")
    
    last_name = forms.CharField(widget= forms.TextInput(attrs={'class':'Register__div__input',
                                                               'placeholder':' '}),required=False,label="Nazwisko")
    
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Użytkowniek już istnieje") 
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
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'autofocus': False})