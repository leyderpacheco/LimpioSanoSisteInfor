from django.db import models
from datetime import timedelta
from django.db.models import Avg
from django.db.models import Sum, F

#creacion del modelo completo de la base de datos a utilizar

class Cliente(models.Model):
    nombre = models.CharField(max_length=200)
    apellido = models.CharField(max_length=200)
    correo = models.EmailField(max_length=256)
    direccion = models.CharField(max_length=50)
    telefono = models.CharField(max_length=15, help_text='numero de contacto')
    
    def __str__(self):
        return f'{self.nombre} {self.apellido}'

class Espacio(models.Model):
    tipo = models.CharField(max_length=50) 
    metraje = models.IntegerField()
    estado = models.CharField(max_length=50)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)

class Empleado(models.Model):
    nombre = models.CharField(max_length=200)
    apellido = models.CharField(max_length=200)
    direccion = models.CharField(max_length=50)
    telefono = models.CharField(max_length=15, help_text='numero de contacto')
    #años de experiencia
    experiencia = models.IntegerField()
    sueldo = models.IntegerField(default=0)


    
class Servicio(models.Model):
    fecha = models.DateTimeField()
    #tipo de servicio
    tipo = models.CharField(max_length=50)
    #lo que costó el servicio
    costo = models.IntegerField(default=0)
    #fk_cliente
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    #fk_empleado
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    espacio = models.ForeignKey(Espacio, on_delete=models.CASCADE)
    
    def date_now(self):
        return self.fecha.strftime('%d/%m/%Y %H:%M:%S')
    
    def tipo_tiempo_estimado(self):
        servicios_previos = Servicio.objects.filter(
            tipo=self.tipo,
            fecha__lt=self.fecha
        )
        tiempo_promedio = servicios_previos.aggregate(tiempo_promedio=Avg('tiempo_servicio'))['tiempo_promedio']
        return tiempo_promedio or 0

    def eficiencia(self):
        tipo_tiempo_estimado = self.tipo_tiempo_estimado()
        if tipo_tiempo_estimado == 0:
            return 0

        eficiencia = (self.tipo_tiempo_estimado() / tipo_tiempo_estimado) * 100
        return round(eficiencia, 2)
    
    def fecha_fin(self):
        return self.fecha + timedelta(minutes=self.tipo_tiempo_estimado())
    
class Inventario(models.Model):
    nombre = models.CharField(max_length=200, unique=True)
    cantidad_total = models.DecimalField(max_digits=9, decimal_places=0, default=0)
    #precio que costaron los productos
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return self.nombre
    
    def obtener_total_actual(self):
        # Obtener la suma de las cantidades compradas
        total_comprado = Detalles_Servicio.objects.filter(
            inventario=self
        ).aggregate(
            total_comprado=Sum(F('cantidad_utilizada') * -1)
        )['total_comprado'] or 0  # En caso de que la suma sea None, establecerlo a 0

        # Calcular el total actual sumando la cantidad total y la cantidad comprada
        total_actual = self.cantidad_total + total_comprado

        return total_actual
    
class Detalles_Servicio(models.Model):
    #id del servicio
    servicio = models.ForeignKey(Servicio,on_delete=models.CASCADE)
    #ID_Inventario, equivale al ID del producto del inventario(ID_Inventario)
    inventario = models.ForeignKey(Inventario, on_delete=models.CASCADE)
    cantidad_utilizada = models.DecimalField(max_digits=9, decimal_places=0, default=0)
    tiempo_servicio = models.IntegerField()
    
     # Puedes agregar un método para actualizar la cantidad total después de cada servicio
    def actualizar_cantidad_total(self):
        self.inventario.cantidad_total -= self.cantidad_utilizada
        self.inventario.save()

    





