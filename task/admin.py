from django.contrib import admin

from task.models.member import Member
from task.models.record import Record
from task.models.group import Group

# Register your models here.
admin.site.register(Member)
admin.site.register(Record)
admin.site.register(Group)