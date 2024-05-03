from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import os


class ModeloBase(models.Model):

    created_at = models.DateTimeField('Fecha de Creacion', auto_now_add=True)
    updated_at = models.DateTimeField('Fecha de Modificacion', auto_now=True)
    deleted_at = models.DateTimeField('Fecha de Eliminacion', null=True, blank=True)
    deleted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    is_deleted = models.BooleanField('Eliminado', default=False)  # Campo para el borrado lógico

    class Meta:
        abstract = True

    def delete(self, *args, **kwargs):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.deleted_by = kwargs.get('deleted_by', None)  # Agregado para pasar el usuario que está eliminando
        self.save()

    def restore(self):
        self.is_deleted = False
        self.deleted_at = None
        self.deleted_by = None
        self.save()



class Reventos(ModeloBase):

    nEvent = models.CharField('Nombre Del Evento',max_length=100)
    nDate = models.DateField('Fecha')
    nTime = models.TimeField('Hora')
    nLocation = models.CharField('Ubicación',max_length=100)
    nDescription = models.TextField('Descripción del Evento',max_length=255)
    nImagen =  models.ImageField('Imagen',upload_to='eventos/',null=True,blank=True)


    class Meta:
        permissions = (("Can_view", "Puede Verlo"),)
        verbose_name = 'Eventos de Seguridad'
        verbose_name_plural = 'Evento de Seguridad'
        db_table = 'events'

    def __str__(self):
        return  self.nDate.strftime('%d/%m/%Y')  + " - " + self.nTime.strftime('%I:%M %p')+ " " + self.nEvent 
    



def visitor_photo_upload_path(instance, filename):
    # Construir la ruta de la carpeta usando el DNI del visitante
    dni_folder = str(instance.dni)
    return os.path.join('photo', dni_folder, filename)


class Person(ModeloBase):
    LIST_NAC = [
        ('VE', 'VENEZOLANO'),
        ('EX', 'EXTRANJERO'),
    ]
    nac = models.CharField('Nacionalidad', max_length=2, choices=LIST_NAC, null=True, blank=True)
    dni = models.CharField('Cedula', primary_key=True, max_length=10)
    first_name = models.CharField('Nombre', max_length=40)
    last_name = models.CharField('Apellido', max_length=40)
    GENDER_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
    ]
    gender = models.CharField('Género', max_length=1, choices=GENDER_CHOICES, null=True, blank=True)
    photo = models.ImageField('Fotografía', upload_to=visitor_photo_upload_path, default='photo/default.jpg')

    class Meta:
        verbose_name = 'Visitante'
        verbose_name_plural = 'Visitantes'
        ordering = ['dni']
        permissions = (
            ("permiso_personalizado", "Describe el permiso"),
        )


    def __str__(self):
        return self.dni


class AccessSEDE(models.Model):
    visitor = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='accesses')
    entry = models.DateField('Fecha del Dia')
    hours = models.TimeField('Hora de Entrada')
    hoursEx = models.TimeField('Hora de Salida', null=True, blank=True)

    DEPARTAMENTS_LIST = [
        ('TALENTO HUMANO', 'TALENTO HUMANO'),
        ('TECNOLOGIA', 'TECNOLOGIA'),
        ('ADMINISTRACION', 'ADMINISTRACION'),
        ('CONSULTORIA JURIDICA', 'CONSULTORIA JURIDICA'),
        ('SERVICIOS GENERALES', 'SERVICIOS GENERALES'),
        ('COMERCIALIZACION', 'COMERCIALIZACION'),
        ('CENTRO DE ESTUDIO DEL AGUA', 'CENTRO DE ESTUDIO DEL AGUA'),
        ('VP. GESTION INTERNA', 'VP. GESTION INTERNA'),
        ('VP. GESTION COMERCIAL', 'VP. GESTION COMERCIAL'),
        ('PRESIDENCIA', 'PRESIDENCIA'),
    ]
    departaments = models.CharField('Oficina a Visitar', max_length=30, choices=DEPARTAMENTS_LIST, null=True, blank=True)

    TYPE_VEHICLE = [
        ('NONE', 'NO POSEE'),
        ('SEDANES', 'CARRO LIVIANO-(TIPO SEDAN)'),
        ('CARGA', 'CAMION'),
    ]

    obs = models.TextField('Observaciones', max_length=140, null=True, blank=True, default='SIN OBSERVACIONES')

    class Meta:
        verbose_name = "Listado Accesos"
        verbose_name_plural = "Listado Accesos"

        ordering = ['entry', 'hours']

    def __str__(self):
        return f"{self.visitor.dni} {self.entry} {self.hours}"
    

