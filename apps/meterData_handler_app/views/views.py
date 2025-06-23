# from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics , status

from rest_framework.mixins import ListModelMixin, CreateModelMixin

from apps.meterData_handler_app.models import MeterReading
from apps.meterData_handler_app.serializers.meterReadSerializer import reqMeterReadSerializer





class MeterDataHandlerView(generics.GenericAPIView, ListModelMixin, CreateModelMixin):
    queryset = MeterReading.objects.all()
    serializer_class = reqMeterReadSerializer

    def get(self, request, *args, **kwargs):
        try:                                    
            return self.list(request, *args, **kwargs)
        
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def post(self, request, *args, **kwargs):
        try:
            return self.create(request, *args, **kwargs)
        
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)