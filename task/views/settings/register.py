from django.contrib.auth.models import User
from django.core.cache import cache
from rest_framework.response import Response
from rest_framework.views import APIView

from task.models.member import Member


class RegisterView(APIView):
    def post(self, request):
        data = request.POST
        username = data.get('username', '').strip()
        password = data.get('password', '').strip()
        if not username or not password or not cache.get(password + '_register'):
            return Response({
                'result': 'failed',
                'error_message': '用户名或密码不正确/密码失效，请重新尝试',
            })
        if User.objects.filter(username=username).exists():
            return Response({
                'result': 'failed',
                'error_message': '用户名已存在，请使用其他用户名',
            })
        user = User(username=username)
        user.set_password(password)
        user.save()
        Member.objects.create(user=user, wechat_id=password, group_id=1).save()
        return Response({
            'result': "success"
        })
