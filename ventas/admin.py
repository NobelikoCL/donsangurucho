from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Producto, Promocion, ProductoEnPromocion, Venta, DetalleVenta

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'precio_formateado', 'stock']
    search_fields = ['nombre', 'descripcion']

class ProductoEnPromocionInline(admin.TabularInline):
    model = ProductoEnPromocion
    extra = 1

@admin.register(Promocion)
class PromocionAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'precio_formateado', 'activa', 'imagen_preview']
    list_filter = ['activa']
    search_fields = ['nombre']
    inlines = [ProductoEnPromocionInline]

    def imagen_preview(self, obj):
        if obj.imagen:
            return mark_safe(f'<img src="{obj.imagen.url}" width="50" height="50" />')
        return "Sin imagen"
    imagen_preview.short_description = 'Vista previa'

@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
    list_display = ['id', 'fecha', 'total']

class DetalleVentaInline(admin.TabularInline):
    model = DetalleVenta
    extra = 1

admin.site.register(ProductoEnPromocion)
admin.site.register(DetalleVenta)
