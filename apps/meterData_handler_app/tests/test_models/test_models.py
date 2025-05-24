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




class MeterReadingMissingFieldTest(TestCase):

    def test_mpam_missing_required_fields(self): # mpan is missing
        readingMissField = MeterReading(
            meter_serial_number="A123456789",  
            register_id="01",
            reading_date=date(2024, 5, 20),
            reading_value=Decimal("1234.5"),
            file_name="flow_file_001.d0010"
        )
        with self.assertRaises(ValidationError):
            readingMissField.full_clean() 


    def test_serial_missing_required_fields(self): # meter_serial_number is missing
        readingMissField = MeterReading(
            mpan="1234567890123",
            register_id="01",
            reading_date=date(2024, 5, 20),
            reading_value=Decimal("1234.5"),
            file_name="flow_file_001.d0010"
        )
        with self.assertRaises(ValidationError):
            readingMissField.full_clean() 


    def test_registerid_missing_required_fields(self): # register_id is missing
        readingMissField = MeterReading(
            mpan="1234567890123",
            meter_serial_number="A123456789",
            reading_date=date(2024, 5, 20),
            reading_value=Decimal("1234.5"),
            file_name="flow_file_001.d0010"
        )
        with self.assertRaises(ValidationError):
            readingMissField.full_clean() 


    def test_readingDate_missing_required_fields(self): # reading_date is missing
        readingMissField = MeterReading(
            mpan="1234567890123",
            meter_serial_number="A123456789",
            register_id="01",
            reading_value=Decimal("1234.5"),
            file_name="flow_file_001.d0010"
        )
        with self.assertRaises(ValidationError):
            readingMissField.full_clean() 


    def test_readingValue_missing_required_fields(self): # reading_value is missing
        readingMissField = MeterReading(
            mpan="1234567890123",
            meter_serial_number="A123456789",
            register_id="01",
            reading_date=date(2024, 5, 20),
            file_name="flow_file_001.d0010"
        )
        with self.assertRaises(ValidationError):
            readingMissField.full_clean() 


    def test_fileName_missing_required_fields(self): # file_name is missing
        readingMissField = MeterReading(
            mpan="1234567890123",
            meter_serial_number="A123456789",
            register_id="01",
            reading_date=date(2024, 5, 20),
            reading_value=Decimal("1234.5"),
        )
        with self.assertRaises(ValidationError):
            readingMissField.full_clean() 





class MeterReadingFieldLengthTest(TestCase):

    def create_valid_reading(self, **overrides):
        data = {
            'mpan': '1234567890123',
            'meter_serial_number': 'ABC1234567',
            'register_id': '01',
            'reading_date': date(2024, 5, 24),
            'reading_value': Decimal('1234.5'),
            'file_name': 'test_file.d0010'
        }
        data.update(overrides)
        return MeterReading(**data)

    def test_mpan_too_long_raises(self):
        reading = self.create_valid_reading(mpan='1' * 14)  # 14 > max_length 13
        with self.assertRaises(ValidationError):
            reading.full_clean()

    def test_meter_serial_number_too_long_raises(self):
        reading = self.create_valid_reading(meter_serial_number='X' * 11)  # max_length = 10
        with self.assertRaises(ValidationError):
            reading.full_clean()

    def test_register_id_too_long_raises(self):
        reading = self.create_valid_reading(register_id='XYZ')  # max_length = 2
        with self.assertRaises(ValidationError):
            reading.full_clean()

    def test_file_name_too_long_raises(self): # file_name max_length = 100
        long_file_name = 'f' * 101
        reading = self.create_valid_reading(file_name=long_file_name)
        with self.assertRaises(ValidationError):
            reading.full_clean()

    def test_invalid_date_raises(self):
        reading = self.create_valid_reading(reading_date='not-a-date')
        with self.assertRaises(ValidationError):
            reading.full_clean()

    def test_invalid_reading_value_type_raises(self):
        reading = self.create_valid_reading(reading_value='not-a-decimal')
        with self.assertRaises(ValidationError):
            reading.full_clean()

