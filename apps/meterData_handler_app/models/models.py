from django.db import models

class FlowFile(models.Model):
    file_name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)


# D0010 model: D0010 data doc => https://www.electralink.co.uk/data-catalogues/dtc-catalogue/
class MeterReading(models.Model):
    mpan_core = models.CharField(max_length=13)
    meter_serial_number = models.CharField(max_length=10)
    register_id = models.CharField(max_length=2)
    reading_date = models.DateField()
    meter_reading = models.DecimalField(max_digits=10, decimal_places=1)
    file_name = models.ForeignKey(FlowFile, on_delete=models.CASCADE)
    



        
