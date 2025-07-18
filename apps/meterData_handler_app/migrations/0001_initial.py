# Generated by Django 5.2.1 on 2025-05-23 17:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='flowFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_name', models.CharField(max_length=100, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='MeterReading',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mpan_core', models.CharField(max_length=13)),
                ('meter_serial_number', models.CharField(max_length=10)),
                ('register_id', models.CharField(max_length=2)),
                ('reading_date', models.DateField()),
                ('meter_reading', models.DecimalField(decimal_places=1, max_digits=10)),
                ('file_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='meterData_handler_app.flowfile')),
            ],
        ),
    ]
