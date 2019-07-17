from django.db import models
from django.contrib.auth.models import AbstractUser


from interview.models import Caregiver

# Create your models here.

TIPO_USUARIO = (
    ('psicologo','Psicólogo'),
    ('cuidador','Cuidador'),
)

class CustomUser(AbstractUser):
    user_type = models.CharField(max_length=20, choices = TIPO_USUARIO)
    caregiver = models.OneToOneField(Caregiver, on_delete = models.CASCADE, null = True)
    
    def __str__(self):
        return self.email

    @property
    def get_full_name(self):
        return self.first_name+' '+self.last_name