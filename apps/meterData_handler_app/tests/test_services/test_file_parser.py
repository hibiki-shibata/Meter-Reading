import os
from pathlib import Path

from datetime import date
from django.test import TestCase
from apps.meterData_handler_app.services.d0010_importer import parse_d0010


class ParseD0010TestCase(TestCase):

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





# Valid test cases
    def test_valid_d0010_file_parses_single_record(self):
        content = (
            "026|1234567890123|V|\n"
            "028|S123456789|C|\n"
            "030|01|20240520000000|1234.5|||T|N|\n"
        )
        
        self.file_path = self.create_temp_file(content)

        results = list(parse_d0010(str(self.file_path)))
        self.assertEqual(len(results), 1)

        result = results[0]
        self.assertEqual(result['mpan'], '1234567890123')
        self.assertEqual(result['meter_serial_number'], 'S123456789')
        self.assertEqual(result['register_id'], '01')
        self.assertEqual(result['reading_date'], date(2024, 5, 20))
        self.assertEqual(result['reading_value'], 1234.5)
        self.assertEqual(result['file_name'], os.path.basename(self.file_path))


    def test_multiple_030_entries_parsed(self):
        content = (
            "026|1234567890123|V|\n"
            "028|S123456789|C|\n"
            "030|01|20240520000000|100.0|||T|N|\n"
            "030|02|20240521000000|200.0|||T|N|\n"
        )
        self.file_path = self.create_temp_file(content)

        results = list(parse_d0010(str(self.file_path)))
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0]['reading_value'], 100.0)
        self.assertEqual(results[1]['reading_value'], 200.0)


# Invalid test cases    
    def test_invalid_date_format_raises(self):
        content = (
            "026|1234567890123|V|\n"
            "028|S123456789|C|\n"
            "030|01|2024/05/20|1234.5|||T|N|\n"
        )
        self.file_path = self.create_temp_file(content)

        with self.assertRaises(ValueError):
            list(parse_d0010(str(self.file_path)))

    def test_unexpected_row_type_raises(self):
        content = (
            "026|1234567890123|V|\n"
            "028|S123456789|C|\n"
            "031|01|20240520000000|1234.5|||T|N|\n"
        )
        self.file_path = self.create_temp_file(content)

        with self.assertRaises(ValueError) as cm:
            list(parse_d0010(str(self.file_path)))


# Unexpected row test row test cases:
    def test_026_only_raises(self):
        content = (
            "026|1234567890123|V|\n"
        )
        self.file_path = self.create_temp_file(content)

        result = list(parse_d0010(str(self.file_path)))
        self.assertEqual(result, [])


    def test_028_only_raises(self):
        content = (
            "028|S123456789|C|\n"
        )
        self.file_path = self.create_temp_file(content)

        with self.assertRaises(ValueError):
            list(parse_d0010(str(self.file_path)))


    def test_030_only_raises(self):
        content = (
            "030|01|20240520000000|||T|N|\n"
        )
        self.file_path = self.create_temp_file(content)

        with self.assertRaises(ValueError):
            list(parse_d0010(str(self.file_path)))

    
    def test_only_026_and_028_raises(self):
        content = (
            "026|1234567890123|V|\n"
            "028|S123456789|C|\n"
        )
        self.file_path = self.create_temp_file(content)

        result = list(parse_d0010(str(self.file_path)))
        self.assertEqual(result, [])


    def test_026_to_030_raises(self):
        content = (
            "026|1234567890123|V|\n"
            "030|01|20240520000000|||T|N|\n"
        )
        self.file_path = self.create_temp_file(content)

        with self.assertRaises(ValueError):
            list(parse_d0010(str(self.file_path)))


    def test_026_to_028_to_026_raises(self):
        content = (
            "026|1234567890123|V|\n"
            "028|S123456789|C|\n"
            "026|9876543210987|V|\n"
        )
        self.file_path = self.create_temp_file(content)

        with self.assertRaises(ValueError):
            list(parse_d0010(str(self.file_path)))


    def test_026_to_028_to_030_to_028_raises(self):
        content = (
            "026|1234567890123|V|\n"
            "028|S123456789|C|\n"
            "030|01|20240520000000|||T|N|\n"
            "028|S987654321|C|\n"
        )
        self.file_path = self.create_temp_file(content)

        with self.assertRaises(ValueError):
            list(parse_d0010(str(self.file_path)))


    def test_unexpected_028_without_026_raises(self):
        content = (
            "028|S123456789|C|\n"
            "030|01|20240520000000|1234.5|||T|N|\n"
        )
        self.file_path = self.create_temp_file(content)

        with self.assertRaises(ValueError):
            list(parse_d0010(str(self.file_path)))
        # self.assertIn("Unexpected row 028 without preceding 026", str(cm.exception))



# Missing data test cases
    def test_missing_epam_core_raises(self):
        content = (
            "026||V|\n"
            "028|S123456789|C|\n"
            "030|01|20240520000000|1234.5|||T|N|\n"
        )
        self.file_path = self.create_temp_file(content)

        with self.assertRaises(ValueError) as cm:
            list(parse_d0010(str(self.file_path)))


    def test_missing_meter_serial_number_raises(self):
        content = (
            "026|1234567890123|V|\n"
            "028||C|\n"
            "030|01|20240520000000|1234.5|||T|N|\n"
        )
        self.file_path = self.create_temp_file(content)

        with self.assertRaises(ValueError) as cm:
            list(parse_d0010(str(self.file_path)))
    

    def test_missing_register_id_raises(self):
        content = (
            "026|1234567890123|V|\n"
            "028|S123456789|C|\n"
            "030||20240520000000|1234.5|||T|N|\n"
        )
        self.file_path = self.create_temp_file(content)

        with self.assertRaises(ValueError):
            list(parse_d0010(str(self.file_path)))


    def test_missing_reading_date_raises(self):
        content = (
            "026|1234567890123|V|\n"
            "028|S123456789|C|\n"
            "030|01||1234.5|||T|N|\n"
        )
        self.file_path = self.create_temp_file(content)

        with self.assertRaises(ValueError):
            list(parse_d0010(str(self.file_path)))


    def test_missing_reading_value_raises(self):
        content = (
            "026|1234567890123|V|\n"
            "028|S123456789|C|\n"
            "030|01|20240520000000|||T|N|\n"
        )
        self.file_path = self.create_temp_file(content)

        with self.assertRaises(ValueError):
            list(parse_d0010(str(self.file_path)))



    
  
        
