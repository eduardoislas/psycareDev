from django.urls import path
from .views import SignUp,index,UpdateUser, UpdatePasswordByUser

urlpatterns = [
    path('', index, name='users'),
    path('registro/', SignUp.as_view(), name='signup'),
    path('editar/<int:user_pk>/', UpdateUser.as_view(), name="edit_user"),
    path('password/<int:user_pk>/', UpdatePasswordByUser.as_view(), name="edit_password"),
]