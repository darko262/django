# Generated by Django 4.1.2 on 2022-12-22 20:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('productos', '0007_rename_slug_producto_slug2'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='producto',
            name='categories',
        ),
        migrations.AddField(
            model_name='producto',
            name='categories',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='productos.category', verbose_name='Categorias'),
        ),
    ]
