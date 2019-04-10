from django.db import models
from datetime import date

# Create your models here.

class Valoracion(models.Model):
    name = models.CharField(max_length=50)
    begin_date = models.DateField(auto_now=False, auto_now_add=False)
    end_date = models.DateField(auto_now=False, auto_now_add=False)

    @property
    def is_in_lapse(self):
        if date.today() >= self.begin_date and date.today() <= self.end_date:
            return True
        return False