from django.urls import path

from .views import index, AddValoration, UpdateValoration

urlpatterns = [
    path('', index, name='valorations'),
    path('agregar/', AddValoration.as_view(), name='add_valoration'),
    path('editar/<int:valoracion_id>', UpdateValoration.as_view(), name='edit_valoration'),
]