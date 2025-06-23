from django.db import models


# D0010 model: D0010 data doc => https://www.electralink.co.uk/data-catalogues/dtc-catalogue/
class MeterReading(models.Model):
    mpan = models.CharField(max_length=13, db_index=True)
    meter_serial_number = models.CharField(max_length=10, db_index=True)
    register_id = models.CharField(max_length=2)
    reading_date = models.DateField()
    reading_value = models.DecimalField(max_digits=10, decimal_places=1)
    file_name = models.CharField(max_length=100) 

    class Meta:
        unique_together = ('mpan', 'register_id', 'reading_date') # Ensure unique readings for each MPAN, register, and date