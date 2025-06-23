from typing import Generator
from datetime import datetime
from dataclasses import dataclass

@dataclass
class MeterReadingData:
    mpan: str
    meter_serial_number: str
    register_id: str
    reading_date: datetime
 

def d0010_parser(D0010_data: dict, file_name: str) -> Generator[dict, None, None]:
            ignored_lines: set = {"ZHV", "ZPT"}
            
            expect026: bool = True
            expect028: bool = False
            expect030: bool = False

            for row in D0010_data:
                if row[0] in ignored_lines:
                    continue

                if row[0] == '026':
                    if not expect026:
                        raise ValueError(f"Unexpected row 026 without preceding 028 in file {file_name} at line {D0010_data}")
                    
                    mpan: str = row[1].strip()
                    expect026 = False
                    expect028 = True
                    expect030 = False
              

                elif row[0] == '028':
                    if not expect028:
                        raise ValueError(f"Unexpected row 028 without preceding 026 in file {file_name} at line {D0010_data}")
                    
                    meter_serial_number: str = row[1].strip()
                    expect026 = False
                    expect028 = False
                    expect030 = True
                                 
                        
                elif row[0] == '030':
                    if not expect030:
                        raise ValueError(f"Unexpected row 030 without preceding 026 or 028 in file {file_name} at line {D0010_data}")
                    
                    register_id: str = row[1].strip()
                    reading_date: datetime = datetime.strptime(row[2].strip(), "%Y%m%d%H%M%S").date()
                    reading_value: float = float(row[3].strip())   

                    if not mpan or not meter_serial_number or not register_id or not reading_date or reading_value is None:                 
                       raise ValueError(f"Missing MPAN core or meter serial number in file {file_name} at line {D0010_data}")
                    
                    else:
                        yield  MeterReadingData (
                            mpan=mpan,
                            meter_serial_number=meter_serial_number,
                            register_id=register_id,
                            reading_date=reading_date,
                            reading_value=reading_value,
                            file_name=file_name
                                
                        )
                        
                    expect026 = True
                    expect028 = False
                    expect030 = True

                else:
                    raise ValueError(f"Unexpected row type {row[0]} in file {file_name} at line {D0010_data}")
