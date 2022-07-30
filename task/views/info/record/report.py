import datetime

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from task.utils.report_util import generate_report
from task.models.member import Member
from task.models.record import Record
from task.utils.datetime_util import get_beginning_of_day


class ReportView(APIView):
    permission_classes = ([IsAuthenticated])

    def get(self, request):
        if not request.user.is_superuser:
            return Response({
                'result': 'failed',
                'error_message': '权限不足, 此操作只能由管理员进行',
            })
        now = datetime.datetime.now()
        beginning_of_yesterday = get_beginning_of_day(now - datetime.timedelta(days=1))
        beginning_of_today = get_beginning_of_day(now)

        active_members = Member.objects.filter(is_active=True)
        competent_members, incompetent_members = {}, {}
        for member in active_members:
            records = Record.objects.filter(
                member=member,
                time__gte=beginning_of_yesterday,
                time__lt=beginning_of_today,
            )
            username = member.user.username
            if len(records) >= 2:
                competent_members[username] = records
            else:
                incompetent_members[username] = records
        for member in active_members:
            username = member.user.username
            if username not in competent_members and username not in incompetent_members:
                incompetent_members[username] = []
        generate_report(competent_members, incompetent_members)
        return Response({
            'result': "success",
        })
