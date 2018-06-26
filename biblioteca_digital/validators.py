from django.core.exceptions import ValidationError


def file_size(value): # add this to some file where you can import it from
    limit = 5 * 1024 * 1024
    if value.size > limit:
        raise ValidationError('Archivo demasiado pesado, no debe pasar los 5MB.')

def pdf_type(value):
    pdf_type= "application/pdf"

    if value.content_type==pdf_type:
        pass
    else:
        raise ValidationError('El archivo debe ser de tipo pdf.')