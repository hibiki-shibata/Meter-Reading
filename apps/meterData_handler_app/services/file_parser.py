# Parser logic for imported files, which is used in import_d0010.py


import csv
from typing import Generator
from d0010_handler import d0010_handler, MeterReadingData




def parse_files(D0010_file_path) -> 'Generator[dict, None, None]':

        
        with open(D0010_file_path, 'r', newline='' ) as file:            

            readData = csv.reader(file, delimiter='|')            
            fileName: str = D0010_file_path.split('/')[-1]

            for reading in d0010_handler(readData, fileName):
                  yield MeterReadingData (
                        mpan=reading.mpan,
                        meter_serial_number=reading.meter_serial_number,
                        register_id=reading.register_id,
                        reading_date=reading.reading_date,
                        reading_value=reading.reading_value,
                        file_name=reading.file_name
                  )
