# Generated by Django 3.2.19 on 2023-06-25 15:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('form', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Field',
            fields=[
                ('id_form', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(default='Unnamed Form', max_length=3000)),
                ('type', models.CharField(choices=[('INTEGER', 'INTEGER'), ('DECIMAL', 'DECIMAL'), ('STRING', 'STRING')], default='STRING', max_length=7)),
                ('form', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='form.form')),
            ],
            options={
                'db_table': 'maps_layers_forms_fields',
                'ordering': ['pk'],
                'managed': True,
            },
        ),
    ]
