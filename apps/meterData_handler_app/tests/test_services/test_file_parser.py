import os
import tempfile
from datetime import date
from django.test import TestCase
from apps.meterData_handler_app.services.file_parser import parse_d0010


class ParseD0010Tests(TestCase):

    def create_temp_file(self, content: str) -> str:
        tmp = tempfile.NamedTemporaryFile(delete=False, mode="w", suffix=".d0010")
        tmp.write(content)
        tmp.close()
        return tmp.name

    def test_valid_file_parses_correctly(self):
        content = (
            "026|1234567890123|V|\n"
            "028|S123456789|C|\n"
            "030|01|20240520000000|1234.5|||T|N|\n"
        )
        file_path = self.create_temp_file(content)

        try:
            results = list(parse_d0010(file_path))
            self.assertEqual(len(results), 1)
            reading = results[0]

            self.assertEqual(reading['mpan'], "1234567890123")
            self.assertEqual(reading['meter_serial_number'], "S123456789")
            self.assertEqual(reading['register_id'], "01")
            self.assertEqual(reading['reading_date'], date(2024, 5, 20))
            self.assertEqual(reading['reading_value'], 1234.5)
            self.assertEqual(reading['file_name'], os.path.basename(file_path))
        finally:
            os.unlink(file_path)

    def test_multiple_030_readings(self):
        content = (
            "026|1234567890123|V|\n"
            "028|S123456789|C|\n"
            "030|01|20240520000000|100.0|||T|N|\n"
            "030|02|20240521000000|200.0|||T|N|\n"
        )
        file_path = self.create_temp_file(content)

        try:
            results = list(parse_d0010(file_path))
            self.assertEqual(len(results), 2)
            self.assertEqual(results[1]['reading_value'], 200.0)
        finally:
            os.unlink(file_path)

    def test_028_without_026_raises_error(self):
        content = (
            "028|S123456789|C|\n"
            "030|01|20240520000000|100.0|||T|N|\n"
        )
        file_path = self.create_temp_file(content)

        try:
            with self.assertRaises(ValueError) as context:
                list(parse_d0010(file_path))
            self.assertIn("Unexpected row 028 without preceding 026", str(context.exception))
        finally:
            os.unlink(file_path)

    def test_030_without_028_uses_previous_serial(self):
        content = (
            "026|1234567890123|V|\n"
            "028|S123456789|C|\n"
            "030|01|20240520000000|100.0|||T|N|\n"
            "030|02|20240521000000|200.0|||T|N|\n"
        )
        file_path = self.create_temp_file(content)

        try:
            results = list(parse_d0010(file_path))
            for reading in results:
                self.assertEqual(reading['meter_serial_number'], "S123456789")
        finally:
            os.unlink(file_path)

    def test_invalid_date_format_raises(self):
        content = (
            "026|1234567890123|V|\n"
            "028|S123456789|C|\n"
            "030|01|2024-05-20|1234.5|||T|N|\n"
        )
        file_path = self.create_temp_file(content)

        try:
            with self.assertRaises(ValueError):
                list(parse_d0010(file_path))
        finally:
            os.unlink(file_path)

    def test_missing_reading_value_raises(self):
        content = (
            "026|1234567890123|V|\n"
            "028|S123456789|C|\n"
            "030|01|20240520000000|||T|N|\n"
        )
        file_path = self.create_temp_file(content)

        try:
            with self.assertRaises(ValueError):
                list(parse_d0010(file_path))
        finally:
            os.unlink(file_path)
