from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('ensayos/',views.ensayo_lista, name='lista'),
    path('ensayo/<int:ensayo>',views.ensayo,name="ensayo"),
    path('ensayo/crear/',views.crear_ensayo, name='crear_ensayo'),
    path('ensayo-clinico/eliminar/<int:ensayo>',views.eliminar,name='eliminar'),
    path('seleccion',views.seleccion,name='seleccion'),
    path('registrar_investigador',views.registrar_investigador,name='registrar_investigador'),
    path('registrar_paciente',views.registrar_paciente,name='registrar_paciente'),
    
]
