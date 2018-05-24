from django.db import models


class Recurso(models.Model):
    titulo = models.CharField(max_length = 255)
    descripcion = models.CharField(max_length = 255)
    valoracion = models.CharField(max_length = 255)
    fecha_creacion = models.DateField("%d-%m-%Y")
    asignatura = models.ForeignKey('Asignatura', on_delete = models.CASCADE)