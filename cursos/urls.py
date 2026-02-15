from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_cursos, name='lista_cursos'),
    path('<slug:slug>/', views.detalle_curso, name='detalle_curso'),
    path('<slug:slug>/clase/<int:clase_id>', views.ver_clase, name="ver_clase")
]