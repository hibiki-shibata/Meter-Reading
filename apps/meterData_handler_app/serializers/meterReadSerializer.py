from rest_framework import serializers
from apps.meterData_handler_app.models import MeterReading


class reqMeterReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeterReading
        fields = ['mpan', 'meter_serial_number', 'register_id', 'reading_date', 'reading_value', 'file_name']
        read_only_fields = ['register_id', 'reading_date', 'reading_value', 'file_name']