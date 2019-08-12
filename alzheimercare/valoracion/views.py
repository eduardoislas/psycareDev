from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, UpdateView
from django.urls import reverse_lazy
from datetime import date
from django.contrib.auth.decorators import login_required
from weasyprint import HTML
from django.views.decorators.cache import cache_page
from django.core.paginator import Paginator
from django.template.loader import render_to_string
from django.http import HttpResponse

import tempfile

from .models import Valoracion
from users.models import CustomUser
from instruments.models import InstrumentAnswer, Instrument
from alzheimercare.decorators import restricted_for_caregivers, restricted_for_caregivers_class, verify_same_user
from .forms import ValorationForm, ReportForm, ResultsFilter

@login_required
@restricted_for_caregivers
def index(request):
    valoration_list = Valoracion.objects.all()
    context = {
        'valoration_list' : valoration_list
    }
    return render(request,'valoracion/index.html', context)

@method_decorator(login_required, name='dispatch')
@method_decorator(restricted_for_caregivers_class, name='dispatch')
class AddValoration(CreateView):
    form_class = ValorationForm
    success_url = reverse_lazy('valorations')
    template_name = 'valoracion/add_valoration.html'

@method_decorator(login_required, name='dispatch')
@method_decorator(restricted_for_caregivers_class, name='dispatch')
class UpdateValoration(UpdateView):
    model = Valoracion
    form_class = ValorationForm
    success_url = reverse_lazy('valorations')
    template_name = 'valoracion/edit_valoracion.html'
    pk_url_kwarg = 'valoracion_id'


@login_required
@restricted_for_caregivers
def instruments_results(request, pk):
    context = {}
    results = InstrumentAnswer.objects.filter(valoration = pk)
    caregivers = []
    for result in results:
        if not result.user in caregivers:
            caregivers.append(result.user)
    paginator = Paginator(caregivers, 10)
    page = request.GET.get('page')
    results_list = paginator.get_page(page)
    context['results_list'] = results_list
    context['valoration'] = get_object_or_404(Valoracion, pk = pk)
    return render(request,'valoracion/results.html', context)

@cache_page(60 * 480)
@login_required
@restricted_for_caregivers
def instruments_user_results(request, valoration_id, usuario_id):
    context = {}
    context['results'] = InstrumentAnswer.objects.filter(valoration = valoration_id, user = usuario_id)
    context['single_result'] = context['results'].first()
    context['valoration'] = get_object_or_404(Valoracion, pk = valoration_id)
    context['usuario'] = get_object_or_404(CustomUser, pk = usuario_id)
    context['total_instruments'] = len(Instrument.objects.filter(status = True))
    context['total_results'] = len(context['results'])
    return render(request, 'valoracion/user_results.html', context)

@login_required
def detail_result(request, result_id):
    context = {}
    result = get_object_or_404(InstrumentAnswer, pk = result_id)
    context['result'] = result
    return render(request, 'valoracion/detail_result.html', context)


@cache_page(60 * 480)
@login_required
@restricted_for_caregivers
def create_report(request, result_id):
    context = {}
    result = InstrumentAnswer.objects.get(pk = result_id)
    list_results = InstrumentAnswer.objects.filter(user = result.user).filter(valoration = result.valoration)

    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            report_context = {}
            # Data
            report_context['result'] = result
            report_context['list_results'] = list_results
            report_context['conclusion'] = form.cleaned_data['conclusion']
            report_context['date'] = date.today()
            report_context['intervention'] = form.cleaned_data['intervention']
            report_context['education'] = form.cleaned_data['education']
            report_context['orientation'] = form.cleaned_data['orientation']
            report_context['group'] = form.cleaned_data['group']

            # Render
            html_string = render_to_string('valoracion/pdf_template.html', report_context)
            html = HTML(string = html_string)
            result = html.write_pdf()
            #Response
            response = HttpResponse(content_type = 'application/pdf;')
            response['Content-Disposition'] = 'attachment; filename = reporte.pdf'
            response['Content-Transfer-Encoding'] = 'binary'
            with tempfile.NamedTemporaryFile(delete=True) as output:
                output.write(result)
                output.flush()
                output = open(output.name, 'rb')
                response.write(output.read())
            return response

    else:
        active_scales = result.instrument.instrumentrank_set.all()
        counter = 0
        for scale in active_scales:
            if scale.is_active and not scale.instrument.name == 'APGAR':
                counter = counter + 1
        if counter == 0 :
            conclusion = 'Mediante la exploración de '+ result.user.first_name +', presenta un riesgo bajo al ser cuidador principal; no presenta sobrecarga en el cuidado y se muestra estable en las escalas de valoración.</p><p>Se recomienda que asista a los grupos de apoyo que imparte el Centro de día, esto con la finalidad de seguir reforzando las habilidades que ha adquirido durante su formación como cuidador y continuar ofreciendo una calidad a su familiar, seguir fortaleciendo el vínculo que mantiene con sus familiares y estar evaluando mensualmente los roles en el cuidado, así mismo realizar tareas de esparcimiento social, con la finalidad de sacar del entorno en el que vive como cuidador. Por parte del área familiar del Centro de día se compromete a realizar sesiones mensuales para dar seguimiento tanto a la relación que mantiene con su familiar, así como a los resultados obtenidos estas valoraciones.'
        elif counter == 1:
            conclusion = 'Mediante la exploración de '+ result.user.first_name +', presenta un riesgo bajo al ser cuidador principal; no presenta sobrecarga en el cuidado y se muestra estable en las escalas de valoración, un indicador que se muestra activo es la depresión, sin embargo, es una emoción que comúnmente se ve activa en el rol como cuidador.</p><p>Se recomienda que asista a los grupos de apoyo que imparte el Centro de día, esto con la finalidad de seguir reforzando las habilidades que ha adquirido durante su formación como cuidador y continuar ofreciendo una calidad a su familiar, seguir fortaleciendo el vínculo que mantiene con sus hermanas y estar evaluando mensualmente los roles en el cuidado, así mismo realizar tareas de esparcimiento social, con la finalidad de sacar del entorno en el que vive como cuidador.</p><p>Por parte del área familiar del Centro de día se compromete a realizar sesiones mensuales para dar seguimiento tanto a la relación que mantiene con su familiar, así como a los resultados obtenidos estas valoraciones.'
        elif counter >= 2:
            conclusion = 'Mediante la exploración de '+ result.user.first_name +', presenta un riesgo moderado al ser cuidadora principal; no presenta una sobrecarga en el cuidado, sin embargo, '+ result.user.first_name +' no percibe un apoyo en el cuidado del adulto, otras escalas que se muestran activas son las de depresión y ansiedad, es importante comentar que aún no representan un problema como tal para el cuidador, pero ya son señales de alarma para su salud emocional. Se recomienda iniciar un proceso de psicoterapia, ya que, las escalas activas en las valoraciones de mayo aumentaron (depresión y ansiedad).</p><p>Con la finalidad de promover una mayor calidad de vida en el cuidador principal se hace la recomendación de iniciar un proceso terapéutico para dar el seguimiento adecuado a los indicadores de depresión y ansiedad que se encuentra activos en su tarea como cuidador. Por parte del área familiar del Centro de día se compromete a realizar sesiones mensuales para dar seguimiento tanto a la relación que mantiene con su familiar, así como a los resultados obtenidos estas valoraciones.</p><p>Continuar activa en los grupos de apoyo que el Centro de día ofrece a cuidadores y sus familiares.'
        data = {
            'conclusion': conclusion
        }
        form = ReportForm(initial = data)
    context['form'] = form
    context['result'] = result
    return render(request, 'valoracion/report_form.html', context)
