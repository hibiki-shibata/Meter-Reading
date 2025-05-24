# from django.core.management.base import BaseCommand

# class Command(BaseCommand):
#     help = 'Say hello'

#     def handle(self, *args, **kwargs):
#         self.stdout.write("Hello, world!")

from django.core.management.base import BaseCommand
from apps.meterData_handler_app.models.models import MeterReading
from apps.meterData_handler_app.services.file_parser import parse_d0010

class Command(BaseCommand):
    help = 'Import D0010 flow file'

    def add_arguments(self, parser):
        parser.add_argument('D0010file', nargs='+', type=str)

    def handle(self, *args, **options):
        try:
        
            for D0010_file_path in options['D0010file']:
            
                for reading in parse_d0010(D0010_file_path):
                    # Check if the reading already exists
                    if MeterReading.objects.filter(
                        mpan=reading['mpan'],
                        meter_serial_number=reading['meter_serial_number'],
                        register_id=reading['register_id'],
                        reading_date=reading['reading_date'],
                        reading_value=reading['reading_value'],
                    ).exists():
                        # raise ValueError(f"Reading already exists: {reading}")
                        self.stdout.write(self.style.WARNING(f"Reading already exists: {reading}"))  
                        continue  

                
                    # Create a new MeterReading object
                    MeterReading.objects.create(
                        mpan=reading['mpan'],
                        meter_serial_number=reading['meter_serial_number'],
                        register_id=reading['register_id'],
                        reading_date=reading['reading_date'],
                        reading_value=reading['reading_value'],
                        file_name=reading['file_name'],
                    )
                self.stdout.write(self.style.SUCCESS(f"Successfully imported {D0010_file_path}"))
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f"File not found: {D0010_file_path}"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"An error occurred: {str(e)}"))

