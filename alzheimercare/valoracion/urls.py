from django.urls import path

from .views import *

urlpatterns = [
    path('', index, name='valorations'),
    path('agregar/', AddValoration.as_view(), name='add_valoration'),
    path('editar/<int:valoracion_id>', UpdateValoration.as_view(), name='edit_valoration'),
    path('resultados/<int:pk>/', instruments_results, name='instruments_results'),
    path('resultados/<int:valoration_id>/<int:usuario_id>/', instruments_user_results, name="instruments_user_results"),
    path('resultados/detail/<int:result_id>/', detail_result, name='detail_result'),
    path('resultados/reporte/<int:result_id>/', create_report, name="create_report")
]