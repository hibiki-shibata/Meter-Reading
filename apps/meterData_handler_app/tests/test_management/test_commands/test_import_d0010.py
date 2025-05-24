

# import tempfile
# import os
# from unittest.mock import patch
# from django.core.management import call_command
# from django.test import TestCase
# from apps.meterData_handler_app.models.models import MeterReading

# class ImportD0010CommandTest(TestCase):

#     def setUp(self):
#         self.valid_data = [
#             {
#                 "mpan": "1234567890123",
#                 "meter_serial_number": "S123456789",
#                 "register_id": "01",
#                 "reading_date": "2024-05-20",
#                 "reading_value": 1234.5,
#                 "file_name": "test_file.d0010",
#             }
#         ]

#     @patch('apps.meterData_handler_app.management.commands.import_d0010.parse_d0010')
#     def test_import_creates_readings(self, mock_parser):
#         mock_parser.return_value = self.valid_data

#         temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".d0010")
#         temp_file.write(b"dummy data\n")
#         temp_file.close()

#         try:
#             call_command('import_d0010', temp_file.name)

#             # Assert data is saved
#             self.assertEqual(MeterReading.objects.count(), 1)
#             reading = MeterReading.objects.first()
#             self.assertEqual(reading.mpan, self.valid_data[0]["mpan"])
#             self.assertEqual(reading.meter_serial_number, self.valid_data[0]["meter_serial_number"])

#         finally:
#             os.unlink(temp_file.name)

#     @patch('apps.meterData_handler_app.management.commands.import_d0010.parse_d0010')
#     def test_duplicate_reading_skipped(self, mock_parser):
#         mock_parser.return_value = self.valid_data

#         # First import
#         call_command('import_d0010', 'fake_file_1.d0010')
#         self.assertEqual(MeterReading.objects.count(), 1)

#         # Second import — should skip duplicate
#         call_command('import_d0010', 'fake_file_1.d0010')
#         self.assertEqual(MeterReading.objects.count(), 1)

#     def test_missing_file_gracefully_handled(self):
#         result = self.capture_command_output('nonexistent_file.d0010')
#         self.assertIn("File not found", result)

#     def capture_command_output(self, file_path):
#         """Helper to capture stdout from the command"""
#         from io import StringIO
#         out = StringIO()
#         call_command('import_d0010', file_path, stdout=out)
#         return out.getvalue()
