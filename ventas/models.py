from django.db import models
from django.contrib.auth.models import User
from django.utils.numberformat import format
import uuid

class Cliente(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    rut = models.CharField(max_length=12, unique=True)
    telefono = models.CharField(max_length=12)

    class Meta:
        app_label = 'ventas'

    def __str__(self):
        return self.usuario.username

class Categoria(models.Model):
    nombre = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = "Categorías"

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.IntegerField()
    imagen = models.ImageField(upload_to='productos/', null=True, blank=True)
    stock = models.IntegerField(default=0)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True)
    es_promocion = models.BooleanField(default=False)  # Añade esta línea si realmente necesitas este campo

    def __str__(self):
        return self.nombre

    @property
    def precio_formateado(self):
        return f"${self.precio:,.0f}"

class Pedido(models.Model):
    numero_pedido = models.CharField(max_length=10, unique=True, default=uuid.uuid4, editable=False)
    cliente = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, default='pendiente')
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def actualizar_total(self):
        self.total = sum(detalle.subtotal() for detalle in self.detalles.all())
        self.save()

    def __str__(self):
        return f"Pedido {self.numero_pedido}"

class DetallePedido(models.Model):
    pedido = models.ForeignKey(Pedido, related_name='detalles', on_delete=models.CASCADE)
    producto = models.ForeignKey('Producto', on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    def subtotal(self):
        return self.cantidad * self.precio_unitario

class Promocion(models.Model):
    nombre = models.CharField(max_length=100)
    productos = models.ManyToManyField('Producto', through='ProductoEnPromocion')
    imagen = models.ImageField(upload_to='promociones/', null=True, blank=True)
    precio = models.IntegerField()
    activa = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

    @property
    def precio_formateado(self):
        return f"${self.precio:,.0f}"

class ProductoEnPromocion(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    promocion = models.ForeignKey(Promocion, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre} en {self.promocion.nombre}"

class Venta(models.Model):
    fecha = models.DateTimeField(auto_now_add=True)
    total = models.IntegerField()

    def __str__(self):
        return f"Venta {self.id} - {self.fecha}"

class DetalleVenta(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey(Producto, on_delete=models.SET_NULL, null=True)
    promocion = models.ForeignKey(Promocion, on_delete=models.SET_NULL, null=True)
    cantidad = models.IntegerField()
    precio_unitario = models.IntegerField()

    def __str__(self):
        return f"Detalle de Venta {self.venta.id} - {self.producto or self.promocion}"
