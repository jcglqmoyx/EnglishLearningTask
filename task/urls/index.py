from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from task.views.info.member.member import MemberView
from task.views.info.record.records import RecordView
from task.views.settings.register import RegisterView
from task.views.wechat.index import WechatView
from task.views.info.record.report import ReportView

urlpatterns = [
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('wechat/verification/', WechatView.as_view(), name='server_verification'),

    path('register/', RegisterView.as_view(), name='register'),

    path('info/member/', MemberView.as_view(), name='get_member_info'),

    path('info/record/', RecordView.as_view(), name='get_latest_records'),
    path('info/report/', ReportView.as_view(), name='generate_report')
]
