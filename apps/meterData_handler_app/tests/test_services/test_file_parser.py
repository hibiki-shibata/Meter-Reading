import os
import tempfile
from datetime import date
from django.test import TestCase
from apps.meterData_handler_app.services.file_parser import parse_d0010


class ParseD0010TestCase(TestCase):

    def create_temp_file(self, content: str) -> str: # Create a temporary file with the given content.
        temp_file = tempfile.NamedTemporaryFile(delete=False, mode='w', suffix='.d0010')
        temp_file.write(content)
        temp_file.close()
        return temp_file.name

    def tearDown(self): 
        """Ensure all temp files are cleaned up automatically if set in tests."""
        for f in getattr(self, "_temp_files", []):
            if os.path.exists(f):
                os.remove(f)

    def _track_temp_file(self, path: str):
        """Track files for cleanup."""
        if not hasattr(self, "_temp_files"):
            self._temp_files = []
        self._temp_files.append(path)
        return path


# Valid test cases
    def test_valid_d0010_file_parses_single_record(self):
        content = (
            "026|1234567890123|V|\n"
            "028|S123456789|C|\n"
            "030|01|20240520000000|1234.5|||T|N|\n"
        )
        file_path = self._track_temp_file(self.create_temp_file(content))

        results = list(parse_d0010(file_path))
        self.assertEqual(len(results), 1)

        result = results[0]
        self.assertEqual(result['mpan'], '1234567890123')
        self.assertEqual(result['meter_serial_number'], 'S123456789')
        self.assertEqual(result['register_id'], '01')
        self.assertEqual(result['reading_date'], date(2024, 5, 20))
        self.assertEqual(result['reading_value'], 1234.5)
        self.assertEqual(result['file_name'], os.path.basename(file_path))

    def test_multiple_030_entries_parsed(self):
        content = (
            "026|1234567890123|V|\n"
            "028|S123456789|C|\n"
            "030|01|20240520000000|100.0|||T|N|\n"
            "030|02|20240521000000|200.0|||T|N|\n"
        )
        file_path = self._track_temp_file(self.create_temp_file(content))

        results = list(parse_d0010(file_path))
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0]['reading_value'], 100.0)
        self.assertEqual(results[1]['reading_value'], 200.0)


# Invalid test cases    
    def test_unexpected_028_without_026_raises(self):
        content = (
            "028|S123456789|C|\n"
            "030|01|20240520000000|1234.5|||T|N|\n"
        )
        file_path = self._track_temp_file(self.create_temp_file(content))

        with self.assertRaises(ValueError) as cm:
            list(parse_d0010(file_path))
        # self.assertIn("Unexpected row 028 without preceding 026", str(cm.exception))

    def test_invalid_date_format_raises(self):
        content = (
            "026|1234567890123|V|\n"
            "028|S123456789|C|\n"
            "030|01|2024/05/20|1234.5|||T|N|\n"
        )
        file_path = self._track_temp_file(self.create_temp_file(content))

        with self.assertRaises(ValueError):
            list(parse_d0010(file_path))



# Missing data test cases
    def test_missing_epam_core_raises(self):
        content = (
            "026||V|\n"
            "028|S123456789|C|\n"
            "030|01|20240520000000|1234.5|||T|N|\n"
        )
        file_path = self._track_temp_file(self.create_temp_file(content))

        with self.assertRaises(ValueError) as cm:
            list(parse_d0010(file_path))

    def test_missing_meter_serial_number_raises(self):
        content = (
            "026|1234567890123|V|\n"
            "028||C|\n"
            "030|01|20240520000000|1234.5|||T|N|\n"
        )
        file_path = self._track_temp_file(self.create_temp_file(content))

        with self.assertRaises(ValueError) as cm:
            list(parse_d0010(file_path))
    
    def test_missing_register_id_raises(self):
        content = (
            "026|1234567890123|V|\n"
            "028|S123456789|C|\n"
            "030||20240520000000|1234.5|||T|N|\n"
        )
        file_path = self._track_temp_file(self.create_temp_file(content))

        with self.assertRaises(ValueError):
            list(parse_d0010(file_path))

    def test_missing_reading_date_raises(self):
        content = (
            "026|1234567890123|V|\n"
            "028|S123456789|C|\n"
            "030|01||1234.5|||T|N|\n"
        )
        file_path = self._track_temp_file(self.create_temp_file(content))

        with self.assertRaises(ValueError):
            list(parse_d0010(file_path))

    def test_missing_reading_value_raises(self):
        content = (
            "026|1234567890123|V|\n"
            "028|S123456789|C|\n"
            "030|01|20240520000000|||T|N|\n"
        )
        file_path = self._track_temp_file(self.create_temp_file(content))

        with self.assertRaises(ValueError):
            list(parse_d0010(file_path))
    
  
        
