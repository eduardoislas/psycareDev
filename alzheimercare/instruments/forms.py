from django import forms
from django.forms import ModelForm, inlineformset_factory


from .models import Instrument, Afirmation, Option, InstrumentRank
from users.models import CustomUser
from valoracion.models import Valoracion

TRUE_FALSE_CHOICES = (
    (True, 'Si'),
    (False, 'No')
)
SEVERITY_CHOICES = (
    (1, 'Baja'),
    (2, 'Media'),
    (3, 'Alta')
)
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

class RankForm(ModelForm):
    is_active = forms.ChoiceField(
        choices = TRUE_FALSE_CHOICES, 
        initial = '',
        widget = forms.Select(),
        required = True,
    )
    severity = forms.ChoiceField(
        choices = SEVERITY_CHOICES,
        initial = '',
        widget = forms.Select(),
        required = True,
    )

    class Meta:
        model = InstrumentRank
        exclude = ['instrument']
        
    
    def __init__(self, *args, **kwargs):
        super(RankForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

class RankEditForm(ModelForm):
    rank_id = forms.IntegerField(required=True)
    
    is_active = forms.ChoiceField(
        choices = TRUE_FALSE_CHOICES, 
        initial = '',
        widget = forms.Select(),
        required = True,
    )
    severity = forms.ChoiceField(
        choices = SEVERITY_CHOICES,
        initial = '',
        widget = forms.Select(),
        required = True,
    )
    class Meta:
        model = InstrumentRank
        exclude = ['instrument']
    
    def __init__(self, *args, **kwargs):
        super(RankEditForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })



#Inline formsets
AfirmationFormSet = inlineformset_factory(Instrument, Afirmation, form = AfirmationForm, extra = 1)
OptionFormSet = inlineformset_factory(Afirmation, Option, form = OptionForm, extra = 0)