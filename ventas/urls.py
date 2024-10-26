from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('productos/', views.productos, name='productos'),
    path('mi-cuenta/', views.mi_cuenta, name='mi_cuenta'),
    path('login/', views.login_view, name='login'),
    path('registro/', views.registro, name='registro'),
    path('logout/', views.logout_view, name='logout'),
    path('carrito/', views.carrito, name='carrito'),
    path('actualizar-estado-pedido/', views.actualizar_estado_pedido, name='actualizar_estado_pedido'),
    path('checkout/', views.checkout, name='checkout'),
    path('guardar-carrito/', views.guardar_carrito, name='guardar_carrito'),
    path('completar-perfil/', views.completar_perfil, name='completar_perfil'),
    path('agregar-al-carrito/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('obtener-cantidad-carrito/', views.obtener_cantidad_carrito, name='obtener_cantidad_carrito'),
    path('confirmacion-pedido/<str:numero_pedido>/', views.confirmacion_pedido, name='confirmacion_pedido'),
    # Asegúrate de que no haya patrones que se llamen a sí mismos
]

