from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordChangeView
from django.utils.decorators import method_decorator


from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser

# Create your views here.

def index(request):
    if request.user.user_type == 'psicologo':
        users_list = CustomUser.objects.filter(user_type = 'cuidador')
    else:
        users_list = CustomUser.objects.filter(Q( user_type = 'cuidador') | Q( user_type = 'psicologo'))
    context = {
        'users_list' : users_list,
    }
    return render(request,'users/index.html', context)
    
class SignUp(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('users')
    template_name = 'signup.html'

class UpdateUser(UpdateView):
    model = CustomUser
    form_class = CustomUserChangeForm
    success_url = reverse_lazy('users')
    template_name = 'users/edit.html'
    pk_url_kwarg = 'user_pk'
    
class UpdatePasswordByUser(PasswordChangeView):
    model = CustomUser
    success_url = reverse_lazy('users')
    template_name = 'users/change_pass.html'
