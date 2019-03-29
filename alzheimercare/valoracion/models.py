from django.db import models
from datetime import datetime

# Create your models here.

class Valoracion(models.Model):
    name = models.CharField(max_length=50)
    begin_date = models.DateField(auto_now=False, auto_now_add=False)
    end_date = models.DateField(auto_now=False, auto_now_add=False)

    # def nombre
