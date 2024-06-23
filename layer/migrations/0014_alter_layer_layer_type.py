# Generated by Django 3.2.19 on 2024-06-23 01:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('layer', '0013_layer_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='layer',
            name='layer_type',
            field=models.CharField(choices=[('Polygon', 'Polygon'), ('Point', 'Point'), ('LineString', 'LineString'), ('Geom', 'Geometry')], default='Geom', max_length=15),
        ),
    ]