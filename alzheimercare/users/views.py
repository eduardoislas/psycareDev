# -*- coding: utf-8 -*-

from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.views import PasswordChangeView
from django.utils.decorators import method_decorator
from django.http import HttpResponseRedirect, JsonResponse
from django.core.mail import send_mail


from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser
from interview.models import Caregiver
from alzheimercare.decorators import restricted_for_caregivers, restricted_for_caregivers_class, verify_same_user

# Create your views here.
@login_required
@restricted_for_caregivers
def index(request):
    status = request.GET.get('status')
    if request.user.user_type == 'psicologo':
        if status == 'activo' or status == None:
            users_list = CustomUser.objects.filter(user_type = 'cuidador').filter(is_active = True)
        elif status == 'inactivo':
            users_list = CustomUser.objects.filter(user_type = 'cuidador').filter(is_active = False)
        else:
            users_list = CustomUser.objects.filter(user_type = 'cuidador')
    else:
        if status == 'activo' or status == None:
            users_list = CustomUser.objects.filter(Q( user_type = 'cuidador') | Q( user_type = 'psicologo')).filter(is_active = True)
        elif status == 'inactivo':
            users_list = CustomUser.objects.filter(Q( user_type = 'cuidador') | Q( user_type = 'psicologo')).filter(is_active = False)
        else:
            users_list = CustomUser.objects.filter(Q( user_type = 'cuidador') | Q( user_type = 'psicologo'))
    context = {
        'users_list' : users_list,
    }
    return render(request,'users/index.html', context)

# @method_decorator(login_required, name="dispatch")
# @method_decorator(restricted_for_caregivers_class, name='dispatch')
# class SignUp(CreateView):
#     form_class = CustomUserCreationForm
#     success_url = reverse_lazy('users')
#     template_name = 'signup.html'

@login_required
@restricted_for_caregivers
def SignUp(request):
    context = {}
    if request.method == 'POST':
        user_form = CustomUserCreationForm(request.POST)
        if user_form.is_valid():
            user = user_form.save(commit=False)
            body = 'Su cuenta ha sido registrada exitosamente, esta es su nueva contraseña: ' + user_form.cleaned_data['password1'] + ' y podrá cambiarla cuando entre a la plataforma.' 
            send_mail('Registro en la aplicación Alzcare', body, 'jesuslara97@gmail.com', [user_form.cleaned_data['email']])
            user.save()
        return HttpResponseRedirect('/usuarios/')    
    else:
        random_password = BaseUserManager().make_random_password()
        form =  CustomUserCreationForm(initial={
            'password1': random_password,
            'password2': random_password,
        })
        form.fields['password1'].widget.render_value = True
        form.fields['password2'].widget.render_value = True
        context['form'] = form
    return render(request,'signup.html', context)



@method_decorator(login_required, name="dispatch")
@method_decorator(verify_same_user, name="dispatch")
class UpdateUser(UpdateView):
    model = CustomUser
    form_class = CustomUserChangeForm
    success_url = reverse_lazy('dashboard')
    template_name = 'users/edit.html'
    pk_url_kwarg = 'user_pk'

@method_decorator(login_required, name="dispatch")
@method_decorator(verify_same_user, name="dispatch")
class UpdatePasswordByUser(PasswordChangeView):
    model = CustomUser
    success_url = reverse_lazy('dashboard')
    template_name = 'users/change_pass.html'

@login_required
@restricted_for_caregivers
def change_status(request, user_pk):
    user = get_object_or_404(CustomUser, pk = user_pk)
    if user.is_active:
        user.is_active = False
    else:
        user.is_active = True
    user.save()
    return HttpResponseRedirect('/usuarios/')

def get_caregiver_data(request):
    caregiver_id = request.GET.get('caregiver_id', None)
    caregiver = get_object_or_404(Caregiver, pk = caregiver_id)
    data = {
        'nombre': caregiver.first_name,
        'apellidos': caregiver.last_name,
        'correo': caregiver.email
    }
    return JsonResponse(data)
    
