from django.db import migrations

def add_default_categories(apps, schema_editor):
    Categoria = apps.get_model('ventas', 'Categoria')
    default_categories = [
        'completos',
        'churrascos',
        'hamburguesas',
        'mechadas',
        'as',
        'chorrillanas',
        'papas fritas',
        'extras',
        'agregados',
        'bebidas'
    ]
    for category_name in default_categories:
        Categoria.objects.get_or_create(nombre=category_name)

class Migration(migrations.Migration):

    dependencies = [
        ('ventas', '0005_producto_es_promocion'),  # Asegúrate de que este sea el número de tu migración anterior
    ]

    operations = [
        migrations.RunPython(add_default_categories),
    ]