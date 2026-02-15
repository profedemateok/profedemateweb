from django.db import models
from django.conf import settings

# Create your models here.
class Clase(models.Model):
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    video_url = models.URLField()

    def __str__(self):
        return self.titulo

class Curso(models.Model):
    titulo = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    imagen = models.ImageField(upload_to='cursos_img/', blank=True, null=True)
    publicado = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    clases = models.ManyToManyField(Clase, through='CursoClase', related_name='cursos')

    def __str__(self):
        return self.titulo

class CursoClase(models.Model):
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    clase = models.ForeignKey(Clase, on_delete=models.CASCADE)
    orden = models.PositiveIntegerField()

    class Meta:
        ordering = ['orden']
        unique_together = ('curso', 'orden')

    def __str__(self):
        return f'{self.curso.titulo} - {self.orden}: {self.clase.titulo}'
    
class Inscripcion(models.Model):
    # Relacionamos al Usuario
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='inscripciones')
    # Relacionamos al Curso
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='inscripciones')
    fecha_compra = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Esto es clave: Evita que un alumno compre el mismo curso dos veces por accidente
        unique_together = ('usuario', 'curso') 

    def __str__(self):
        return f"{self.usuario.username} matriculado en {self.curso.titulo}"

    