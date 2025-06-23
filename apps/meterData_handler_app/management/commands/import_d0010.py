# class Command(BaseCommand):
#     help = 'Say hello'

#     def handle(self, *args, **kwargs):
#         self.stdout.write("Hello, world!")

from django.core.management.base import BaseCommand
from apps.meterData_handler_app.tasks.file_reader import file_reader


class Command(BaseCommand):
    help = 'Import D0010 flow file'

    def add_arguments(self, parser: BaseCommand) -> None:
        parser.add_argument('D0010file', nargs='+', type=str)


    def handle(self, *args, **options: dict) -> None:
        try:
        
            for D0010_file_path in options['D0010file']:  
                file_reader.delay(D0010_file_path)                            

                self.stdout.write(self.style.SUCCESS(f"Successfully imported - file is being processed{D0010_file_path}"))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"An unexpected error occurred: {str(e)}"))
            raise e
