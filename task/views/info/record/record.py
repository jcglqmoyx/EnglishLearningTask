from django.core import serializers
from rest_framework.response import Response
from rest_framework.views import APIView

from task.models.record import Record


class RecordView(APIView):
    def get(self, request):
        records = serializers.serialize('json', Record.objects.all()[:20])
        return Response({
            'result': "success",
            'data': records,
        })
