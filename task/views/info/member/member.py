from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from task.models.member import Member


class MemberView(APIView):
    permission_classes = ([IsAuthenticated])

    def get(self, request):
        user = request.user
        member = Member.objects.get(user=user)
        return Response({
            'result': 'success',
            'username': user.username,
            'last_login': user.last_login,
            'date_joined': user.date_joined,
            'is_active': member.is_active,

            'wechat_id': member.wechat_id,
            'quit_time': member.quit_time,
        })
