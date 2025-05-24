# Doc: https://docs.djangoproject.com/en/5.2/ref/contrib/admin/#the-register-decorator

from django.contrib import admin
# # Register your models here.
from .models.models import MeterReading


@admin.register(MeterReading)
class MeterReadingAdmin(admin.ModelAdmin):
    list_display = (
        "mpan",
        "meter_serial_number",
        "reading_date",
        "reading_value",
        "file_name",
    )
    search_fields = ("mpan", "meter_serial_number")


