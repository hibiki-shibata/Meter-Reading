# Parser logic for imported files, which is used in import_d0010.py

from typing import Generator
from apps.meterData_handler_app.services.d0010_parser import d0010_parser
from apps.meterData_handler_app.models.models import MeterReading


def d0010_importer(read_data, file_name) -> 'Generator[dict, None, None]':

            for reading in d0010_parser(read_data, file_name):

                    if MeterReading.objects.filter(
                        mpan=reading.mpan,
                        meter_serial_number=reading.meter_serial_number,
                        register_id=reading.register_id,
                        reading_date=reading.reading_date,
                        reading_value=reading.reading_value,
                    ).exists():
                        # raise ValueError(f"Reading already exists: {reading}")
                        print(f"Reading already exists: {reading}")                        
                        continue  

                
                    # Create a new MeterReading object
                    MeterReading.objects.create(
                        mpan=reading.mpan,
                        meter_serial_number=reading.meter_serial_number,
                        register_id=reading.register_id,
                        reading_date=reading.reading_date,
                        reading_value=reading.reading_value,
                    )

            print(f"Successfully imported {file_name}")
