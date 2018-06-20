from django.db import models
from datetime import datetime
import os
from django.conf import settings
from django.utils.translation import ugettext_lazy as _



class Servicio_Local_Educacion(models.Model):
    nombre = models.CharField(max_length = 50)
    def __str__(self):
        return (self.nombre)

    class Meta: 
        verbose_name = _('servicio local de educación') 
        verbose_name_plural = _('servicios locales de educación')

class Departamento_Provincial_Educacion(models.Model):
    nombre = models.CharField(max_length = 50)
    def __str__(self):
        return (self.nombre)

    class Meta: 
        verbose_name = _('departamento provincial de educación') 
        verbose_name_plural = _('departamentos provinciales de educación') 

class Establecimiento(models.Model):
    nombre = models.CharField(max_length = 50)
    direccion = models.CharField(max_length = 100)
    departamento_Provincial_Educacion = models.ForeignKey('Departamento_Provincial_Educacion', on_delete = models.CASCADE)
    servicio_Local_Educacion = models.ForeignKey('Servicio_Local_Educacion', on_delete = models.CASCADE)
    def __str__(self):
        return (self.nombre)

    class Meta: 
        verbose_name = _('establecimiento') 
        verbose_name_plural = _('establecimientos') 

class Asignatura(models.Model):
    nombre = models.CharField(max_length = 50)
    def __str__(self):
        return (self.nombre)

    class Meta: 
        verbose_name = _('asignatura') 
        verbose_name_plural = _('asignaturas') 

class Encargado(models.Model):
    establecimiento = models.ForeignKey('Establecimiento', on_delete = models.CASCADE)
    asignatura = models.ForeignKey('Asignatura', on_delete = models.CASCADE)
    usuario = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    supervisor = models.ForeignKey('analitica.Supervisor',on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.usuario.__str__()

    class Meta: 
        verbose_name = _('encargado') 
        verbose_name_plural = _('encargados') 

class Grupo(models.Model):
    nombre = models.CharField(max_length = 50)
    autor = models.ForeignKey('Encargado', on_delete = models.CASCADE)
    establecimiento = models.ForeignKey('Establecimiento', on_delete = models.CASCADE)

    def __str__(self):
        return '%s del %s' % (self.nombre, self.establecimiento)

    class Meta: 
        verbose_name = _('grupo') 
        verbose_name_plural = _('grupos') 

class RutAutorizados(models.Model):
    '''
    Modelo que representa a un usuario perteneciente a un grupo de una consulta en especifica.
    '''
    rut = models.CharField(max_length=15)
    nombre = models.CharField(max_length=50)
    grupo = models.ManyToManyField("Grupo")

