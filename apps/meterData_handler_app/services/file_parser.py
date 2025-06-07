# Parser logic for imported files, which is used in import_d0010.py


import csv
from datetime import datetime
import logging
from typing import Generator
from dataclasses import dataclass

from celery import shared_task

logger = logging.getLogger(__name__)

@dataclass
class MeterReadingData:
    mpan: str
    meter_serial_number: str
    register_id: str
    reading_date: datetime
    reading_value: float
    file_name: str


def parse_d0010(D0010_file_path) -> 'Generator[dict, None, None]':
        ignored_lines: set = {"ZHV", "ZPT"} 

        
        with open(D0010_file_path, 'r', newline='' ) as file:
            reader = csv.reader(file, delimiter='|')
            
            fileName: str = D0010_file_path.split('/')[-1] 
            current_mpan_core: str = None
            current_meter_serial_number: str = None

            expect026: bool = True
            expect028: bool = False
            expect030: bool = False

            for row in reader:
                if row[0] in ignored_lines:
                    continue

                if row[0] == '026':
                    if not expect026:
                        raise ValueError(f"Unexpected row 026 without preceding 028 in file {fileName} at line {reader.line_num}")
                    
                    current_mpan_core: str = row[1].strip()
                    expect026 = False
                    expect028 = True
                    expect030 = False
              

                elif row[0] == '028':
                    if not expect028:
                        raise ValueError(f"Unexpected row 028 without preceding 026 in file {fileName} at line {reader.line_num}")
                    
                    current_meter_serial_number: str = row[1].strip()
                    expect026 = False
                    expect028 = False
                    expect030 = True
                                 
                        
                elif row[0] == '030':
                    if not expect030:
                        raise ValueError(f"Unexpected row 030 without preceding 026 or 028 in file {fileName} at line {reader.line_num}")
                    
                    register_id: str = row[1].strip()
                    reading_date: datetime = datetime.strptime(row[2].strip(), "%Y%m%d%H%M%S").date()
                    reading_value: float = float(row[3].strip())   

                    if not current_mpan_core or not current_meter_serial_number or not register_id or not reading_date or reading_value is None:                 
                       raise ValueError(f"Missing MPAN core or meter serial number in file {fileName} at line {reader.line_num}")
                    
                    else:
                        yield  MeterReadingData (
                            mpan=current_mpan_core,
                            meter_serial_number=current_meter_serial_number,
                            register_id=register_id,
                            reading_date=reading_date,
                            reading_value=reading_value,
                            file_name=fileName
                                
                        )
                        
                    expect026 = True
                    expect028 = False
                    expect030 = True

                else:
                    raise ValueError(f"Unexpected row type {row[0]} in file {fileName} at line {reader.line_num}")
                

                
                
                
