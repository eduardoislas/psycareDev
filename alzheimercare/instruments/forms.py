from django import forms
from django.forms import ModelForm, inlineformset_factory

from .models import Instrument, Afirmation, Option

class AfirmationForm(ModelForm):
    class Meta:
        model = Afirmation
        exclude = ()
        label = {
            'is_inverse': 'algo'
        }
    def __init__(self, *args, **kwargs):
        super(AfirmationForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control m-20'
            })

class OptionForm(ModelForm):
    class Meta:
        model = Option
        exclude = ()
    def __init__(self, *args, **kwargs):
        super(OptionForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })


AfirmationFormSet = inlineformset_factory(Instrument, Afirmation, form = AfirmationForm, extra = 1)