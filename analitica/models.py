from django.db import models
from django.conf import settings

#modelos importados
from gestion_usuarios import Asignatura, Departamento_Provincial_Educacion, Servicio_Local_Educacion, Encargado

class Supervisor(models.Model):
    asignatura = models.ForeignKey('Asignatura', on_delete = models.CASCADE)
    departamento_Provincial_Educacion = models.ForeignKey('Departamento_Provincial_Educacion', on_delete = models.CASCADE)
    servicio_Local_Educacion = models.ForeignKey('Servicio_Local_Educacion', on_delete = models.CASCADE)
    usuario = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)

    def __str__(self):
        return self.usuario.__str__()

    class Meta: 
        verbose_name = _('supervisor') 
        verbose_name_plural = _('supervisores') 

class Actividad(models.Model):
    '''
    Modelo que representa una actividad de un encargado. Esta actividad puede ser la creación de
    una consulta, la subida de un recurso académico...
    '''
    titulo = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=300)
    link = models.URLField(max_length=200)
    encargado = models.ForeignKey('Encargado',on_delete=models.CASCADE)
    fecha = models.DateField("%d-%m-%Y", default=datetime.now)
