# from django.core.management.base import BaseCommand

# class Command(BaseCommand):
#     help = 'Say hello'

#     def handle(self, *args, **kwargs):
#         self.stdout.write("Hello, world!")

from django.core.management.base import BaseCommand
from apps.meterData_handler_app.models.models import FlowFile, MeterReading
from apps.meterData_handler_app.services.file_parser import parse_d0010

class Command(BaseCommand):
    help = 'Import D0010 flow file'

    def add_arguments(self, parser):
        parser.add_argument('D0010file', nargs='+', type=str)

    def handle(self, *args, **options):
        for D0010_file_path in options['D0010file']:
            filename = D0010_file_path.split('/')[-1]
            
            if FlowFile.objects.filter(file_name=filename).exists():
                self.stdout.write(self.style.WARNING(f"{filename} already imported"))
                continue

            flow_file = FlowFile.objects.create(file_name=filename)

           
            for reading in parse_d0010(D0010_file_path):
                # Check if the reading already exists
                if MeterReading.objects.filter(
                    mpan_core=reading['mpan_core'],
                    meter_serial_number=reading['meter_serial_number'],
                    register_id=reading['register_id'],
                    reading_date=reading['reading_date'],
                    reading_value=reading['reading_value'],
                ).exists():
                    self.stdout.write(self.style.WARNING(f"Reading already exists: {reading}"))
                    continue

                # Create a new MeterReading object
            
                MeterReading.objects.create(
                    mpan_core=reading['mpan_core'],
                    meter_serial_number=reading['meter_serial_number'],
                    register_id=reading['register_id'],
                    reading_date=reading['reading_date'],
                    reading_value=reading['reading_value'],
                    file_name=flow_file,
                )
            self.stdout.write(self.style.SUCCESS(f"Imported {filename}"))


# class FlowFile(models.Model):
#     file_name = models.CharField(max_length=100, unique=True)
#     created_at = models.DateTimeField(auto_now_add=True)


# # D0010 model: D0010 data doc => https://www.electralink.co.uk/data-catalogues/dtc-catalogue/
# class MeterReading(models.Model):
#     mpan_core = models.CharField(max_length=13)
#     meter_serial_number = models.CharField(max_length=10)
#     register_id = models.CharField(max_length=2)
#     reading_date = models.DateField()
#     meter_reading = models.DecimalField(max_digits=10, decimal_places=1)
#     file_name = models.ForeignKey(FlowFile, on_delete=models.CASCADE)