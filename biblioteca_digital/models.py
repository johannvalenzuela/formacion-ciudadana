from django.db import models
from datetime import datetime
import os
from django.conf import settings

TEMA_ALTERNATIVAS = (
    (1, 'formacion ciudadana'),
    (2, 'convivencia escolar'),
    (3, 'otros'),
)

def update_imagen(instance, filename):
    upload_to = 'recursos/'
    ext = filename.split('.')[-1]
    filename = '{}_{}.{}'.format(instance.titulo,'img_des', ext)
    return os.path.join(upload_to, filename)

def update_filename(instance, filename):
    upload_to = 'recursos/'
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(instance.titulo, ext)
    return os.path.join(upload_to, filename)

class Recurso(models.Model):
    titulo = models.CharField(max_length = 255, blank = False, null = False, unique=True)
    descripcion = models.CharField(max_length = 255, blank = False, null = False)
    imagen_descriptiva = models.FileField(upload_to=update_imagen, null = False)
    fecha_creacion = models.DateTimeField(default=datetime.now)
    tema = models.PositiveSmallIntegerField(choices=TEMA_ALTERNATIVAS,default=1)
    archivo = models.FileField(upload_to=update_filename, null = False)
    valoracionTotal = models.FloatField(default=0)
    cant_valoracion = models.PositiveIntegerField(default=0)
    autor = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)

    def setValoracion(self, valoracionNueva):
        valoracionNueva = (int)(valoracionNueva)
        self.cant_valoracion +=1
        self.valoracionTotal = (self.valoracionTotal*self.cant_valoracion + valoracionNueva)/self.cant_valoracion



    def __str__(self):
        return '%s' % (self.titulo)

class ComentarioRecurso(models.Model):
    autorComentario = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    recurso = models.ForeignKey('Recurso',on_delete=models.CASCADE)
    comentario = models.CharField(max_length= 255, blank=False)
    fecha_creacion = models.DateTimeField(default=datetime.now, blank=True)

class ValoracionRecurso(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    recurso = models.ForeignKey('Recurso',on_delete=models.CASCADE)
    valoracion = models.FloatField(default=0)

    
