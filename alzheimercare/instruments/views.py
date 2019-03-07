from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect, JsonResponse
from django.views.generic import CreateView
from django.urls import reverse_lazy, reverse
from django.db import transaction
from django.template.loader import render_to_string
from django.forms import inlineformset_factory

from .models import Instrument, Afirmation, Option
from .forms import AfirmationFormSet, OptionForm

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

