from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.db.models import Q, Prefetch, F, Avg,Max,Min,Count
from django.views.defaults import page_not_found
from django.contrib import messages
from datetime import datetime
from django.contrib.auth import login
from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth.models import Group


def my_error_404(request,exception=None):
    return render(request, 'errores/404.html',None,None,404)

def my_error_400(request,exception=None):
    return render(request, 'errores/400.html',None,None,400)

def my_error_403(request,exception=None):
    return render(request, 'errores/403.html',None,None,403)

def my_error_500(request,exception=None):
    return render(request, 'errores/500.html',None,None,500)

def index(request):
    
    if request.user.is_authenticated:
    
        if(not "fecha_inicio" in request.session):
            request.session["fecha_inicio"] = datetime.now().strftime('%d/%m/%Y %H:%M')
        
        if (not 'welcome_message1' in request.session):
            frase = "Bienvenid@, "
            request.session['welcome_message1'] = frase
        
        if (not 'usuario' in request.session):
            request.session['usuario'] = request.user.username
        
    
    return render(request, 'app/index.html', {})