from rest_framework import serializers
from apps.meterData_handler_app.models import MeterReading

import datetime


class reqMeterReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeterReading
        fields = [
            "mpan",
            "meter_serial_number",
            "register_id",
            "reading_date",
            "reading_value",
            "file_name",
        ]
        read_only_fields = ["register_id", "reading_date", "reading_value", "file_name"]
        extra = "forbid"
    


    def to_internal_value(self, data): # Avoid unexpected field
        allowed = set(self.fields.keys())
        incoming = set(data.keys())
        extra_field = allowed - incoming
        if extra_field:
            raise serializers.ValidationError(f"unexpected fields:", extra_field)
        return super().to_internal_value(data)
    

    def validate_mpan(self, value): # Field Level Validation
        if len(value) !=13 or not value.isdigit():
            raise serializers.ValidationError(
                "MPAN must be 13 numeric digit")
        return value
    

    def validate(self, data): # Object Level Validation
        if not data.get("meter_serial_number"):
            raise serializers.ValidationError(
                "Meter serial number is required")
        reading_date = data.get("reading_date")
        if reading_date and reading_date > datetime.today():
            raise serializers.ValidationError(
                "Reading date cannot be in the future")
        return data