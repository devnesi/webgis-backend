# Generated by Django 3.2.19 on 2023-06-24 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0004_rename_maps_map'),
    ]

    operations = [
        migrations.AlterField(
            model_name='map',
            name='name',
            field=models.CharField(default='Unnamed map', max_length=3000),
        ),
    ]