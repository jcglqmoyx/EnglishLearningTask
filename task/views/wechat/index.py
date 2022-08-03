import hashlib
import time
from datetime import timedelta

import xmltodict
from django.contrib.auth.models import User
from django.core.cache import cache
from django.shortcuts import HttpResponse
from django.utils.timezone import now
from rest_framework.response import Response
from rest_framework.views import APIView

from task.models.group import Group
from task.models.member import Member
from task.models.record import Record

WECHAT_TOKEN = 'test'


class WechatView(APIView):
    def get(self, request):
        args = request.GET
        signature = args.get('signature')
        echostr = args.get('echostr')
        timestamp = args.get('timestamp')
        nonce = args.get('nonce')
        temp = [WECHAT_TOKEN, timestamp, nonce]
        temp.sort()
        temp = "".join(temp)
        m = hashlib.sha1()
        m.update(temp.encode('utf8'))
        sig = m.hexdigest()

        if sig == signature:
            if request.method == "GET":
                return HttpResponse(echostr)
        else:
            return 'errno', 403

    def post(self, request):
        request_body = request.body
        data = xmltodict.parse(request_body).get('xml')

        message_type = data['MsgType']
        wechat_id = data['FromUserName']

        response = {
            "ToUserName": wechat_id,
            "FromUserName": data['ToUserName'],
            "CreateTime": int(time.time()),
            "MsgType": "text",
        }
        if message_type == 'text':
            content = data['Content']
            if content == 'p':
                response['Content'] = wechat_id
                cache.set(wechat_id + '_register', True, 3600)
            # 补卡
            elif content == 'm':
                cache.set(wechat_id, True, 20)
                response['Content'] = '开始补卡, 请在20秒内上传昨天的打卡图片..'
            elif content[:2] == 'r ' and len(content) > 2:
                username = content[2:]
                if Member.objects.filter(wechat_id=wechat_id).exists():
                    response['Content'] = '你已经注册过了, 你的用户名为%s, 请不要重复注册' % Member.objects.get(
                        wechat_id=wechat_id).user.username
                elif User.objects.filter(username=username).exists():
                    response['Content'] = '用户名已存在, 请换一个用户名'
                else:
                    group = Group.objects.all().order_by('-id').first()
                    user = User(username=username)
                    user.set_password(wechat_id)
                    user.save()
                    Member.objects.create(user=user, wechat_id=wechat_id, group=group).save()
                    response['Content'] = '注册成功。你的用户名为: %s, 请联系管理员激活账号' % username
            else:
                response['Content'] = '欢迎使用打卡系统, 请输入"r 用户名"开始注册, 注册成功后，请联系管理员激活账号'

        elif message_type == 'image':
            member = Member.objects.filter(wechat_id=wechat_id).first()
            if not member:
                response['Content'] = '尚未注册'
            elif not member.is_active:
                response['Content'] = '账号尚未激活'
            else:
                pic_url = data['PicUrl']
                # 补卡
                if cache.get(wechat_id):
                    cache.delete_many(wechat_id)
                    Record.objects.create(
                        member=member,
                        time=now() - timedelta(days=1),
                        image_url=pic_url,
                        is_submitted_later=True
                    )
                    records = Record.objects.all().filter(member=member).order_by('-time')[:20]
                    links, count_yesterday_record = '', 0
                    yesterday = now() - timedelta(days=1)
                    for i in range(len(records) - 1, -1, -1):
                        if records[i].time.day == yesterday.day:
                            count_yesterday_record += 1
                            links += '<a href=\'%s\'>链接%d</a>  ' % (records[i].image_url, count_yesterday_record)

                    content = '<a href=\'%s\'>图片</a>已上传。  ' \
                              '你昨天一共向公众号发送了%d张图片(包括补卡图片）, %d张图片的链接分别为: %s。 ' \
                              '今天查卡的时候只会检查最后两张图片，如果最后两张图片不符合要求，请重新补卡' \
                              % (pic_url, count_yesterday_record, count_yesterday_record, links)
                    response['Content'] = content
                # 打卡
                else:
                    Record.objects.create(
                        member=member,
                        time=now(),
                        image_url=pic_url,
                        is_submitted_later=False
                    )
                    records = Record.objects.all().filter(member=member).order_by('-time')[:10]
                    links, count_today_record = '', 0
                    for i in range(len(records) - 1, -1, -1):
                        if records[i].time.day == now().day:
                            count_today_record += 1
                            links += '<a href=\'%s\'>链接%d</a>  ' % (records[i].image_url, count_today_record)

                    content = '<a href=\'%s\'>图片</a>已上传。  ' \
                              '你今天已经向公众号发送了%d张图片, %d张图片的链接分别为: %s。 ' \
                              '明天查卡的时候只会检查最后两张图片，如果最后两张图片不符合要求，请重发。' \
                              % (pic_url, count_today_record, count_today_record, links)

                    response['Content'] = content

        return Response(xmltodict.unparse({'xml': response}))
