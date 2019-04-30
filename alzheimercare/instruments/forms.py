from django import forms
from django.forms import ModelForm, inlineformset_factory, Form

from .models import Instrument, Afirmation, Option
from users.models import CustomUser
from valoracion.models import Valoracion

class InstrumemtForm(ModelForm):
    class Meta:
        model = Instrument
        exclude = ()
    def __init__(self, *args, **kwargs):
        super(InstrumemtForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control m-20'
            })

class AfirmationForm(ModelForm):
    class Meta:
        model = Afirmation
        exclude = ()
        widgets = {'instrument': forms.HiddenInput()}
        
    def __init__(self, *args, **kwargs):
        super(AfirmationForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control m-20'
            })

class AfirmationEditForm(ModelForm):
    af_id = forms.IntegerField(required=True)
    class Meta:
        model = Afirmation
        exclude = ()
        widgets = {'instrument': forms.HiddenInput()}
        
    def __init__(self, *args, **kwargs):
        super(AfirmationEditForm, self).__init__(*args, **kwargs)
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

class CaregiverChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return '{firstname} {lastname}'.format(firstname = obj.first_name, lastname = obj.last_name)

class ValorationChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return '{name}'.format(name = obj.name)

class ResultsFilter(Form):
    caregivers = CaregiverChoiceField(queryset=CustomUser.objects.filter(user_type='cuidador'), required= False)
    valorations = ValorationChoiceField(queryset=Valoracion.objects.all(), required = False)
    def __init__(self, *args, **kwargs):
        super(ResultsFilter, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })




#Inline formsets
AfirmationFormSet = inlineformset_factory(Instrument, Afirmation, form = AfirmationForm, extra = 1)
OptionFormSet = inlineformset_factory(Afirmation, Option, form = OptionForm, extra = 0)