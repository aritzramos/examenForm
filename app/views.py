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

# =============================================
# Registrar Investigador
# =============================================

def registrar_investigador(request):
    if request.method == 'POST':
        formulario = UsuarioFormInvestigador(request.POST)
        if formulario.is_valid():
            usuario = formulario.save()
            grupo = Group.objects.get(name='Investigadores')
            grupo.user_set.add(usuario)
            user = Investigador.objects.create( usuario = usuario)
            user.save()
            
                
            login(request, usuario)
            return redirect('index')
    else:
        formulario = UsuarioFormInvestigador()
    return render(request, 'registration/Psignup.html', {'formulario': formulario})

# =============================================
# Seleccion de registro
# =============================================

def seleccion(request):
    return render(request, 'registration/seleccion.html', {})




# =============================================
# Registrar Paciente
# =============================================

def registrar_paciente(request):
    if request.method == 'POST':
        formulario = UsuarioFormPaciente(request.POST)
        if formulario.is_valid():
            usuario = formulario.save()
            grupo = Group.objects.get(name='Pacientes')
            grupo.user_set.add(usuario)
            user = Paciente.objects.create( usuario = usuario)
            user.save()
            
                
            login(request, usuario)
            return redirect('index')
    else:
        formulario = UsuarioFormPaciente()
    return render(request, 'registration/Psignup.html', {'formulario': formulario})




def ensayo_lista(request):
    ensayos = EnsayoClinico.objects.all()
    return render(request, 'ensayoClinico/lista.html', {'ensayo': ensayos})

def ensayo(request, ensayo):
    ensayo_clinico = EnsayoClinico.objects.get(id=ensayo)
    return render(request, 'ensayoClinico/ensayo.html', {'ensayo': ensayo_clinico})

@login_required
@permission_required('app.add_ensayo')
def crear_ensayo(request):
    if request.method == 'POST':
        form = EnsayoClinicoForm(request.POST)
        if form.is_valid():
            nuevo_ensayo = form.save()
            investigador = Investigador.objects.get(usuario=request.user)
            nuevo_ensayo.creado_por = investigador
            nuevo_ensayo.save()
            form.save_m2m()  # Guardar las relaciones ManyToMany
            return redirect('lista')
    else:
        form = EnsayoClinicoForm()
    
    return render(request, 'ensayoClinico/crear_ensayo.html', {'form': form})

@login_required
@permission_required('app.delete_ensayo')
def eliminar(ensayo_id):
    ensayo = EnsayoClinico.objects.get(id=ensayo_id)
    try:
        ensayo.delete()
    except:
        pass
    return redirect('lista')
