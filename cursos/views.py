from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Curso, CursoClase, Inscripcion

# Create your views here.
def lista_cursos(request):
    cursos = Curso.objects.filter(publicado=True)
    return render(request, 'cursos/lista_cursos.html', {'cursos': cursos})

def detalle_curso(request, slug):
    curso = get_object_or_404(Curso, slug=slug)
    clases_ordenadas = CursoClase.objects.filter(curso=curso).order_by('orden').select_related('clase')

    return render(request, 'cursos/detalle_curso.html', {
        'curso': curso,
        'clases_ordenadas': clases_ordenadas
    })

@login_required(login_url='login') # Redirige al login si no tiene sesión
def ver_clase(request, slug, clase_id):
    # 1. Buscamos el curso
    curso = get_object_or_404(Curso, slug=slug)
    tiene_acceso = Inscripcion.objects.filter(usuario=request.user, curso=curso).exists()
    if not tiene_acceso and not request.user.is_superuser:
        # Le enviamos un mensaje de error
        messages.error(request, 'Debes adquirir este curso para poder ver sus clases.')
        # Lo pateamos de vuelta a la página de detalles del curso
        return redirect('detalle_curso', slug=curso.slug)
    
    curso_clase = get_object_or_404(CursoClase, curso=curso, clase__id=clase_id)
    clase_actual = curso_clase.clase
    lista_clases = CursoClase.objects.filter(curso=curso).order_by('orden').select_related('clase')

    return render(request, 'cursos/ver_clase.html', {
        'curso': curso,
        'clase_actual': clase_actual,
        'lista_clases': lista_clases,
        'clase_orden': curso_clase.orden
    })