from django.db import models
from django.contrib.auth.models import AbstractUser


class Usuario(AbstractUser):
    
    ADMINISTRADOR = 1
    INVESTIGADOR = 2
    PACIENTE = 3
    ROLES = (
        (ADMINISTRADOR, 'Administrador'),
        (INVESTIGADOR, 'Investigador'),
        (PACIENTE, 'Paciente'),
    )
    rol = models.PositiveSmallIntegerField(
        choices=ROLES,
        default=1
    )


class Farmaco(models.Model):
    
    nombre = models.CharField(max_length=100)
    apto_para_ensayos = models.BooleanField()
    
    def __str__(self):
        return self.nombre
    
class EnsayoClinico(models.Model):
    
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    farmaco = models.ForeignKey(Farmaco, on_delete=models.CASCADE)
    pacientes = models.ManyToManyField('Paciente')
    nivel_seguimiento = models.IntegerField()
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    activo = models.BooleanField(default=True)
    creado_por = models.ForeignKey('Investigador',
    on_delete=models.CASCADE)
    
    def __str__(self):
        return self.nombre
    
    
class Investigador(models.Model):
    
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Paciente(models.Model):
    
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    edad = models.IntegerField()
    def __str__(self):
        return self.user