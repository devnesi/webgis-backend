# Generated by Django 3.2.19 on 2023-06-24 12:37

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('map', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Map',
            new_name='Maps',
        ),
    ]
