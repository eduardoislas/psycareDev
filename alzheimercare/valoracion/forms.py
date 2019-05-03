from django import forms
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from datetime import date

from .models import Valoracion

class DateInput(forms.DateInput):
    input_type = 'date'

class ValorationForm(ModelForm):
    name = forms.CharField(required=False)

    class Meta:
        model = Valoracion
        fields = ['name','begin_date','end_date']
        widgets = {
            'begin_date': DateInput(format='%Y-%m-%d'),
            'end_date': DateInput(format='%Y-%m-%d'),
        }
    def __init__(self, *args, **kwargs):
        super(ValorationForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control m-20'
            })
    
    def clean(self):
        self.cleaned_data = super(ValorationForm, self).clean()

        print(self.instance.pk)
        months = {
            '01': 'Enero',
            '02': 'Febrero',
            '03': 'Marzo',
            '04': 'Abril',
            '05': 'Mayo',
            '06': 'Junio',
            '07': 'Julio',
            '08': 'Agosto',
            '09': 'Septiembre',
            '10': 'Octubre',
            '11': 'Noviembre',
            '12': 'Diciembre',
        }

        begin_date = self.cleaned_data.get('begin_date')
        end_date = self.cleaned_data.get('end_date')
        
        name =  months[begin_date.strftime('%m')] + ' - ' + months[end_date.strftime('%m')] + ' ' + begin_date.strftime('%Y')

        if begin_date is not None and end_date is not None:
            if end_date < date.today():
                self.add_error(None, ValidationError('La fecha final no puede ser anterior al dia de hoy'))
            elif not begin_date < end_date:
                self.add_error(None, ValidationError('La fecha inicial debe ser anterior a la fecha final'))
            else:
                if not self.instance.pk:
                    valorations = Valoracion.objects.all()
                else:
                    valorations = Valoracion.objects.exclude(pk = self.instance.pk)
                for valoration in valorations:
                    if begin_date >= valoration.begin_date and begin_date <= valoration.end_date:
                        self.add_error(None, ValidationError('Ya existe un periodo de valoración conformado con las fechas ingresadas.'))
        self.cleaned_data['name'] = name
        return self.cleaned_data
