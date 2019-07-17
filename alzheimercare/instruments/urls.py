from django.urls import path

from instruments.views import *

urlpatterns = [
    path('', index, name='index'),
    path('agregar/', add_instrument.as_view(), name='add_instrument'),
    path('<int:instrument_id>/opciones/', add_options, name='add_options'),
    path('opciones/ajax/<int:afirmation_id>/', add_options_modal, name='add_options_modal'),
    path('<int:instrument_id>/', change_status_instrument, name = 'change_status_instrument'),
    path('<int:instrument_id>/editar/', edit_instrument, name = 'edit_instrument'),
    path('opciones/ajax/editar/<int:afirmation_id>/', edit_options, name = 'edit_options_modal'),
    path('contestar/<int:instrument_id>/', answer_instrument, name='answer_instrument'),
    path('preview/<int:instrument_id>/', preview_instruments, name='preview_instruments'),
    path('<int:instrument_id>/rangos/', add_rank, name="add_ranks"),
    path('<int:instrument_id>/rangos/edit/', edit_rank, name="edit_ranks"),

]
