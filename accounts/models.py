from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class MyAccountManager(BaseUserManager):
    def create_user(self, first_name, last_name, username, email, password=None):
        if not email:
            raise ValueError('el usuario debe tener un email')

        if not username:
            raise ValueError('el usuario debe tener un nombre')

        user = self.model(
            email = self.normalize_email(email),
            username = username,
            first_name = first_name,
            last_name = last_name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, first_name, last_name, username, email, password):
        user= self.create_superuser(
            email = self.normalize_email(email),
            username = username,
            password = password,
            first_name = first_name,
            last_name = last_name,
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user

class Account(AbstractBaseUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True) # para que sea unico
    email = models.CharField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=50)
    
    #campos atributos de django
    date_joined = models.DateTimeField(auto_now_add=True) # fecha de creacion del usuario
    last_login = models.DateTimeField(auto_now_add=True) # ultima ves que el usuario estuvo online
    is_admin = models.BooleanField(default=False) # para saber si es un admin
    is_staff = models.BooleanField(default=False) # para saber si es un staff
    is_active = models.BooleanField(default=False) # para saber si esta activo
    is_superadmin = models.BooleanField(default=False) # para saber si es un superadmin
    
    USERNAME_FIELD = 'email' # que el parametro del login sea el email
    # REQUIRED_FIELD = ['username', 'first_name', 'last_name'] # datos requeridos obligatorios
    
    objects = MyAccountManager()
    
    def __str__(self): # en admin para que se registre un label
        return self.email
    
    def has_perm(self, perm, obj=None): # si tiene permiso a admin
        return self.is_admin
    
    def has_module_perms(self, add_label): # si es admin para que tenga permiso a los modulos
        return True
# Create your models here.
