from django import forms
from django.contrib.auth import authenticate
from .models import CustomUser

# Formulario para registrar un nuevo usuario
class CustomUserCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['nombre_de_usuario', 'correo_electronico', 'edad', 'password']

    def clean_password(self):
        password = self.cleaned_data.get("password")
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
