from django.test import TestCase
from .models import Empleado  # Asegúrate de importar tu modelo

class EmpleadosViewTest(TestCase):
    def setUp(self):
        # Asegúrate de que los datos que buscas existan en la base de datos
        Empleado.objects.create(
            nombre="Maicol",
            apellido="Moreno",
            direccion="Calle 71 # 8-39\nApto. 15\n680581\nBarbosa, Santander",
            telefono="+57 605 808 83 50",
            experiencia="4",
            sueldo="2035238"
        )

    def test_empleados_view(self):
        # Realiza la solicitud a la vista
        response = self.client.get('/mis_empleados/')  # Ajusta la URL según tu configuración

        # Verifica que la respuesta tenga el contenido esperado
        self.assertContains(response, 'Maicol Moreno')
