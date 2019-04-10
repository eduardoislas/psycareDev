from django.urls import path

from . import views
from .views import add_instrument, add_options, add_options_modal, change_status_instrument, edit_instrument, edit_options, index, answer_instrument, instruments_results, detail_result

urlpatterns = [
    path('', index, name='index'),
    path('agregar/', add_instrument.as_view(), name='add_instrument'),
    path('<int:instrument_id>/opciones/', add_options, name='add_options'),
    path('opciones/ajax/<int:afirmation_id>/', add_options_modal, name='add_options_modal'),
    path('<int:instrument_id>/', change_status_instrument, name = 'change_status_instrument'),
    path('<int:instrument_id>/editar/', edit_instrument, name = 'edit_instrument'),
    path('opciones/ajax/editar/<int:afirmation_id>/', edit_options, name = 'edit_options_modal'),
    path('contestar/<int:instrument_id>', answer_instrument, name='answer_instrument'),
    path('resultados/', instruments_results, name='instruments_results'),
    path('resultados/<int:result_id>', detail_result, name='detail_result'),
]
