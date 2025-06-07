from apps.meterData_handler_app.models.models import MeterReading
from apps.meterData_handler_app.services.file_parser import parse_d0010
from apps.meterData_handler_app.services.file_parser import MeterReadingData
from celery import shared_task

reading: MeterReadingData


@shared_task(bind=True, max_retries=3, default_retry_delay=5)
def import_meterread_file(self, D0010_file_path):
    try:        

                for reading in parse_d0010(D0010_file_path):
       
                    # Check if the reading already exists
                    if MeterReading.objects.filter(
                        mpan=reading.mpan,
                        meter_serial_number=reading.meter_serial_number,
                        register_id=reading.register_id,
                        reading_date=reading.reading_date,
                        reading_value=reading.reading_value,
                    ).exists():
                        # raise ValueError(f"Reading already exists: {reading}")
                        self.stdout.write(self.style.WARNING(f"Reading already exists: {reading}"))  
                        continue  

                
                    # Create a new MeterReading object
                    MeterReading.objects.create(
                        mpan=reading.mpan,
                        meter_serial_number=reading.meter_serial_number,
                        register_id=reading.register_id,
                        reading_date=reading.reading_date,
                        reading_value=reading.reading_value,
                    )
                self.stdout.write(self.style.SUCCESS(f"Successfully imported {D0010_file_path}"))

    except FileNotFoundError:
        self.stdout.write(self.style.ERROR(f"File not found: {D0010_file_path}"))
        raise FileNotFoundError
    except Exception as e:
        self.stdout.write(self.style.ERROR(f"An unexpected error occurred: {str(e)}"))
        raise e
# better implement RETRY  by self.retry(exc=e, countdown=60) 