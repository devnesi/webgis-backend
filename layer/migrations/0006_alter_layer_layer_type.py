# Generated by Django 3.2.19 on 2023-06-24 16:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('layer', '0005_auto_20230624_1254'),
    ]

    operations = [
        migrations.AlterField(
            model_name='layer',
            name='layer_type',
            field=models.CharField(choices=[('POLYGON', 'POLYGON'), ('POINT', 'POINT'), ('LINE', 'LINE'), ('GEOMETRY', 'GEOMETRY')], default='GEOMETRY', max_length=8),
        ),
    ]
