from django.shortcuts import render, get_object_or_404
from .models import Curso, CursoClase

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