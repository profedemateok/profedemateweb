from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import RegistroUsuarioForm
from cursos.models import Inscripcion

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
    # Traemos todas las inscripciones del usuario que está logueado
    # select_related('curso') es para que Django no haga consultas extra lentas
    inscripciones = Inscripcion.objects.filter(usuario=request.user).select_related('curso')
    
    return render(request, 'usuarios/panel.html', {'inscripciones': inscripciones})