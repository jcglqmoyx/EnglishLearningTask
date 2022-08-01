import datetime

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from task.models.group import Group
from task.models.member import Member
from task.models.record import Record
from task.utils.datetime_util import get_beginning_of_day
from task.utils.report_util import generate_report


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

        groups = Group.objects.all()
        for group in groups:
            group_members = active_members.filter(group=group)
            if group_members.count() > 0:
                successful_members, rest_for_one_day_members, rest_for_two_days_members, failed_members = {}, {}, {}, {}
                for member in active_members:
                    records = Record.objects.filter(
                        member=member,
                        time__gte=beginning_of_yesterday,
                        time__lt=beginning_of_today,
                    )
                    username = member.user.username
                    if len(records) >= 2:
                        successful_members[username] = records
                    else:
                        if member.count_failure_in_a_week >= 2:
                            failed_members[username] = records
                        elif member.count_failure_in_a_week == 1:
                            rest_for_two_days_members[username] = records

                        elif member.count_failure_in_a_week == 0:
                            rest_for_one_day_members[username] = records

                        member.count_failure_in_a_week += 1
                        member.save()

                    if datetime.datetime.now().weekday() == 0:
                        member.count_failure_in_a_week = 0
                        member.save()
                for member in active_members:
                    username = member.user.username
                    if username not in successful_members \
                            and username not in rest_for_one_day_members \
                            and username not in rest_for_two_days_members \
                            and username not in failed_members:
                        failed_members[username] = []
                generate_report(group.id, successful_members, rest_for_one_day_members, rest_for_two_days_members, failed_members)
        return Response({
            'result': "success",
        })
