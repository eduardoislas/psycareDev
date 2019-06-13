from django.db import models

from valoracion.models import Valoracion
from users.models import CustomUser

# Gestionar instrumentos

class Instrument(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=300, blank=True, null=True)
    instructions = models.TextField(max_length=400, blank=True, null=True)
    status = models.BooleanField(default=True)
    is_complex = models.BooleanField(default=False)
    class Meta:
        ordering = ['name']

class Afirmation(models.Model):
    instrument = models.ForeignKey(Instrument, on_delete=models.CASCADE)
    text = models.CharField(max_length=250)
    is_inverse = models.BooleanField(default=False)

class Option(models.Model):
    afirmation = models.ForeignKey(Afirmation, on_delete=models.CASCADE)
    option = models.CharField(max_length=50)
    value = models.IntegerField()


# Constestar instrumentos

class InstrumentAnswer(models.Model):
    instrument = models.ForeignKey(Instrument, related_name='answers',on_delete=models.CASCADE)
    valoration = models.ForeignKey(Valoracion, related_name='valoration', on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, related_name='usuario', on_delete=models.CASCADE)
    answer_date = models.DateField(auto_now=False, auto_now_add=False)

class Answers(models.Model):
    instrument_answer = models.ForeignKey(InstrumentAnswer, on_delete=models.CASCADE)
    afirmation = models.ForeignKey(Afirmation, on_delete=models.CASCADE)
    option = models.ForeignKey(Option, on_delete=models.CASCADE)

#Rangos calificacion instrumentos

class InstrumentRank(models.Model):
    instrument = models.ForeignKey(Instrument, on_delete = models.CASCADE)
    min_points = models.IntegerField()
    max_points = models.IntegerField()
    rank = models.CharField(max_length = 50)
    is_active = models.BooleanField(null = True)
    severity = models.IntegerField(null = True)



