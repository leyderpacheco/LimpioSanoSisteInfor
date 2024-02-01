import os
import django
from faker import Faker
from random import randint, choice
from myapp.models import Cliente, Espacio, Empleado, Servicio, Inventario, Detalles_Servicio
from django.utils import timezone
from datetime import datetime, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sist_infor.settings')
django.setup()

fake = Faker('es_CO')  # Establecer el idioma a español para obtener direcciones colombianas

# Eliminar todos los registros existentes
Detalles_Servicio.objects.all().delete()
Servicio.objects.all().delete()
Inventario.objects.all().delete()
Empleado.objects.all().delete()
Espacio.objects.all().delete()
Cliente.objects.all().delete()

# Crear una lista de clientes para su reutilización
clientes = [Cliente(
    nombre=fake.first_name(),
    apellido=fake.last_name(),
    correo=fake.email(),
    direccion=fake.address(),
    telefono=fake.phone_number()
) for _ in range(50)]

# Repetir algunos clientes hasta 3 o 4 veces
for _ in range(2):  # Ajusta este número según sea necesario
    clientes.extend(choice(clientes) for _ in range(randint(3, 4)))

# Guardar los clientes individualmente
for cliente in clientes:
    cliente.save()

# Crear una lista de espacios para su reutilización
espacios = [Espacio(
    tipo=fake.random_element(elements=('casa', 'oficina', 'apartamento')),
    metraje=randint(10, 300),
    estado=fake.random_element(elements=('en servicio', 'finalizado', 'próximo')),
    cliente=choice(clientes)
) for _ in range(50)]

# Guardar los espacios individualmente
for espacio in espacios:
    espacio.save()

# Crear una lista de empleados (limitada a 6)

empleados = [Empleado(
    nombre=fake.first_name(),
    apellido=fake.last_name(),
    direccion=fake.address(),
    telefono=fake.phone_number(),
    experiencia=randint(1, 10),
    sueldo=max(min(randint(1200000, 3500000) + (100000 * randint(1, 10)), 3500000), 1200000)
) for _ in range(6)]




# Guardar los empleados individualmente
for empleado in empleados:
    empleado.save()

# Asignar empleados con más experiencia a espacios con más espacio
empleados.sort(key=lambda x: x.experiencia, reverse=True)
for empleado in empleados:
    espacio_asignado = next((espacio for espacio in espacios if espacio.estado == 'próximo'), None)
    if espacio_asignado:
        espacio_asignado.empleado = empleado
        espacio_asignado.save()

# Calcular la fecha actual
fecha_actual = datetime.now()

# Definir la ventana de tiempo (5 meses antes y 1 mes después)
start_date = fecha_actual - timedelta(days=5*30)
end_date = fecha_actual + timedelta(days=30)

# Crear una lista de servicios para su reutilización
servicios = [Servicio(
    fecha=fake.date_time_between_dates(datetime_start=start_date, datetime_end=end_date),
    tipo=fake.random_element(elements=('Limpieza hogar', 'Limpieza oficina')),  # Modificado para tipos específicos
    costo=randint(80000, 100000) * (1 + 0.01 * espacio.metraje),
    cliente=choice(clientes),
    empleado=choice(empleados),
    espacio=choice(espacios)
) for _ in range(50)]

# Guardar los servicios individualmente
for servicio in servicios:
    servicio.save()

# Crear una lista de inventarios con nombres fijos
nombres_inventario = [
    'Detergente para lavar platos',
    'Limpiador multiusos',
    'Limpiador de vidrios',
    'Desinfectante',
    'Jabones ecológicos'
]

# Crear una lista de inventarios para su reutilización
inventarios = [Inventario(
    nombre=nombre,
    cantidad_total=500,  # Asignar una cantidad total predeterminada de 500
    precio=randint(10000, 300000)
) for nombre in nombres_inventario]

# Guardar inventarios primero
for inventario in inventarios:
    inventario.save()



# Crear una lista de detalles de servicio para su reutilización
detalles_servicios = []
for espacio in espacios:
    for _ in range(3):
        inventario_elegido = choice(inventarios)

        # Asegurarse de que la cantidad total no sea negativa
        cantidad_total_disponible = max(0, inventario_elegido.cantidad_total)

        # Asegurarse de que la cantidad utilizada de "Jabones ecológicos" sea como máximo 1
        if inventario_elegido.nombre == 'Jabones ecológicos':
            cantidad_utilizada = min(1, cantidad_total_disponible) * espacio.metraje // 100
        else:
            cantidad_utilizada = randint(0, min(10, cantidad_total_disponible)) * espacio.metraje // 100

        detalle_servicio = Detalles_Servicio(
            servicio=choice(servicios),
            inventario=inventario_elegido,
            cantidad_utilizada=cantidad_utilizada,
            tiempo_servicio=randint(30, 240)
        )

        # Reducir la cantidad total del inventario utilizado
        inventario_elegido.cantidad_total -= cantidad_utilizada
        inventario_elegido.save()

        detalles_servicios.append(detalle_servicio)

# Guardar los detalles de servicio individualmente
for detalle_servicio in detalles_servicios:
    detalle_servicio.save()

# ...


print("Base de datos poblada exitosamente!")
