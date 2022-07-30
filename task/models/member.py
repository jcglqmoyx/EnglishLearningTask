from django.db import models
from django.contrib.auth.models import User


class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    wechat_id = models.CharField(max_length=128)
    enter_time = models.DateTimeField(null=True)
    quit_time = models.DateTimeField(null=True)
    is_active = models.BooleanField(default=False)
    total_active_days = models.IntegerField(default=0)
    max_active_days_in_a_row = models.IntegerField(default=0)
    group_id = models.IntegerField()

    def set_password(self, password):
        self.password = password

    def set_total_active_days(self, total_active_days):
        self.total_active_days = total_active_days

    def sex_max_active_days_in_a_row(self, max_active_days_in_a_row):
        self.max_active_days_in_a_row = max_active_days_in_a_row

    def set_enter_time(self, enter_time):
        self.enter_time = enter_time
