from django.urls import path

from . import views
from .views import add_instrument

urlpatterns = [
    path('', views.index, name='index'),
    path('agregar/', add_instrument.as_view(), name='add_instrument'),
    path('<int:instrument_id>/opciones/', views.add_options, name='add_options'),
    path('opciones/ajax/<int:afirmation_id>/', views.add_options_modal, name='add_options_modal'),
    path('<int:instrument_id>/status/', views.change_status_instrument, name = 'change_status_instrument'),
]
