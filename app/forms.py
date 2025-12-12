from django.forms import ModelForm
from django import forms
from .models import Usuario, EnsayoClinico, Farmaco, Investigador, Paciente
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone


class UsuarioFormPaciente(UserCreationForm):
    edad = forms.IntegerField(label='Edad')
    class Meta:
        model = Usuario

        fields = ['username', 'email', 'edad', 'password1', 'password2']
      

class UsuarioFormInvestigador(UserCreationForm):
    class Meta:
        model = Usuario

        fields = ['username', 'email', 'password1', 'password2']

# =============================================
# Formulario para crear y editar EnsayoClinico
# =============================================

class EnsayoClinicoForm(ModelForm):
    class Meta:
        model = EnsayoClinico
        fields = ['nombre', 
                  'descripcion', 
                  'farmaco', 
                  'pacientes', 
                  'nivel_seguimiento', 
                  'fecha_inicio', 
                  'fecha_fin', 
                  'activo']
        labels = {
            'nombre': 'Nombre del Ensayo Clínico',
            'descripcion': 'Descripción',
            'farmaco': 'Fármaco',
            'pacientes': 'Pacientes',
            'nivel_seguimiento': 'Nivel de Seguimiento',
            'fecha_inicio': 'Fecha de Inicio',
            'fecha_fin': 'Fecha de Fin',
            'activo': '¿Activo?'
        }
        
        widgets = {
            'descripcion': forms.Textarea(),
            'pacientes': forms.SelectMultiple(),
            'nivel_seguimiento': forms.NumberInput(attrs={'min': 0, 'max': 10}), #Controlamos el rango del nivel de seguimiento
            'fecha_inicio': forms.SelectDateWidget(years=range(2020,2026)),
            'fecha_fin': forms.SelectDateWidget(years=range(2020,2026))
        }
    def clean(self):
        super().clean()
        
        nombre = self.cleaned_data.get('nombre')
        descripcion = self.cleaned_data.get('descripcion')
        farmaco = self.cleaned_data.get('farmaco')
        pacientes = self.cleaned_data.get('pacientes')
        nivel_seguimiento = self.cleaned_data.get('nivel_seguimiento')
        fecha_inicio = self.cleaned_data.get('fecha_inicio')
        fecha_fin = self.cleaned_data.get('fecha_fin')
        
        #Comprobamos que no haya ningun ensayo clinico con el mismo nombre
        nombreEnsayo = EnsayoClinico.objects.filter(nombre=nombre).first()
        if (not nombreEnsayo is None):
            if(not self.instance is None and nombreEnsayo.id == self.instance.id):
                pass
            else:
                self.add_error('nombre', 'Ya existe un ensayo clínico con ese nombre.')
        
        if len(descripcion) >= 100:
            self.add_error('descripcion', 'La descripción no puede tener más de 100 caracteres.')
            
        if farmaco is not None and not farmaco.apto_para_ensayos:
            self.add_error('farmaco', 'El fármaco seleccionado no es apto para ensayos clínicos.')
        
        if not pacientes.count() == 0 and pacientes.filter(edad__lt=18):
            self.add_error('pacientes', 'Todos los pacientes deben ser mayores de edad.') 
        
        if nivel_seguimiento is not None:
            if nivel_seguimiento < 0 or nivel_seguimiento > 10:
                self.add_error('nivel_seguimiento', 'El nivel de seguimiento debe estar entre 0 y 10.')
                
        if fecha_inicio is not None and fecha_fin is not None:
            if fecha_fin < fecha_inicio:
                self.add_error('fecha_fin', 'La fecha de fin debe ser posterior a la fecha de inicio.')
        if fecha_fin >= timezone.now():
            self.add_error('fecha_fin', 'La fecha de fin no puede ser en el futuro.')
        
        
        return self.cleaned_data