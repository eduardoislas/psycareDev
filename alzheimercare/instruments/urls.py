from django.urls import path

from . import views
from .views import add_instrument, add_options, add_options_modal, change_status_instrument, edit_instrument, edit_options, index

urlpatterns = [
    path('', index, name='index'),
    path('agregar/', add_instrument.as_view(), name='add_instrument'),
    path('<int:instrument_id>/opciones/', add_options, name='add_options'),
    path('opciones/ajax/<int:afirmation_id>/', add_options_modal, name='add_options_modal'),
    path('<int:instrument_id>/', change_status_instrument, name = 'change_status_instrument'),
    path('<int:instrument_id>/editar/', edit_instrument, name = 'edit_instrument'),
    path('opciones/ajax/editar/<int:afirmation_id>/', edit_options, name = 'edit_options_modal'),
]
