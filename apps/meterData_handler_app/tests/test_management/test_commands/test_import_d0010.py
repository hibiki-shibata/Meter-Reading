from pathlib import Path
from django.core.management import call_command
from django.test import TestCase
from apps.meterData_handler_app.models import MeterReading
from datetime import date


class ImportD0010CommandTest(TestCase):


    def create_temp_file(self, content: str) -> Path: # Create a temporary file with the given content.
        file_path = Path("sampleFile.D0010").resolve() # Full Path
        file_path.write_text(content)
        return file_path

    def tearDown(self): 
        if hasattr(self, "file_path") and self.file_path.exists():
            self.file_path.unlink()
            # print(f"File deleted: {self.file_path}")
        else:
            print("No file to delete or file does not exist.")
   



    def test_successful_import_creates_reading(self):
        content = (
            "026|1234567890123|V|\n"
            "028|S123456789|C|\n"
            "030|01|20240520000000|1234.5|||T|N|\n"
        )

        self.file_path = self.create_temp_file(content)


        call_command('import_d0010', str(self.file_path))
        reading = MeterReading.objects.first()

        self.assertEqual(MeterReading.objects.count(), 1)
        self.assertEqual(reading.mpan, '1234567890123')
        self.assertEqual(reading.meter_serial_number, 'S123456789')
        self.assertEqual(reading.register_id, '01')
        self.assertEqual(reading.reading_date, date(2024, 5, 20))
        self.assertEqual(reading.reading_value, 1234.5)


    def test_duplicate_reading_is_skipped(self):
        content = (
            "026|1234567890123|V|\n"
            "028|S123456789|C|\n"
            "030|01|20240520000000|1234.5|||T|N|\n"
        )
        
        self.file_path = self.create_temp_file(content)

        call_command('import_d0010', str(self.file_path))
        call_command('import_d0010', str(self.file_path))

        self.assertEqual(MeterReading.objects.count(), 1)
        reading = MeterReading.objects.first()
        self.assertEqual(reading.reading_value, 1234.5)



# Error handling tests    
    def test_file_not_found(self):
        content = (
            "026|1234567890123|V|\n"
            "028|S123456789|C|\n"
            "030|01|20240520000000|1234.5|||T|N|\n"
        )
        self.file_path = self.create_temp_file(content)

        with self.assertRaises(FileNotFoundError):
              call_command('import_d0010', "missing_file.D0010")


    def test_parse_raises_missing_mpan_core(self):
            content = (
                "026||V|\n"
                "028|S123456789|C|\n"
                "030|01|20240520000000|1234.5|||T|N|\n"
            )
            self.file_path = self.create_temp_file(content)

            with self.assertRaises(ValueError) as cm:
                call_command('import_d0010', str(self.file_path))


    def test_parse_raises_missing_meter_serial_number(self):
        content = (
            "026|1234567890123|V|\n"
            "028||C|\n"
            "030|01|20240520000000|1234.5|||T|N|\n"
        )
        self.file_path = self.create_temp_file(content)

        with self.assertRaises(ValueError) as cm:
            call_command('import_d0010', str(self.file_path))


    def test_parse_raises_missing_register_id(self):
        content = (
            "026|1234567890123|V|\n"
            "028|S123456789|C|\n"
            "030||20240520000000|1234.5|||T|N|\n"
        )
        self.file_path = self.create_temp_file(content)

        with self.assertRaises(ValueError):
            call_command('import_d0010', str(self.file_path))

    def test_parse_raises_missing_reading_date(self):
        content = (
            "026|1234567890123|V|\n"
            "028|S123456789|C|\n"
            "030|01||1234.5|||T|N|\n"
        )
        self.file_path = self.create_temp_file(content)

        with self.assertRaises(ValueError):
            call_command('import_d0010', str(self.file_path))


    def test_parse_raises_missing_reading_value(self):
        content = (
            "026|1234567890123|V|\n"
            "028|S123456789|C|\n"
            "030|01|20240520000000|||T|N|\n"
        )
        self.file_path = self.create_temp_file(content)

        with self.assertRaises(ValueError):
            call_command('import_d0010', str(self.file_path))


    def test_unexpected_row_raises(self):
        content = (
            "026|1234567890123|V|\n"
            "028|S123456789|C|\n"
            "031|01|20240520000000|1234.5|||T|N|\n"  # Unexpected row type
        )
        self.file_path = self.create_temp_file(content)

        with self.assertRaises(ValueError):
            call_command('import_d0010', str(self.file_path))
