from rest_framework.response import Response
from rest_framework.views import APIView

from task.models.group import Group


class GroupCountView(APIView):
    def get(self, request):
        return Response({
            'result': 'success',
            'group_count': Group.objects.all().count(),
        })
