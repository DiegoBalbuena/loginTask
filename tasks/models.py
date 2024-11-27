from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils.timezone import now

class CustomUserManager(BaseUserManager):
    def create_user(self, correo_electronico, nombre_de_usuario, edad=0, password=None, **extra_fields):
        if not correo_electronico:
            raise ValueError("El usuario debe tener un correo electrónico")
        correo_electronico = self.normalize_email(correo_electronico)
        user = self.model(
            correo_electronico=correo_electronico,
            nombre_de_usuario=nombre_de_usuario,
            edad=edad,
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, correo_electronico, nombre_de_usuario, edad=0, password=None, **extra_fields):
        extra_fields.setdefault('es_superusuario', True)
        return self.create_user(correo_electronico, nombre_de_usuario, edad, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    nombre_de_usuario = models.CharField(max_length=150, unique=True)
    correo_electronico = models.EmailField(unique=True)
    edad = models.PositiveIntegerField(default=0)
    es_superusuario = models.BooleanField(default=False)
    es_personal = models.BooleanField(default=False)
    esta_activo = models.BooleanField(default=True)
    fecha_union = models.DateTimeField(auto_now_add=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'correo_electronico'
    REQUIRED_FIELDS = ['nombre_de_usuario', 'edad']

    def __str__(self):
        return self.correo_electronico
