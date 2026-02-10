from django.db import models

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

    