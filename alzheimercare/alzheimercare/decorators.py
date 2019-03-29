from django.shortcuts import get_object_or_404
from users.models import CustomUser
from django.http import HttpResponseForbidden
from django.db.models import Q

# No access to caregivers
def restricted_for_caregivers(function):
    def wrap(request, *args, **kwargs):
        user = get_object_or_404(CustomUser,pk=request.user.pk)
        if user.user_type == 'cuidador':
            return HttpResponseForbidden()
        else:
            return function(request, *args, **kwargs)
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    wrap.__module__ = function.__module__
    return wrap


# No access to caregivers
def restricted_for_caregivers_class(function):
    def wrap(request, *args, **kwargs):
        user = get_object_or_404(CustomUser,pk=request.user.pk)
        if user.user_type == 'cuidador':
            return HttpResponseForbidden()
        else:
            return function(request, *args, **kwargs)
    return wrap


def verify_same_user(function):
    def wrap(request, *args, **kwargs):
        user = request.user
        pk_user = kwargs.pop('user_pk')
        if Q(user.is_superuser) | Q(user.user_type == "psicologo"):
            return function(request, *args, **kwargs)
        elif user.id == pk_user:
            return function(request, *args, **kwargs)
        else:
            return HttpResponseForbidden()
    return wrap