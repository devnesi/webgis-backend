# Generated by Django 3.2.19 on 2023-06-24 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('geometry', '0003_alter_geometry_table'),
    ]

    operations = [
        migrations.AddField(
            model_name='geometry',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='geometry',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
