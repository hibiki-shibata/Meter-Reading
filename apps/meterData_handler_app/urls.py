from django.urls import path
from apps.meterData_handler_app.views.views import MeterDataHandlerView, MeterFileCreateView

urlpatterns = [
    path('meterData/', MeterDataHandlerView.as_view(), name='meter_data_handler'),
    path('meterData/create/', MeterFileCreateView.as_view(), name='meter_file_create'),
]