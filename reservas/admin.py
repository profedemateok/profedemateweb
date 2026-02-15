from django.contrib import admin
from .models import Servicio, Disponibilidad, Reserva

@admin.register(Servicio)
class ServicioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio', 'duracion_minutos', 'activo')

@admin.register(Disponibilidad)
class DisponibilidadAdmin(admin.ModelAdmin):
    list_display = ('servicio', 'fecha', 'hora_inicio', 'reservado')
    list_filter = ('servicio', 'fecha', 'reservado')
    # Esto te permite ver solo los turnos futuros, no los de hace 3 meses
    date_hierarchy = 'fecha' 

@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ('alumno', 'disponibilidad', 'pagado', 'fecha_reserva')