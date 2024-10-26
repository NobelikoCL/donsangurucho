from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegistroClienteForm, PedidoForm, LoginForm, CheckoutForm, ClienteForm
from .models import Cliente, Producto, Pedido, DetallePedido, Promocion, Categoria
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json
import uuid
from django.shortcuts import get_object_or_404
import logging
from django.db import models
from django.utils import timezone

logger = logging.getLogger(__name__)

def home(request):
    return render(request, 'home.html')

def productos(request):
    categoria = request.GET.get('categoria', 'todos')
    categorias = ['todos', 'sandwiches', 'bebidas', 'promociones']  # Ajusta según tus categorías reales
    
    if categoria == 'promociones':
        promociones = Promocion.objects.filter(activa=True)
        productos = []
    elif categoria == 'todos':
        promociones = Promocion.objects.filter(activa=True)
        productos = Producto.objects.all()
    else:
        promociones = []
        productos = Producto.objects.filter(categoria=categoria)
    
    context = {
        'categorias': categorias,
        'categoria_seleccionada': categoria,
        'promociones': promociones,
        'productos': productos,
    }
    return render(request, 'productos.html', context)

def login_view(request):
    if request.user.is_authenticated:
        return redirect('mi_cuenta')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            rut = form.cleaned_data.get('rut')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=rut, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Usuario o contraseña incorrectos')
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

def registro(request):
    if request.user.is_authenticated:
        return redirect('mi_cuenta')
    if request.method == 'POST':
        form = RegistroClienteForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            Cliente.objects.create(
                usuario=usuario,
                rut=form.cleaned_data['rut'],
                telefono=form.cleaned_data['telefono']
            )
            login(request, usuario)
            return redirect('home')
    else:
        form = RegistroClienteForm()
    return render(request, 'accounts/registro.html', {'form': form})

@login_required
def realizar_pedido(request):
    if request.method == 'POST':
        form = PedidoForm(request.POST)
        if form.is_valid():
            # Lógica para procesar el pedido
            pass
    else:
        form = PedidoForm()
    productos = Producto.objects.all()
    return render(request, 'ventas/realizar_pedido.html', {'form': form, 'productos': productos})

@login_required
def mis_pedidos(request):
    pedidos = Pedido.objects.filter(cliente__usuario=request.user)
    return render(request, 'ventas/mis_pedidos.html', {'pedidos': pedidos})

@login_required
def mi_cuenta(request):
    # Esta vista solo será accesible para usuarios autenticados
    return render(request, 'accounts/mi_cuenta.html', {'user': request.user})

def carrito(request):
    if request.method == 'POST':
        # Aquí manejarías la lógica para agregar/actualizar items en el carrito
        # Por ahora, solo devolveremos un JSON de éxito
        return JsonResponse({'success': True})
    return render(request, 'carrito.html')

@login_required
def checkout(request):
    pedido = Pedido.objects.filter(cliente=request.user, estado='pendiente').first()
    if not pedido:
        return redirect('productos')
    
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            # Procesar el pago aquí (si es necesario)
            pedido.estado = 'confirmado'
            pedido.fecha_confirmacion = timezone.now()
            pedido.save()
            return redirect('confirmacion_pedido', numero_pedido=pedido.numero_pedido)
    else:
        form = CheckoutForm()
    
    context = {
        'pedido': pedido,
        'form': form,
    }
    return render(request, 'checkout.html', context)

# Si tienes una vista para recuperación de contraseña, actualízala también:
def password_recovery(request):
    # ... lógica de recuperación de contraseña ...
    return render(request, 'accounts/recovery.html', {...})

@csrf_exempt
def guardar_carrito(request):
    if request.method == 'POST':
        carrito = json.loads(request.body)
        request.session['carrito'] = carrito
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

def completar_perfil(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            cliente = form.save(commit=False)
            cliente.usuario = request.user
            cliente.save()
            return redirect('checkout')
    else:
        form = ClienteForm()
    return render(request, 'completar_perfil.html', {'form': form})

@require_POST
def agregar_al_carrito(request):
    try:
        producto_id = request.POST.get('producto_id')
        cantidad = int(request.POST.get('cantidad', 1))

        producto = Producto.objects.get(id=producto_id)
        pedido, created = Pedido.objects.get_or_create(
            cliente=request.user,
            estado='pendiente',
            defaults={'total': 0}  # Asegúrate de proporcionar un valor por defecto
        )

        detalle, detalle_created = DetallePedido.objects.get_or_create(
            pedido=pedido,
            producto=producto,
            defaults={'cantidad': 0, 'precio_unitario': producto.precio}
        )

        detalle.cantidad += cantidad
        detalle.save()

        pedido.actualizar_total()  # Actualiza el total del pedido

        return JsonResponse({
            'success': True,
            'mensaje': f'{producto.nombre} agregado al carrito',
            'cantidad_total': pedido.detalles.aggregate(total=models.Sum('cantidad'))['total']
        })
    except Producto.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Producto no encontrado'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

@require_POST
def actualizar_estado_pedido(request):
    data = json.loads(request.body)
    nuevo_estado = data.get('estado')

    pedido = Pedido.objects.filter(cliente=request.user, estado='desertado').first()

    if pedido:
        pedido.estado = nuevo_estado
        pedido.save()
        return JsonResponse({'success': True, 'numero_pedido': pedido.numero_pedido})
    else:
        return JsonResponse({'success': False, 'error': 'No se encontró un pedido activo'})

def confirmacion_pedido(request, numero_pedido):
    pedido = get_object_or_404(Pedido, numero_pedido=numero_pedido, cliente=request.user)
    detalles = DetallePedido.objects.filter(pedido=pedido)
    context = {
        'pedido': pedido,
        'detalles': detalles,
    }
    return render(request, 'ventas/confirmacion_pedido.html', context)

def obtener_cantidad_carrito(request):
    if request.user.is_authenticated:
        pedido = Pedido.objects.filter(cliente=request.user, estado='pendiente').first()
        cantidad = pedido.obtener_cantidad_total() if pedido else 0
    else:
        cantidad = 0
    return JsonResponse({'cantidad': cantidad})
