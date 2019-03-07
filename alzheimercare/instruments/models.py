from django.db import models

# Create your models here.

class Instrument(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=300, blank=True, null=True)
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
