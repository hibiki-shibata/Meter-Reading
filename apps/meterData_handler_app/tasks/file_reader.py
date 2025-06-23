from celery import shared_task
import csv

from apps.meterData_handler_app.services.d0010_importer import d0010_importer



@shared_task(bind=True, max_retries=3, default_retry_delay=5, retry_backoff=True)
def file_reader(self, file_path):
    try:        
             with open(file_path, 'r', newline='') as file:
                readData = csv.reader(file, delimiter='|')            
                fileName: str = file_path.split('/')[-1]

                d0010_importer(readData, fileName)


    except FileNotFoundError:
        self.stdout.write(self.style.ERROR(f"File not found: {file_path}"))
        raise FileNotFoundError
    except Exception as e:
        self.stdout.write(self.style.ERROR(f"An unexpected error occurred: {str(e)}"))
        raise e

# better implement RETRY  by self.retry(exc=e, countdown=60) 