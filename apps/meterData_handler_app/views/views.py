# from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics , status

from rest_framework.mixins import ListModelMixin, CreateModelMixin

from rest_framework.views import APIView

from apps.meterData_handler_app.models import MeterReading
from apps.meterData_handler_app.serializers.meterReadSerializer import reqMeterReadSerializer

from apps.meterData_handler_app.tasks.file_reader import d0010_importer





class MeterDataHandlerView(generics.GenericAPIView, ListModelMixin, CreateModelMixin):
    queryset = MeterReading.objects.all()
    serializer_class = reqMeterReadSerializer

    def get(self, request, *args, **kwargs):
        try:                                    
            return self.list(request, *args, **kwargs)
        
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
        
class MeterFileCreateView(APIView):

    def post(self, request, *args, **kwargs):
        try:
            file = request.FILES.get("file")
            if not file:
                return Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)
                        
            d0010_importer(request.FILES["file"].read().decode('utf-8'), file.name)
            return Response({"message": "File is being processed"}, status=status.HTTP_202_ACCEPTED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
