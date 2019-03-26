from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

TIPO_USUARIO = (
    ('psicologo','Psicólogo'),
    ('cuidador','Cuidador'),
)

class CustomUser(AbstractUser):
    user_type = models.CharField(max_length=20, choices = TIPO_USUARIO)
    def __str__(self):
        return self.email