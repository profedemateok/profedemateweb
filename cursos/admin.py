from django.contrib import admin
from .models import Curso, Clase, CursoClase

# Register your models here.
@admin.register(Clase)
class ClaseAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'video_url')
    search_fields = ('titulo', )

class CursoClaseInline(admin.TabularInline):
    model = CursoClase
    extra = 1
    autocomplete_fields = ['clase']

@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'precio', 'publicado')
    inlines = [CursoClaseInline]
    prepopulated_fields = {'slug' : ('titulo',)}