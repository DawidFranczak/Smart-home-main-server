from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from .models import User, HomeNavImage
from django import forms  

class CreateUserForm(UserCreationForm):

    username = forms.CharField(
        widget = forms.TextInput(
            attrs={ 'class':'Register__div__input',
                   'placeholder':' ',
                   'type':'login'}),
        label="Login",
        min_length=5, 
        max_length=150)

    password1 = forms.CharField(
        widget = forms.TextInput(
            attrs={'class':'Register__div__input',
                   'placeholder':' ',
                   'type':'password'}),
        label="Hasło")
      
    password2 = forms.CharField(
        widget = forms.TextInput(
            attrs={'class':'Register__div__input',
                   'placeholder':' ',
                   'type':'password'}),
        label="Powtórz hasło") 
    
    email = forms.EmailField(
        widget = forms.EmailInput(
            attrs={'class':'Register__div__input',
                   'placeholder':' '}),
        label="Email")
    
    first_name = forms.CharField(
        widget= forms.TextInput(
            attrs={'class':'Register__div__input',
                   'placeholder':' '}),
        required=False,
        label="Imię")
    
    last_name = forms.CharField(
        widget= forms.TextInput(
            attrs={'class':'Register__div__input',
                   'placeholder':' '}),
        required=False,
        label="Nazwisko")
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'autofocus': False})
    
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
    
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'email', 'first_name', 'last_name']
    
        
class ChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(
        widget = forms.PasswordInput(
            attrs={'class':'Register__div__input'}),
        label="Podaj aktualne hasło")
    
    new_password1 = forms.CharField(
        widget = forms.PasswordInput(
            attrs={'class':'Register__div__input'}),
        label="Podaj nowe hasło")
    
    new_password2= forms.CharField(
        widget = forms.PasswordInput(
            attrs={'class':'Register__div__input'}),
        label="Powtórz nowe hasło")
    
    
    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password')
        
        if not self.user.check_password(old_password): 
            raise forms.ValidationError("Podane hsało jest nieprawidłowe.") 
        return old_password

    def clean_new_password1(self):
        new_password1 = self.cleaned_data.get('new_password1')
        if len(new_password1)<8: 
            raise forms.ValidationError("Hasło jest za krótkie.") 
        return new_password1
    
    def clean_new_password2(self):
        new_password1 = self.cleaned_data.get('new_password1')
        new_password2 = self.cleaned_data.get('new_password2')
        if new_password1 != new_password2: 
            raise forms.ValidationError("Hasła nie są takie same.") 
        return new_password2

    class Meta:
        model = User
        fields = ['old_password', 'new_password1', 'new_password2']
        
        
class ChangeEmailForm(forms.Form):
    
    new_email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={'class':'Email__div__input'}),
        label="Podaj nowego emaila"
        )
    
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)
        
    def clean_new_email(self):
        new_email = self.cleaned_data.get('new_email')
        if User.objects.filter(email = new_email).exists():
            raise forms.ValidationError('Adres email jest już zajęty')
        return new_email
        
    def save(self, commit=True):
        new_email = self.cleaned_data.get('new_email')
        user = User.objects.get(email = self.user.email)
        user.email = new_email
        if commit:
            user.save()
        return self.user
    
    class Meta:
        model = User
        fields = ['email']


class ChangeImageForm(forms.Form):
    home = forms.ImageField(label='Zdjęcie domku', required=False)
    rpl = forms.ImageField(label='Zdjęcie grupowania urządzeń', required=False)
    aquarium = forms.ImageField(label='Zdjęcie akwarium', required=False)
    sunblind = forms.ImageField(label='Zdjęcie rolet', required=False)
    temperature = forms.ImageField(label='Zdjęcie temperatury', required=False)
    profile = forms.ImageField(label='Zdjęcie ustawień', required=False)
    light = forms.ImageField(label='Zdjęcie światła', required=False)
    stairs = forms.ImageField(label='Zdjęcie schodów', required=False)
    sensor = forms.ImageField(label='Zdjęcie dodawania urządzeń', required=False)
    logout = forms.ImageField(label='Zdjęcie wylogowywania', required=False)
    
    IMAGES = ['home','rpl','aquarium','sunblind','temperature',
                  'profile','light','stairs','sensor','logout']
    
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)
        
    # def clean(self):
    #     for image in self.IMAGES:
    #         print(user_image.image)
    #         new_image = self.cleaned_data.get(image)
    #         if new_image is not None:
    #             pass
    
    def reset(self):
        user_image = HomeNavImage.objects.get(user_id=self.user.id)
        
        user_image.home = 'images/home.png'
        user_image.rpl = 'images/rfid.png'
        user_image.aquarium = 'images/aqua.png'
        user_image.sunblind = 'images/sunblind.png'
        user_image.temperature ='images/temp.png'
        user_image.profile = 'images/user.png'
        user_image.light = 'images/lamp.png'
        user_image.stairs = 'images/stairs.png'
        user_image.sensor = 'images/sensor.png'
        user_image.logout = 'images/logout.png'
        user_image.save()
        return self.user
    
    def save(self):
        user_image = HomeNavImage.objects.get(user_id=self.user.id)
        # for image in self.IMAGES:
        #     new_image = self.cleaned_data.get(image)
        #     if new_image is not None:
        #         user_image = new_image
        #         print('hehe')
        
        if self.cleaned_data.get('home') is not None:
            user_image.home = self.cleaned_data.get('home')
        if self.cleaned_data.get('rpl') is not None:
            user_image.rpl = self.cleaned_data.get('rpl')
        if self.cleaned_data.get('aquarium') is not None:
            user_image.aquarium = self.cleaned_data.get('aquarium')
        if self.cleaned_data.get('sunblind') is not None:
            user_image.sunblind = self.cleaned_data.get('sunblind')
        if self.cleaned_data.get('temperature') is not None:
            user_image.temperature = self.cleaned_data.get('temperature')
        if self.cleaned_data.get('profile') is not None:
            user_image.profile = self.cleaned_data.get('profile')
        if self.cleaned_data.get('light') is not None:
            user_image.light = self.cleaned_data.get('light')
        if self.cleaned_data.get('stairs') is not None:
            user_image.stairs = self.cleaned_data.get('stairs')
        if self.cleaned_data.get('sensor') is not None:
            user_image.sensor = self.cleaned_data.get('sensor')
        if self.cleaned_data.get('logout') is not None:
            user_image.logout = self.cleaned_data.get('logout')
            
        user_image.save()
        return self.user
        
    class Meta:
        model = HomeNavImage
        fields = '__all__'
        
        