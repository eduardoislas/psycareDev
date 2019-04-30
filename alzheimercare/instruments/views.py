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
from datetime import date


from .models import Instrument, Afirmation, Option, InstrumentAnswer, Answers
from .forms import InstrumemtForm, AfirmationFormSet, OptionForm, AfirmationForm, OptionFormSet, AfirmationEditForm, ResultsFilter
from alzheimercare.decorators import restricted_for_caregivers, restricted_for_caregivers_class, only_caregiver
from valoracion.models import Valoracion
from users.models import CustomUser

# Create your views here.

@login_required
def index(request):
    context = {}
    if request.user.user_type == 'cuidador':
        valoracion = [obj for obj in Valoracion.objects.all() if obj.is_in_lapse][0]
        instruments_list = Instrument.objects.filter(status = True)
        instrument_answered = InstrumentAnswer.objects.filter(user = request.user).filter(valoration = valoracion)
        context['instrument_answered'] = instrument_answered
    else:
        status = request.GET.get('status')
        if status == 'activo' or status == None:
            instruments_list = Instrument.objects.filter(status=True)
        elif status == 'inactivo':
            instruments_list = Instrument.objects.filter(status=False)
        else:
            instruments_list = Instrument.objects.all()
            
    context['instruments_list'] = instruments_list
    return render(request, 'instruments/index.html', context)

@login_required
@restricted_for_caregivers
def add_options(request, instrument_id):
    instrument = get_object_or_404(Instrument, pk = instrument_id)
    return render(request, 'instruments/add_options.html', {'instrument' : instrument})

@method_decorator(login_required, name='dispatch')
@method_decorator(restricted_for_caregivers_class, name='dispatch')
class add_instrument(CreateView):
    model = Instrument
    fields = ['name','description','instructions','status','is_complex']
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

@login_required
@restricted_for_caregivers
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

@login_required
@restricted_for_caregivers
def change_status_instrument(request, instrument_id):
    instrument = get_object_or_404(Instrument, pk = instrument_id)
    if instrument.status:
        instrument.status = False
    else:
        instrument.status = True
    instrument.save()
    return HttpResponseRedirect('/instrumentos/')

@login_required
@restricted_for_caregivers
def edit_instrument(request, instrument_id):
    if request.method == 'POST':
        instrumentForm = InstrumemtForm(request.POST)
        afirmationFormSet = formset_factory(AfirmationEditForm, extra=0)
        afirmationForm = afirmationFormSet(request.POST)
        if instrumentForm.is_valid() and afirmationForm.is_valid():
            instrumento = Instrument.objects.get(pk=instrument_id)
            instrumento.name = instrumentForm.cleaned_data['name']
            instrumento.description = instrumentForm.cleaned_data['description']
            instrumento.instructions = instrumentForm.cleaned_data['instructions']
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

@login_required
@restricted_for_caregivers
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

@login_required
@only_caregiver
def answer_instrument(request, instrument_id):
    context = {}
    valoracion = [obj for obj in Valoracion.objects.all() if obj.is_in_lapse][0]

    if request.method == 'POST':
        instrument = Instrument.objects.get(pk = request.POST.get('instrument_id'))
        instrument_answer = InstrumentAnswer.objects.create(instrument = instrument, valoration = valoracion, user = request.user, answer_date = date.today())
        afirmation_list = Afirmation.objects.filter(instrument = instrument.pk)
        for afirmation in afirmation_list:
            option = Option.objects.get(pk = request.POST.get('afirmation_'+str(afirmation.pk))) 
            Answers.objects.create(instrument_answer = instrument_answer, afirmation = afirmation, option = option)
        return HttpResponseRedirect('/instrumentos/')
    else:
        instrument = get_object_or_404(Instrument, pk = instrument_id)
        if InstrumentAnswer.objects.filter(instrument = instrument).filter(valoration = valoracion).filter(user = request.user).exists():
            return HttpResponse("Ya has contestado este instrumento")
        context['instrument'] = instrument
        context['valoracion'] = valoracion
    return render(request, 'instruments/answer_instrument.html', context)

@login_required
@restricted_for_caregivers
def instruments_results(request):
    context = {}
    if request.method == 'POST':
        filter_form = ResultsFilter(request.POST)
        if filter_form.is_valid():
            if filter_form.cleaned_data['caregivers'] is not None and filter_form.cleaned_data['valorations'] is not None:
                caregiver = CustomUser.objects.get(pk = filter_form.cleaned_data['caregivers'].id)
                valoration = Valoracion.objects.get(pk = filter_form.cleaned_data['valorations'].id)
                results = InstrumentAnswer.objects.filter(user = caregiver).filter(valoration = valoration)
            elif filter_form.cleaned_data['caregivers'] is None and filter_form.cleaned_data['valorations'] is None:
                results = InstrumentAnswer.objects.all()
            elif filter_form.cleaned_data['caregivers'] is None:
                valoration = Valoracion.objects.get(pk = filter_form.cleaned_data['valorations'].id)
                results = InstrumentAnswer.objects.filter(valoration = valoration)
            elif filter_form.cleaned_data['valorations'] is None:
                caregiver = CustomUser.objects.get(pk = filter_form.cleaned_data['caregivers'].id)
                results = InstrumentAnswer.objects.filter(user = caregiver)
    else:
        results = InstrumentAnswer.objects.all()

    form  = ResultsFilter()
    context['results_list'] = results
    context['form'] = form
    return render(request,'instruments/results.html', context)


@login_required
def detail_result(request, result_id):
    context = {}
    result = get_object_or_404(InstrumentAnswer, pk = result_id)
    context['result'] = result
    return render(request, 'instruments/detail_result.html', context)

@login_required
@restricted_for_caregivers
def preview_instruments(request, instrument_id):
    context = {}
    instrument = get_object_or_404(Instrument, pk = instrument_id)
    context['instrument'] = instrument
    return render(request, 'instruments/preview.html', context)