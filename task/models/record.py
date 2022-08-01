from django.db import models
from task.models.member import Member


class Record(models.Model):
    id = models.IntegerField(primary_key=True)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    time = models.DateTimeField()
    image_url = models.URLField(max_length=512)
    is_submitted_later = models.BooleanField(default=False)
