from django.db import models
from datetime import datetime
from gestion_usuarios.models import Grupo
from django.conf import settings

#modelos 
from gestion_usuarios.models import Encargado

class Consulta(models.Model): 
    ''' 
    Es la consulta 
    '''
    autor = models.ForeignKey(Encargado,on_delete=models.CASCADE)
    titulo = models.CharField(max_length = 100) 
    fecha_creacion = models.DateField("%d-%m-%Y", default= datetime.now) 
    fecha_finalizacion = models.DateField("%d-%m-%Y", null=False) 
    fecha_inicio = models.DateField("%d-%m-%Y", null=False) 
    descripcion = models.CharField(max_length = 255) 
    grupo = models.ManyToManyField(Grupo, blank=True, default=None)

    def __str__(self): 
        return (self.titulo) 
 
class ConsultaPropuesta(models.Model):
    ''' 
    Son las alternativas
    '''
    autor = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    titulo = models.CharField(max_length = 100) 
    descripcion = models.CharField(max_length = 255) 
    fecha_creacion = models.DateField("%d-%m-%Y", default=datetime.now) 
    contenido = models.TextField() 
    consulta = models.ForeignKey('Consulta', on_delete = models.CASCADE)
    votos = models.PositiveIntegerField(default=0) 
    def __str__(self): 
        return (self.titulo) 
  
class ConsultaRespuesta(models.Model):
    ''' 
    Es la respuesta de un usuario en especifico
    ''' 
    rut = models.CharField(max_length = 15) 
    fecha_creacion = models.DateField("%d-%m-%Y", default=datetime.now) 
    consulta = models.ForeignKey('Consulta', on_delete = models.CASCADE) 
    consulta_propuesta = models.ForeignKey('ConsultaPropuesta', on_delete = models.CASCADE) 
    
#class Restriccion(models.Model): 
#    nombre = models.CharField(max_length = 255) 
#    def __str__(self): 
#        return (self.nombre) 

