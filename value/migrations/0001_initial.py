# Generated by Django 3.2.19 on 2023-06-25 16:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('geometry', '0004_auto_20230624_1252'),
        ('field', '0002_alter_field_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='Value',
            fields=[
                ('id_value', models.AutoField(primary_key=True, serialize=False)),
                ('varchar_value', models.CharField(blank=True, max_length=3000, null=True)),
                ('number_value', models.FloatField(blank=True, null=True)),
                ('field', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='field.field')),
                ('geometry', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='geometry.geometry')),
            ],
            options={
                'db_table': 'maps_layers_forms_fields_values',
                'ordering': ['pk'],
                'managed': True,
            },
        ),
    ]
