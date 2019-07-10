from django import forms
from django.forms import ModelForm

from .models import Interview, Adult, Context, Tutor, Caregiver, Process

class DateInput(forms.DateInput):
    input_type = 'date'

class TimeInput(forms.TimeInput):
    input_type = 'time'

class InterviewForm(ModelForm):
    class Meta:
        model =  Interview
        exclude = ()
        widgets = {
            'date': DateInput(format='%Y-%m-%d'),
            'begin_time': TimeInput(format='%H:%M'),
            'end_time': TimeInput(format='%H:%M'),
        }
    
    def __init__(self, *args, **kwargs):
        super(InterviewForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

class AdultForm(ModelForm):
    class Meta:
        model = Adult
        exclude = ()
        widgets = {
            'birth_date': DateInput(format='%Y-%m-%d'),
        }
    
    def __init__(self, *args, **kwargs):
        super(AdultForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

class ContextForm(ModelForm):
    class Meta:
        model = Context
        exclude = ()
        widgets = {
            'specification': forms.Textarea,
            'services': forms.Textarea,
            'actions': forms.Textarea,
        }
    
    def __init__(self, *args, **kwargs):
        super(ContextForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })
    
class TutorForm(ModelForm):
    class Meta:
        model = Tutor
        exclude = ()
        widgets = {
            'how': forms.Textarea,
            'responsibilities': forms.Textarea,
        }
    
    def __init__(self, *args, **kwargs):
        super(TutorForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

class CaregiverForm(ModelForm):
    class Meta:
        model = Caregiver
        exclude = ()
        widgets = {
            'birth_date': DateInput(format='%Y-%m-%d'),
        }

    def __init__(self, *args, **kwargs):
        super(CaregiverForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })


class ProcessForm(ModelForm):
    class Meta:
        model = Process
        exclude = ()

    def __init__(self, *args, **kwargs):
        super(ProcessForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })