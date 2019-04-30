from django.urls import path
from .views import SignUp, index, UpdateUser, UpdatePasswordByUser, change_status

urlpatterns = [
    path('', index, name='users'),
    path('registro/', SignUp, name='signup'),
    path('editar/<int:user_pk>/', UpdateUser.as_view(), name='edit_user'),
    path('password/<int:user_pk>/', UpdatePasswordByUser.as_view(), name='edit_password'),
    path('estatus/<int:user_pk>/', change_status, name='change_user_status'),
]