from django.db import models


class Servicio_Local_Educacion(models.Model):
    nombre = models.CharField(max_lenght = 255)
    def __str__(self):
        return (self.nombre)

class Departamento_Provincial_Educacion(models.Model):
    nombre = models.CharField(max_lenght = 255)
    def __str__(self):
        return (self.nombre)

class Establecimiento(models.Model):
    nombre = models.CharField(max_lenght = 255)
    direccion = models.CharField(max_lenght = 255)
    departamento_Provincial_Educacion = models.ForeignKey('Departamento_Provincial_Educacion', on_delete = models.CASCADE)
    servicio_Local_Educacion = models.ForeignKey('Servicio_Local_Educacion', on_delete = models.CASCADE)
    def __str__(self):
        return (self.nombre)

class Asignatura(models.Model):
    nombre = models.CharField(max_lenght = 255)
    def __str__(self):
        return (self.nombre)

class Encargado(models.Model):
    establecimiento = models.ForeignKey('Establecimiento', on_delete = models.CASCADE)
    asignatura = models.ForeignKey('Asignatura', on_delete = models.CASCADE)
    usuario = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    
class Supervisor(models.Model):
    asignatura = models.ForeignKey('Asignatura', on_delete = models.CASCADE)
    departamento_Provincial_Educacion = models.ForeignKey('Departamento_Provincial_Educacion', on_delete = models.CASCADE)
    servicio_Local_Educacion = models.ForeignKey('Servicio_Local_Educacion', on_delete = models.CASCADE)
    usuario = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)

class Grupo(models.Model):
    nombre = models.CharField(max_lenght = 255)
    establecimiento = models.ForeignKey('Establecimiento', on_delete = models.CASCADE)
    usuarios = models.ManyToManyField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    def __str__(self):
        return (self.nombre)


