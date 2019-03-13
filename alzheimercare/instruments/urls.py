from django.urls import path

from . import views
from .views import add_instrument

urlpatterns = [
    path('', views.index, name='index'),
    path('agregar/', add_instrument.as_view(), name='add_instrument'),
    path('<int:instrument_id>/opciones/', views.add_options, name='add_options'),
    path('opciones/ajax/<int:afirmation_id>/', views.add_options_modal, name='add_options_modal'),
    path('<int:instrument_id>/', views.change_status_instrument, name = 'change_status_instrument'),
    path('<int:instrument_id>/editar/', views.edit_instrument, name = 'edit_instrument'),

    path('opciones/ajax/editar/<int:afirmation_id>/', views.edit_options, name = 'edit_options_modal'),
]
