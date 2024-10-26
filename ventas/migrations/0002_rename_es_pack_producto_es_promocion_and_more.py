# Generated by Django 5.1.2 on 2024-10-26 05:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ventas', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='producto',
            old_name='es_pack',
            new_name='es_promocion',
        ),
        migrations.AddField(
            model_name='producto',
            name='productos_en_promocion',
            field=models.ManyToManyField(blank=True, to='ventas.producto'),
        ),
        migrations.AlterField(
            model_name='producto',
            name='descripcion',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='producto',
            name='nombre',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='producto',
            name='precio',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
