from rest_framework import serializers
# rest_framework를 불러오고
from . import models
from taggit_serializer.serializers import (TagListSerializerField,
                                           TaggitSerializer)
from nomadgram.users import models as user_models


class SmallImageSerializer(serializers.ModelSerializer):

    """ Used for the notifications """

    class Meta:
        model = models.Image
        fields = (
            'file',
        )


class CountImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Image
        fields = (
            'id',
            'file',
            'comment_count',
            'like_count',
        )


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
    # 댓글을 달 때마다 생성자를 바꿔서 달 수는 없으므로 read_only=True 를 해준다.
    creator = FeedUserSerializer(read_only=True)

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


class ImageSerializer(TaggitSerializer, serializers.ModelSerializer):

    comments = CommentSerializer(many=True)
    creator = FeedUserSerializer()
    tags = TagListSerializerField()


    class Meta:
        model = models.Image
        fields = (
            'id',
            'file',
            'location',
            'caption',
            'comments',
            'like_count',
            'creator',
            'tags',
            'created_at'
        )
