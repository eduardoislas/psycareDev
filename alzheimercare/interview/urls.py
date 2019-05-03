from django.urls import path

from .views import index, add_interview, answer_interview, add_adult, add_context, add_tutor, add_caregiver, add_process

urlpatterns = [
    path('', index, name='interviews'),
    path('agregar/', add_interview, name='add_interview'),
    path('llenar/<int:interview_id>/', answer_interview, name='answer_interview'),
    path('llenar/<int:interview_id>/agregar_adulto', add_adult, name='add_adult'),
    path('llenar/<int:interview_id>/agregar_contexto', add_context, name='add_context'),
    path('llenar/<int:interview_id>/agregar_tutor', add_tutor, name='add_tutor'),
    path('llenar/<int:interview_id>/agregar_cuidador', add_caregiver, name='add_caregiver'),
    path('llenar/<int:interview_id>/agregar_proceso', add_process, name='add_process'),

]