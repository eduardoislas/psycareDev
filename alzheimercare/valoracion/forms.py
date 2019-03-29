from django import forms
from django.forms import ModelForm

from .models import Valoracion

class DateInput(forms.DateInput):
    input_type = 'date'

class ValorationForm(ModelForm):
    class Meta:
        model = Valoracion
        exclude = ()
        widgets = {
            'begin_date': DateInput(),
            'end_date': DateInput(),
        }
    def __init__(self, *args, **kwargs):
        super(ValorationForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control m-20'
            })