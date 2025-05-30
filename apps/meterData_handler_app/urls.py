from django.urls import path
from apps.meterData_handler_app.views.views import MeterDataHandlerView

urlpatterns = [
    path('meterData/', MeterDataHandlerView.as_view(), name='meter_data_handler'),
]
 