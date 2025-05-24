from django.contrib import admin

# # Register your models here.
from .models.models import MeterReading, FlowFile


@admin.register(MeterReading)
class MeterReadingAdmin(admin.ModelAdmin):
    list_display = (
        "mpan_core",
        "meter_serial_number",
        "reading_date",
        "reading_value",
        "file_name",
    )
    search_fields = ("mpan_core", "meter_serial_number")


# @admin.register(FlowFile)
# class FlowFileAdmin(admin.ModelAdmin):
#     list_display = ("file_name", "created_at")
#     search_fields = ("file_name",)
