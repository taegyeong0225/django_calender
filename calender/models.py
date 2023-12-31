from django.db import models
from django.contrib.auth.models import User # user 연결


# calender/models.py
class Events(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255,null=True,blank=True)
    start = models.DateTimeField(null=True,blank=True)
    end = models.DateTimeField(null=True,blank=True)

    f_category = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        db_table = "tblevents"