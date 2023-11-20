from django.urls import path
from . import views

urlpatterns = [
    path('espacios/', views.home, name="home"),
    path('',views.index, name="dashboard-index"),
    #path('menu/', views.menu, name="dashboard"),
    #path('dashboard/', views.dashboard, name="dashboard"),
    path('about/', views.about, name="about"),
    path('hello/<str:username>', views.hello, name="hello"),
    path('mis_clientes/', views.clientes, name="clientes"),
    path('inventario/', views.inventarios, name="inventario"),
    path('servicios/', views.servicios, name="servicios"),
    path('mis_empleados/', views.empleados, name="empleados"),
]