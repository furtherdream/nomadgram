from django.db import models
from nomadgram.users import models as user_models
# models가 두개이기 때문에 장고가 혼란에 빠질 수 있다. 닉네임 : user_models로 불러 올 수 있도록 한다. (충돌 방지)

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

    def __str__(self):
        return '{} - {}'.format(self.location, self.caption)


class Comment(TimeStampedModel):

    """ Comment Model """

    # 댓글은 댓글을 생성한 생성자가 있고, 어떤 이미지에 달렸는지 이미지가 존재함
    message = models.TextField()
    creator = models.ForeignKey(user_models.User, on_delete=models.PROTECT, null=True)
    image = models.ForeignKey(Image, on_delete=models.PROTECT, null=True)

    def __str__(self):
        return self.message


class Like(TimeStampedModel):

    """ Like Model """

    # 좋아요는 이미지 / 아이디 / 생성자가 필요하다
    # foreignKey() 는 장고가 () 안에 있는 것을 찾아옴 => 유저 > 모델 > 클레스의 유저를 불러와야 함
    creator = models.ForeignKey(user_models.User, on_delete=models.PROTECT, null=True)
    image = models.ForeignKey(Image, on_delete=models.PROTECT, null=True)

    def __str__(self):
        return 'User: {} - Image Caption: {}'.format(self.creator.username, self.image.caption)