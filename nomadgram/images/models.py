from django.db import models
from nomadgram.users import models as user_models

class TimeStampedModel(models.Model):
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # ()를 빈칸으로 놔두면 내가 원할 때 추가를 할 수 있다는 뜻이다
    # auto_now_add는 자동으로 추가를 하는 것이고, auto_now는 모델이 저장될 때마다 자동으로 새로고침

    #모델이 아니고 abstract 모델이라고 장고에게 설명?
    class Meta:
        abstract = True # 이 모델은 abstrct base 클래스이다. 라는 의미 (데이터 베이스에 저장 X)

class Image(TimeStampedModel):

    """ Image Model """

    file = models.ImageField()
    location = models.CharField(max_length=140)
    caption = models.TextField()
    creator = models.ForeignKey(user_models.User, on_delete=models.PROTECT, null=True)


class Comment(TimeStampedModel):

    """ Comment Model """

    message = models.TextField()
    creator = models.ForeignKey(user_models.User, on_delete=models.PROTECT, null=True)
    image = models.ForeignKey(Image, on_delete=models.PROTECT, null=True)


class Like(TimeStampedModel):

    """ Like Model """

    creator = models.ForeignKey(user_models.User, on_delete=models.PROTECT, null=True)
    image = models.ForeignKey(Image, on_delete=models.PROTECT, null=True)