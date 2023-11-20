from django.contrib import admin
from .models import Cliente, Empleado, Espacio, Servicio, Inventario, Detalles_Servicio

# Lista de todos los modelos
modelos = [Cliente, Empleado, Espacio, Servicio, Inventario, Detalles_Servicio]

# Register your models here.
# Registro de todos los modelos en el administrador
for modelo in modelos:
    admin.site.register(modelo)