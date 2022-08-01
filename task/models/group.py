from django.db import models


class Group(models.Model):
    id = models.IntegerField(primary_key=True)
    created_time = models.DateTimeField(auto_now_add=True)
    member_count = models.IntegerField(default=0)