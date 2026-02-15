from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_servicios, name='lista_servicios'),
    path('servicio/<int:servicio_id>/', views.ver_horarios, name='ver_horarios'),
    path('reservar/<int:disponibilidad_id>/', views.reservar_turno, name='reservar_turno'),
]