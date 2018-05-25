from django.db import models
from datetime import datetime
import os
from uuid import uuid4

def update_filename(instance, filename):
    upload_to = 'recursos/' + instance.titulo
    ext = filename.split('.')[-1]
    filename = '{}_{}.{}'.format(instance.titulo,'img_des', ext)
    return os.path.join(upload_to, filename)


class Recurso(models.Model):
    titulo = models.CharField(max_length = 255, blank = False, null = False, unique=True)
    descripcion = models.CharField(max_length = 255, blank = False, null = False)
    imagen_descriptiva = models.FileField(upload_to=update_filename)
    valoracion = models.IntegerField(default=0)
    fecha_creacion = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return '%s' % (self.titulo)