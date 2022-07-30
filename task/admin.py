from django.contrib import admin

from task.models.member import Member
from task.models.record import Record

# Register your models here.
admin.site.register(Member)
admin.site.register(Record)
