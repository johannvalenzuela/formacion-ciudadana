from django.db import models

class Usuario(models.Model):
    nombre = models.CharField(max_length = 255)
    rut = models.CharField(max_length = 255)
    num_documento = models.CharField(max_length = 255)
    fecha_nacimiento = models.DateField("%d-%m-%Y")
    password = models.CharField(max_length = 255)
    apellido_paterno = models.CharField(max_length = 255)
    apellido_materno = models.CharField(max_length = 255)
    tipo = models.CharField(max_length = 255)
    def __str__(self):
        return (self.nombre)

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
    
class Supervisor(models.Model):
    asignatura = models.ForeignKey('Asignatura', on_delete = models.CASCADE)
    departamento_Provincial_Educacion = models.ForeignKey('Departamento_Provincial_Educacion', on_delete = models.CASCADE)
    servicio_Local_Educacion = models.ForeignKey('Servicio_Local_Educacion', on_delete = models.CASCADE)

class Grupo(models.Model):
    nombre = models.CharField(max_lenght = 255)
    establecimiento = models.ForeignKey('Establecimiento', on_delete = models.CASCADE)
    def __str__(self):
        return (self.nombre)

class Grupo_Usuario(models.Model):
    grupo = models.ForeignKey('Grupo', on_delete = models.CASCADE)


# CONSULTA CIUDADANA

class Consulta(models.Model):
    titulo = models.CharField(max_length = 255)
    fecha_creacion = models.DateField("%d-%m-%Y")
    fecha_finalizacion = models.DateField("%d-%m-%Y")
    fecha_inicio = models.DateField("%d-%m-%Y")
    descripcion = models.CharField(max_length = 255)
    def __str__(self):
        return (self.titulo)

class Consulta_propuesta(models.Model):
    titulo = models.CharField(max_length = 255)
    descripcion = models.CharField(max_length = 255)
    fecha_creacion = models.DateField("%d-%m-%Y")
    #contenido     Nose que es :v
    consulta = models.ForeignKey('Consulta', on_delete = models.CASCADE)
    def __str__(self):
        return (self.titulo)

class Restriccion(models.Model):
    nombre = models.CharField(max_length = 255)
    def __str__(self):
        return (self.nombre)

class Consulta_respuesta(models.Model):
    rut = models.CharField(max_length = 255)
    fecha_creacion = models.DateField("%d-%m-%Y")
    consulta = models.ForeignKey('Consulta', on_delete = models.CASCADE)
    consulta_propuesta = models.ForeignKey('Consulta_propuesta', on_delete = models.CASCADE)

class Consulta_grupo(models.Model):
    consulta = models.ForeignKey('Consulta', on_delete = models.CASCADE)
    grupo = models.ForeignKey('Grupo', on_delete = models.CASCADE)

# BIBLIOTECA DE RECURSOS
class Recurso(models.Model):
    titulo = models.CharField(max_length = 255)
    descripcion = models.CharField(max_length = 255)
    valoracion = models.CharField(max_length = 255)
    fecha_creacion = models.DateField("%d-%m-%Y")
    asignatura = models.ForeignKey('Asignatura', on_delete = models.CASCADE)