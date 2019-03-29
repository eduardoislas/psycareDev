from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, UpdateView
from django.urls import reverse_lazy


from .models import Valoracion
from alzheimercare.decorators import restricted_for_caregivers, restricted_for_caregivers_class, verify_same_user
from .forms import ValorationForm


def index(request):
    valoration_list = Valoracion.objects.all()
    context = {
        'valoration_list' : valoration_list
    }
    return render(request,'valoracion/index.html', context)

@method_decorator(restricted_for_caregivers_class, name='dispatch')
class AddValoration(CreateView):
    form_class = ValorationForm
    success_url = reverse_lazy('valorations')
    template_name = 'valoracion/add_valoration.html'

@method_decorator(restricted_for_caregivers_class, name='dispatch')
class UpdateValoration(UpdateView):
    model = Valoracion
    form_class = ValorationForm
    success_url = reverse_lazy('valorations')
    template_name = 'valoracion/edit_valoracion.html'
    pk_url_kwarg = 'valoracion_id'