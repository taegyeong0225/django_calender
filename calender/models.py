# models.py
from django.db import models
from django.contrib.auth.models import User

class Events(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default="None")  # Relate each event to a specific user
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=False, blank=False, default="입력 필요")
    end = models.DateTimeField(null=True, blank=True)  # blank=True로 수정
    category = models.CharField(
        max_length=20,
        choices=[
            ('food', '재료'),
            ('no-food', '비재료'),
            ('none', '선택하지 않음'),  # 추가 옵션
        ],
        null=False,
        blank=False,  # blank=True에서 blank=False로 수정
        default='none'  # 기본값 설정
    )


    class Meta:
        db_table = "tblevents"