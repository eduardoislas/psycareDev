from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect, JsonResponse
from django.views.generic import CreateView
from django.urls import reverse_lazy, reverse
from django.db import transaction
from django.template.loader import render_to_string
from django.forms import inlineformset_factory, formset_factory
from django.core import serializers
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


from .models import Instrument, Afirmation, Option
from .forms import InstrumemtForm, AfirmationFormSet, OptionForm, AfirmationForm, OptionFormSet, AfirmationEditForm

# Create your views here.

def index(request):
    status = request.GET.get('status')
    if status == 'activo' or status == None:
        instruments_list = Instrument.objects.all().filter(status=True)
    elif status == 'inactivo':
        instruments_list = Instrument.objects.all().filter(status=False)
    else:
        instruments_list = Instrument.objects.all()
    context = {
        'instruments_list' : instruments_list
    }
    return render(request, 'instruments/index.html', context)

def add_options(request, instrument_id):
    instrument = get_object_or_404(Instrument, pk = instrument_id)
    return render(request, 'instruments/add_options.html', {'instrument' : instrument})

class add_instrument(CreateView):
    model = Instrument
    fields = ['name','description','status','is_complex']
    template_name = 'instruments/add_instrument.html'
    success_url = reverse_lazy('index')
    def get_context_data(self,**kwargs):
        data = super(add_instrument, self).get_context_data(**kwargs)
        if self.request.POST:
            data['afirmations'] = AfirmationFormSet(self.request.POST)
        else:
            data['afirmations'] = AfirmationFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        afirmations = context['afirmations']
        with transaction.atomic():
            self.object = form.save()
            if afirmations.is_valid():
                afirmations.instance = self.object
                afirmations.save()
        return super(add_instrument, self).form_valid(form)

def add_options_modal(request, afirmation_id):
    template = {}
    afirmation_obj = get_object_or_404(Afirmation, pk = afirmation_id)
    pk = afirmation_obj.instrument.id
    instrument_obj = get_object_or_404(Instrument, pk = pk)
    afirmations_list = Afirmation.objects.filter(instrument = pk)
    if request.is_ajax and request.method == 'POST':
        OptionFormSet = inlineformset_factory(Afirmation, Option, form = OptionForm, extra = 0)
        option_formset = OptionFormSet(request.POST)
        if option_formset.is_valid():
            if instrument_obj.is_complex:
                for form in option_formset:
                    if form.has_changed():
                        options = form.save(commit = False)
                        options.afirmation = afirmation_obj
                        options.save()
            else:
                for afirmation in afirmations_list:
                    for form in option_formset:
                        if form.has_changed():
                            o = Option(afirmation = afirmation, option = form.cleaned_data['option'], value = form.cleaned_data['value'])
                            o.save()
            template['is_valid'] = True
        else:
            template['is_valid'] = False
    else:
        OptionFormSet = inlineformset_factory(Afirmation, Option, form = OptionForm, extra = 5)
    template['data'] = render_to_string('instruments/modal_option.html', {'option_form': OptionFormSet, 'url_post':reverse('add_options_modal', kwargs = {'afirmation_id':afirmation_id})})
    return JsonResponse(template)

def change_status_instrument(request, instrument_id):
    instrument = get_object_or_404(Instrument, pk = instrument_id)
    if instrument.status:
        instrument.status = False
    else:
        instrument.status = True
    instrument.save()
    return HttpResponseRedirect('/instrumentos/')

def edit_instrument(request, instrument_id):
    if request.method == 'POST':
        instrumentForm = InstrumemtForm(request.POST)
        afirmationFormSet = formset_factory(AfirmationEditForm, extra=0)
        afirmationForm = afirmationFormSet(request.POST)
        if instrumentForm.is_valid() and afirmationForm.is_valid():
            instrumento = Instrument.objects.get(pk=instrument_id)
            instrumento.name = instrumentForm.cleaned_data['name']
            instrumento.description = instrumentForm.cleaned_data['description']
            instrumento.status = instrumentForm.cleaned_data['status']
            instrumento.save()
            for form in afirmationForm.forms:
                afirmation = Afirmation.objects.get(pk = form.cleaned_data['af_id'])
                afirmation.text = form.cleaned_data['text']
                afirmation.is_inverse = form.cleaned_data['is_inverse']
                afirmation.save()
                    
        return HttpResponseRedirect('/instrumentos/')
    else:
        instrument = get_object_or_404(Instrument, pk = instrument_id)
        instrument_form = InstrumemtForm(instance = instrument)
        afirmation_list = Afirmation.objects.filter(instrument=instrument)
        afirmation_form = formset_factory(AfirmationEditForm, extra=0)
        data = {
            'form-TOTAL_FORMS': afirmation_list.count(),
            'form-INITIAL_FORMS': '0',
        }
        for a in range(len(afirmation_list)):
            data['form-'+str(a)+'-af_id'] = afirmation_list[a].id
            data['form-'+str(a)+'-instrument'] = instrument_id
            data['form-'+str(a)+'-text'] = afirmation_list[a].text
            data['form-'+str(a)+'-is_inverse'] = afirmation_list[a].is_inverse
        afirmation_formset = afirmation_form(data)

    return render(request, 'instruments/edit_instrument.html', {
            'instrument_form':instrument_form,
            'afirmation_form':afirmation_formset,
        })

def edit_options(request, afirmation_id):
    template = {}
    afirmation_obj = get_object_or_404(Afirmation, pk = afirmation_id)
    pk = afirmation_obj.instrument.id
    instrument_obj = get_object_or_404(Instrument, pk = pk)
    afirmations_list = Afirmation.objects.filter(instrument = pk)
    if request.is_ajax and request.method == 'POST':
        OptionFormSet = inlineformset_factory(Afirmation, Option, form = OptionForm, extra = 0)
        option_formset = OptionFormSet(request.POST, instance = afirmation_obj)
        if option_formset.is_valid():
            if instrument_obj.is_complex:
                for form in option_formset:
                    if form.has_changed():
                        option = form.cleaned_data['id']
                        option.value = form.cleaned_data['value']
                        option.option = form.cleaned_data['option']
                        option.save()
            else:
                data = []
                for form in option_formset:
                    o = form.cleaned_data['id']
                    o.afirmation = afirmation_obj
                    o.option = form.cleaned_data['option']
                    o.value = form.cleaned_data['value']
                    data.append(o)
                for afirmation in afirmations_list:
                    option_list = Option.objects.filter(afirmation = afirmation)
                    for i in range(len(option_list)):
                        op = Option.objects.get(pk = option_list[i].id)
                        op.afirmation = afirmation
                        op.option = data[i].option
                        op.value = data[i].value
                        op.save()
            template['is_valid'] = True
        else:
            template['is_valid'] = False
    else:
        OptionFormSet = inlineformset_factory(Afirmation, Option, form = OptionForm, extra = 0)
        OptionFormSet = OptionFormSet(instance = afirmation_obj)
    template['data'] = render_to_string('instruments/edit_modal_option.html', {'option_form': OptionFormSet, 'url_post':reverse('edit_options_modal', kwargs = {'afirmation_id':afirmation_id})})
    return JsonResponse(template)