from django.shortcuts import render
from .models import Cliente, Empleado, Espacio, Servicio, Inventario, Detalles_Servicio
from django.http import HttpResponse
import json
from django.core.serializers import serialize
from django.db.models import Count
from django.db.models.functions import TruncMonth
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse
from django.db.models import Sum
from datetime import datetime, timedelta
from datetime import timedelta
import json
from datetime import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Sum, F
from django.utils import timezone

# Create your views here.
"""def menu(request):
    return render(request, 'index.html')"""
def index(request):
     # Se obtiene el total de clientes y servicios
    total_clientes = Cliente.objects.count()
    total_servicios = Servicio.objects.count()
    
     # Obtén datos mensuales de servicios
    servicios_por_mes = Servicio.objects.annotate(mes=TruncMonth('fecha')).values('mes').annotate(total=Count('id')).order_by('mes')

    # Convierte los datos a una lista antes de pasarlos al contexto
    servicios_por_mes_list = list(servicios_por_mes)

    # Convierte la lista a una cadena JSON
    servicios_por_mes_json = json.dumps(servicios_por_mes_list, cls=DjangoJSONEncoder)
    
   # Obtener la suma del costo de los servicios agrupados por mes
    ingresos_por_mes = Servicio.objects.annotate(month=TruncMonth('fecha')).values('month').annotate(ingresos=Sum('costo')).order_by('month')
    
    ########################
    # Obtener los ingresos mensuales
    ingresos_mensuales = Servicio.objects.values('fecha__year', 'fecha__month').annotate(ingreso_mensual=Sum('costo')).order_by('fecha__year', 'fecha__month').values_list('ingreso_mensual', flat=True)

    # Calcular el crecimiento mes a mes
    crecimiento_mes_a_mes = calcular_crecimiento_mes_a_mes(ingresos_mensuales)

    # Calcular el promedio del crecimiento
    promedio_crecimiento = sum(crecimiento_mes_a_mes) / len(crecimiento_mes_a_mes) if crecimiento_mes_a_mes else None
   
    # Pasa los datos al contexto
    context = {
        'total_clientes': total_clientes,
        'total_servicios': total_servicios,
        'servicios_por_mes_json': servicios_por_mes_json,
        'ingresos_por_mes': ingresos_por_mes,
        'promedio_crecimiento': promedio_crecimiento.__round__,
        
    }
    
    return render(request, "dashboard.html", context)

def calcular_crecimiento_mes_a_mes(ingresos):
    crecimiento_mes_a_mes = []
    ingreso_anterior = 0

    for ingreso_actual in ingresos:
        tasa_crecimiento = ((ingreso_actual - ingreso_anterior) / ingreso_anterior) * 100 if ingreso_anterior != 0 else 0
        crecimiento_mes_a_mes.append(tasa_crecimiento)
        ingreso_anterior = ingreso_actual

    return crecimiento_mes_a_mes

def home(request):
    # Obtener la información para el gráfico de tipos de espacios
    espacios = Espacio.objects.values('tipo').annotate(total=Count('id'))
    nombres_espacios = [espacio['tipo'] for espacio in espacios]
    totales = [espacio['total'] for espacio in espacios]

    # Obtener la información para el gráfico de estados de espacios
    estados_espacios = Espacio.objects.values('estado').annotate(total=Count('id'))
    nombres_estados = [estado['estado'] for estado in estados_espacios]
    totales_estados = [estado['total'] for estado in estados_espacios]

    data = {
        'nombres_espacios': nombres_espacios,
        'totales': totales,
        'estados_espacios': nombres_estados,
        'total_por_estado': totales_estados,
    }
    json_data = json.dumps(data)

    return render(request, 'espacios.html', {'data': json_data})
    

"""def dashboard(request):
    return render(request, 'dashboard.html')"""
    
def hello(request, username):
    #print(username)
    return HttpResponse("<h1>Hello %s</h1>" %username)

def about(request):
    return render(request, 'about.html')


def inventarios(request):
    inventarios = Inventario.objects.all()

    historiales = []
    for inventario in inventarios:
        historial_compras = Detalles_Servicio.objects.filter(
            inventario=inventario,
            cantidad_utilizada__gt=0
        ).values(
            'cantidad_utilizada',
            'servicio__fecha',
            'inventario__precio'
        )

        historial_usos = Detalles_Servicio.objects.filter(
            inventario=inventario,
            servicio__espacio__estado='finalizado'
        ).values(
            'cantidad_utilizada',
            'servicio__fecha'
        ).annotate(total_utilizado=Sum('cantidad_utilizada'))

        # Asegurarse de que la cantidad utilizada no sea mayor que la cantidad total
        if historial_usos and historial_usos[0]['total_utilizado'] > inventario.cantidad_total:
            historial_usos[0]['total_utilizado'] = inventario.cantidad_total

        # Obtener el total actual usando el método que definiste en el modelo Inventario
        total_actual = inventario.obtener_total_actual()

        # Calcular la división y agregar el resultado al contexto
        aproximado_futuros_servicios = total_actual / 2

        historiales.append({
            'inventario': inventario,
            'historial_compras': historial_compras,
            'historial_usos': historial_usos,
            'total_actual': total_actual,
            'aproximado_futuros_servicios': aproximado_futuros_servicios,
        })

    return render(request, 'inventarios.html', {'historiales': historiales})


def clientes(request):
    #clientes = list(Cliente.objects.values())
    clientes = Cliente.objects.all()
    return render(request, 'clientes.html', {
        'clientes': clientes
    })

def empleados(request):
    
    def default_serializer(obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        raise TypeError("Type not serializable")

    empleados = Empleado.objects.all()
    servicios_proximos = Servicio.objects.filter(espacio__estado='próximo', fecha__gt=timezone.now())

    for servicio in servicios_proximos:
        empleados_disponibles = empleados.filter(
            experiencia__gte=servicio.empleado.experiencia
        ).order_by('experiencia')

        if empleados_disponibles.exists():
            empleado_asignado = empleados_disponibles.first()
            servicio.empleado = empleado_asignado
            servicio.save()

    servicios_asignados = Servicio.objects.filter(espacio__estado='próximo', fecha__gt=timezone.now()).values(
        'id', 'cliente__nombre', 'empleado__nombre', 'empleado__apellido', 'fecha', 'espacio__tipo'
    )
    
    print(servicios_asignados)

    data = {
        'empleados': [
            [empleado.nombre, empleado.apellido, empleado.direccion, empleado.telefono, str(empleado.experiencia), str(empleado.sueldo)]
            for empleado in empleados
        ],
        'servicios_realizados': [
            empleado.servicio_set.count() for empleado in empleados
        ],
        'servicios_asignados': [
            {
                'id': servicio['id'],
                'cliente': servicio['cliente__nombre'],
                'empleado': f"{servicio['empleado__nombre']} {servicio['empleado__apellido']}",
                'fecha': servicio['fecha'],
                'tipo_espacio': servicio['espacio__tipo'],
            }
            for servicio in servicios_asignados
        ],
    }

    print(data['servicios_asignados'])
    json_data = json.dumps(data, default=default_serializer)
    return render(request, 'empleados.html', {'data': json_data})

def format_datetime(obj):
    if isinstance(obj, datetime):
        return obj.strftime('%Y-%m-%dT%H:%M:%SZ')
    return obj

def espacios(request):
    return render(request, 'espacios.html')

def servicios(request):
    
    def default_serializer(obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        raise TypeError("Type not serializable")
    
    servicios = Servicio.objects.all()
    
    data = {
        'servicios': [
            [servicio.fecha, servicio.tipo, str(servicio.costo), servicio.cliente.nombre, f"{servicio.empleado.nombre} {servicio.empleado.apellido}", servicio.espacio.tipo]
            for servicio in servicios
        ],
    }

    json_data = json.dumps(data, default=default_serializer)
    #context = {'data': json_data}
    print(data['servicios'])
    return render(request, 'servicios.html', {'data': json_data})

def gestion(request):
    return render(request, 'gestion_inv.html')