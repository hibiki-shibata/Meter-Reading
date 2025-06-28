from django.db import models



class Meter(models.Model):
    mpan = models.CharField(max_length=13, unique=True, db_index=True)
    serial_number = models.CharField(max_length=10, unique=True, db_index=True)

class Register(models.Model):
    meter = models.ForeignKey(Meter, on_delete=models.CASCADE)
    register_id = models.CharField(max_length=2)
    
    class Meta:
        unique_together = [('meter', 'register_id')]

class MeterReading(models.Model):
    register = models.ForeignKey(Register, on_delete=models.CASCADE)
    reading_date = models.DateField()
    reading_value = models.DecimalField(max_digits=10, decimal_places=1)

    class Meta:
        unique_together = [('register', 'reading_date')]




# # D0010 model: D0010 data doc => https://www.electralink.co.uk/data-catalogues/dtc-catalogue/
# class MeterReading(models.Model):
#     mpan = models.CharField(max_length=13, db_index=True)
#     meter_serial_number = models.CharField(max_length=10, db_index=True)
#     register_id = models.CharField(max_length=2)
#     reading_date = models.DateField()
#     reading_value = models.DecimalField(max_digits=10, decimal_places=1)
#     file_name = models.CharField(max_length=100) 

#     class Meta:
#         unique_together = ('mpan', 'register_id', 'reading_date') # Ensure unique readings for each MPAN, register, and date