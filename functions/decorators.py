from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render
from django.http import Http404

def superuser_only(function):
    """Limit view to superusers only."""
    def _inner(request, *args, **kwargs):
        if not request.user.is_superuser:
            raise Http404("Strona nie istnieje")          
        return function(request, *args, **kwargs)
    return _inner


def staff_only(function):
    """Limit view to staff only."""
    def _inner(request, *args, **kwargs):
        if not request.user.is_staff:
            raise Http404("Strona nie istnieje")          
        return function(request, *args, **kwargs)
    return _inner


def login_only(function):
    """Limit view to all registred users."""
    def _inner(request, *args, **kwargs):
        if not request.user.is_active:
            return render(request, template_name='registration/only_for_login_users.html') 
        elif request.user.is_active:         
            return function(request, *args, **kwargs)
    return _inner



def if_logined_denied(function):
    """Limit view to anonymouse."""
    def _inner(request,*args,**kwargs):
        if not request.user.is_active:
            return function(request,*args,**kwargs)
        elif request.user:
            raise Http404("Strona nie istnieje")
    return _inner







   
