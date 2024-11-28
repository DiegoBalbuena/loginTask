from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

# Formulario para registrar un nuevo usuario
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'age', 'password1', 'password2']
        
    def clean_password(self):
        password = self.cleaned_data.get("password1")
        if len(password) < 6:
            raise forms.ValidationError("La contraseña debe tener al menos 6 caracteres.")
        return password

# Formulario de inicio de sesión
class LoginForm(forms.Form):
    correo_electronico = forms.EmailField(label="Correo electrónico")
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        correo_electronico = self.cleaned_data.get("correo_electronico")
        password = self.cleaned_data.get("password")
        user = authenticate(correo_electronico=correo_electronico, password=password)
        if user is None:
            raise forms.ValidationError("Correo electrónico o contraseña incorrectos.")
        return self.cleaned_data

class TaskCreationForm(forms.Form):
    title = forms.CharField(label='Título', max_length=255)  
    content = forms.CharField(label='Contenido', widget=forms.Textarea())  

class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'age', 'password']
        labels = {
            'username': 'Nombre de usuario',
            'email': 'Correo electrónico',
            'age': 'Edad',
        }
        widgets = {
            'password': forms.PasswordInput(),
        }
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError("Las contraseñas no coinciden")
        return cleaned_data
        
from django.contrib.auth.forms import AuthenticationForm

class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Correo Electrónico', max_length=100)
    password = forms.CharField(widget=forms.PasswordInput())

