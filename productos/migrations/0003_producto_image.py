# Generated by Django 4.1.2 on 2022-12-06 15:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('productos', '0002_producto_delete_service'),
    ]

    operations = [
        migrations.AddField(
            model_name='producto',
            name='image',
            field=models.ImageField(null=True, upload_to='productos', verbose_name='Imagen'),
        ),
    ]