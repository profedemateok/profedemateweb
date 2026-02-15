from django.db import models
from django.conf import settings
from django.utils import timezone

class Servicio(models.Model):
    nombre = models.CharField(max_length=100) # Ej: "Clase Particular 1 a 1"
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    duracion_minutos = models.PositiveIntegerField(default=60)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

class Disponibilidad(models.Model):
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE)
    fecha = models.DateField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    reservado = models.BooleanField(default=False)
    
    # Esto es para evitar que crees dos turnos a la misma hora por error
    class Meta:
        verbose_name_plural = "Disponibilidades"
        ordering = ['fecha', 'hora_inicio']

    def __str__(self):
        return f"{self.servicio} - {self.fecha} {self.hora_inicio}"

class Reserva(models.Model):
    alumno = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    disponibilidad = models.OneToOneField(Disponibilidad, on_delete=models.CASCADE)
    fecha_reserva = models.DateTimeField(auto_now_add=True)
    # Aquí luego agregaremos estado de pago: 'pendiente', 'pagado'
    pagado = models.BooleanField(default=False) 

    def __str__(self):
        return f"Reserva de {self.alumno} para {self.disponibilidad}"