# models.py
from django.db import models
from django.contrib.auth.models import User

class Events(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, default=None)
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255,null=False,blank=False, default="입력 필요")
    end = models.DateTimeField(null=True,blank=False)
    category = models.CharField(
        max_length=20,  # 적절한 최대 길이 설정
        choices=[
            ('food', '재료'),  # HTML select의 value 및 표시 텍스트
            ('no-food', '비재료'),
        ],
        null=False,
        blank=True
    )


    class Meta:
        db_table = "tblevents"