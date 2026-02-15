from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Servicio, Disponibilidad, Reserva

def lista_servicios(request):
    servicios = Servicio.objects.filter(activo=True)
    return render(request, 'reservas/servicios.html', {'servicios': servicios})

@login_required(login_url='login')
def ver_horarios(request, servicio_id):
    servicio = get_object_or_404(Servicio, id=servicio_id)
    
    # Filtramos: Que sean de este servicio, que NO estén reservados, 
    # y que la fecha sea hoy o futuro (no mostramos el pasado)
    horarios = Disponibilidad.objects.filter(
        servicio=servicio,
        reservado=False,
        fecha__gte=timezone.now().date()
    ).order_by('fecha', 'hora_inicio')

    return render(request, 'reservas/horarios.html', {
        'servicio': servicio,
        'horarios': horarios
    })

@login_required
def reservar_turno(request, disponibilidad_id):
    # Esta es la lógica para confirmar la reserva
    turno = get_object_or_404(Disponibilidad, id=disponibilidad_id)
    
    if turno.reservado:
        messages.error(request, "Lo sentimos, este turno ya fue tomado por otro alumno.")
        return redirect('lista_servicios')

    # Si es método POST (confirmación del usuario)
    if request.method == 'POST':
        # 1. Crear la reserva
        reserva = Reserva.objects.create(
            alumno=request.user,
            disponibilidad=turno
        )
        
        # 2. Marcar el turno como ocupado
        turno.reservado = True
        turno.save()
        
        messages.success(request, f"¡Reserva exitosa! Te esperamos el {turno.fecha}.")
        return redirect('panel_alumno') # Ojo: Tendremos que agregar las reservas al panel después

    # Si es GET, mostramos confirmación
    return render(request, 'reservas/confirmar_reserva.html', {'turno': turno})