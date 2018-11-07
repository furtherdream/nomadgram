from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
# django.db 를 models를 불러온다. (두번째 줄 수정)

class User(AbstractUser):

    # User는 AbstractUser를 확장하는 개념으로 AbstractUser를 포함하고 있다.
    
    # 아래에 gender는 조건을 만들어야 함
    # constant를 생성 : 성별 선택을 위해서
    GENDER_CHOICES = (
        ('male', 'Male'),
        ('Female', 'Female'),
        ('not-specified', 'Not specified')
    )

    # First Name and Last Name do not cover name patterns
    # around the globe.
    name = models.CharField(_("Name of User"), blank=True, max_length=255)
    # 필드를 추가하는 방법은 매우 심플함 (Variable Name을 만들어 주면 됨)
    website = models.URLField(null=True)
    bio = models.TextField(null=True)
    phone = models.CharField(max_length=140, null=True)
    gender = models.CharField(max_length=80, choices=GENDER_CHOICES, null=True)

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})
    