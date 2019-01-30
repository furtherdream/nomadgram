from rest_framework import serializers
# rest_framework를 불러오고
from . import models
from nomadgram.users import models as user_models

# 시리얼라이저는 모델과 같은 필드가 있음. 해당 필드만 가져오고 싶다고 입력할 수 있
# 그 전에 메타클래스를 줘야함 (meta class : Extra Information Class - 설정하는 클래스) 
class FeedUserSerializer(serializers.ModelSerializer):
    # 피드에 이미지 상단에 아이디와 이미지를 불러오기 위해
    class Meta:
        model = user_models.User
        fields = (
            'username',
            'profile_image'
        )


class CommentSerializer(serializers.ModelSerializer):
    # 댓글은 생성한 사람의 이름 그리고 댓글 순으로 출력되고 있음
    creator = FeedUserSerializer()

    class Meta:
        model = models.Comment
        fields = (
            'id',
            'message',
            'creator',
        )


class LikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Like
        fields = '__all__'


class ImageSerializer(serializers.ModelSerializer):

    comments = CommentSerializer(many=True)
    creator = FeedUserSerializer()

    class Meta:
        model = models.Image
        fields = (
            'id',
            'file',
            'location',
            'caption',
            'comments',
            'like_count',
            'creator'
        )