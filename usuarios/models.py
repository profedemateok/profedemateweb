from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Usuario(AbstractUser):
    es_estudiante = models.BooleanField(default=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f'{self.username} ({'Estudiante' if self.es_estudiante else 'Admin'})'