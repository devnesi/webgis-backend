# Generated by Django 3.2.19 on 2023-06-24 12:40

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('map', '0003_auto_20230624_1238'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Maps',
            new_name='Map',
        ),
    ]
