Sistema de Información Limpio Sano
Descripción del Proyecto
El "Sistema de Información Limpio Sano" es una aplicación web integral diseñada para la gestión y seguimiento de diversas áreas operativas de la empresa "Limpio Sano." La plataforma proporciona funcionalidades específicas para la administración de clientes, empleados, espacios, inventarios, servicios, y un dashboard con métricas clave para la toma de decisiones informadas.

Módulos Principales
1. Clientes
Descripción:
Gestiona la información de los clientes de "Limpio Sano," incluyendo datos personales y detalles de contacto.
2. Empleados
Descripción:
Permite la administración de los empleados de la empresa, con detalles como experiencia, sueldo, y asignación de servicios.
3. Espacios
Descripción:
Facilita el seguimiento de diferentes tipos de espacios, con información detallada sobre su estado actual y total.
4. Inventarios
Descripción:
Gestiona los suministros ecológicos a través del tiempo, proporcionando un historial de compras y usos.
5. Servicios
Descripción:
Administra los servicios proporcionados por la empresa, incluyendo detalles de clientes, empleados asignados y fechas de servicio.
6. Dashboard
Descripción:
Presenta métricas clave de la empresa en un formato visual y fácil de entender, incluyendo información sobre clientes, servicios, ingresos, y tasas de crecimiento.
Cómo Correr el Proyecto
A continuación se detallan los pasos generales para ejecutar el proyecto:

Requisitos Previos

activar entorno virtual, 

activar ejecucion de scripts, como admin: Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
luego activar virtualenv: ./venv/Scripts/activate


pip install -r requirements.txt

git clone 

Navega al directorio del proyecto:

python manage.py migrate
python manage.py makemigrations


python manage.py runserver


Inicia el servidor de desarrollo:
http://127.0.0.1:8000/


¡Listo! Ahora deberías poder explorar todas las funcionalidades del "Sistema de Información Limpio Sano."