# Parser logic for imported files, which is used in import_d0010.py


import csv
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

def parse_d0010(D0010_file_path):
        
        with open(D0010_file_path, 'r') as file:
            reader = csv.reader(file, delimiter='|')
            
            fileName = D0010_file_path.split('/')[-1] 
            current_mpan_core = None
            current_meter_serial_number = None
            expect028: bool = False

            for row in reader:
                if row[0] == '026':
                    current_mpan_core = row[1].strip()
                    expect028 = True

                elif row[0] == '028':
                    if expect028:
                        current_meter_serial_number = row[1].strip()
                        expect028 = False
                    else:
                         logger.warning(f"Unexpected row 028 without preceding 026 in file {fileName} at line {reader.line_num}")
                        
                elif row[0] == '030':
                    register_id = row[1].strip()
                    reading_date = datetime.strptime(row[2].strip(), "%Y%m%d%H%M%S").date()
                    reading_value = float(row[3].strip())                    
                    yield {
                            'mpan': current_mpan_core,
                            'meter_serial_number': current_meter_serial_number,
                            'register_id': register_id,
                            'reading_date': reading_date,
                            'reading_value': reading_value,
                            'file_name': fileName,
                        }
                    expect028 = False