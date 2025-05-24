# Test for apps/meterData_handler_app/models/models.py

from django.test import TestCase
from apps.meterData_handler_app.models import MeterReading
from datetime import date
from decimal import Decimal

from django.core.exceptions import ValidationError

class MeterReadingModelTest(TestCase):

    def setUp(self):
        self.reading = MeterReading.objects.create(
            mpan="1234567890123",
            meter_serial_number="A123456789",
            register_id="01",
            reading_date=date(2024, 5, 20),
            reading_value=Decimal("1234.5"),
            file_name="flow_file_001.d0010"
        )

    def test_meter_reading_created_successfully(self):
        self.assertEqual(MeterReading.objects.count(), 1)

    def test_fields_are_stored_correctly(self):
        reading = self.reading
        self.assertEqual(reading.mpan, "1234567890123")
        self.assertEqual(reading.meter_serial_number, "A123456789")
        self.assertEqual(reading.register_id, "01")
        self.assertEqual(reading.reading_date, date(2024, 5, 20))
        self.assertEqual(reading.reading_value, Decimal("1234.5"))
        self.assertEqual(reading.file_name, "flow_file_001.d0010")

    def test_mpan_field_length(self):
        reading = self.reading
        self.assertEqual(len(reading.mpan), 13)

    def test_meter_serial_number_max_length(self):
        reading = self.reading
        self.assertTrue(len(reading.meter_serial_number) <= 10)


    def test_missing_required_fields(self):
        readingMissField = MeterReading(
            meter_serial_number="A123456789",  # mpan is missing
            register_id="01",
            reading_date=date(2024, 5, 20),
            reading_value=Decimal("1234.5"),
            file_name="flow_file_001.d0010"
        )
        with self.assertRaises(ValidationError):
            readingMissField.full_clean() 


    def test_too_long_mpan_fails(self):
        readingTooLongField = MeterReading(
            mpan="1" * 14,  # too long
            meter_serial_number="A123456789",
            register_id="01",
            reading_date=date(2024, 5, 20),
            reading_value=Decimal("1234.5"),
            file_name="flow_file_001.d0010"
        )
        
        with self.assertRaises(ValidationError):
            readingTooLongField.full_clean()

