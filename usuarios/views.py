from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import RegistroUsuarioForm
from cursos.models import Inscripcion
from reservas.models import Reserva # Importar el modelo Reserva
from django.utils import timezone # Importar para saber la fecha de hoy

# Create your views here.
def registro(request):
    if request.method == "POST":
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            login(request, usuario)
            return redirect('home')
    else:
        form = RegistroUsuarioForm()
    
    return render(request, 'usuarios/registro.html', {'form': form})
        
@login_required
def panel_alumno(request):
    # 1. Traer Cursos Grabados (lo que ya teníamos)
    inscripciones = Inscripcion.objects.filter(usuario=request.user).select_related('curso')
    
    # 2. Traer Reservas Futuras (NUEVO)
    # Filtramos donde la fecha sea mayor o igual (gte) a hoy.
    # Usamos select_related para traer los datos del servicio y la disponibilidad de un solo viaje (optimización).
    reservas_futuras = Reserva.objects.filter(
        alumno=request.user,
        disponibilidad__fecha__gte=timezone.now().date()
    ).select_related('disponibilidad', 'disponibilidad__servicio').order_by('disponibilidad__fecha', 'disponibilidad__hora_inicio')

    context = {
        'inscripciones': inscripciones,
        'reservas_futuras': reservas_futuras
    }
    
    return render(request, 'usuarios/panel.html', context)