from django.contrib.auth.models import User
from django.db import models

from task.models.group import Group


class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    wechat_id = models.CharField(max_length=128)
    enter_time = models.DateTimeField(auto_now_add=True)
    quit_time = models.DateTimeField(null=True)
    is_active = models.BooleanField(default=False)
    count_failure_in_a_week = models.IntegerField(default=0)
    group = models.ForeignKey(Group, on_delete=models.DO_NOTHING)

    def set_password(self, password):
        self.password = password

    def set_count_failure_in_a_week(self, count_failure_in_a_week):
        self.count_failure_in_a_week = count_failure_in_a_week
