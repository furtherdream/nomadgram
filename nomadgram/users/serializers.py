from rest_framework import serializers
from . import models
from nomadgram.images import serializers as image_serializers


class UserProfileSerializer(serializers.ModelSerializer):

    images = image_serializers.CountImageSerializer(many=True)
    post_count = serializers.ReadOnlyField()
    followers_count = serializers.ReadOnlyField() 
    following_count = serializers.ReadOnlyField() 

    class Meta:
        model = models.User
        fields = (
            'profile_image',
            'username',
            'name',
            'bio',
            'website',
            # 추가적으로 이미지수, 팔로잉수, 팔로워서 카운트 : 모델에서 카운트 함 (property로)
            'post_count',
            'followers_count',
            'following_count',
            # 가지고 있는 이미지를 불러오는데 이미지 ID만 불러온다 => 시리얼라이즈가 필요함.
            # 근데 유저 안에서 이미지 시리얼라이즈를 불러오면 이미지 안에 유저를 다시 불러는 circular dependency가 됨
            # 그래서 이미지 시리얼라이즈에서 작업하고 가지고 올거임
            'images'
        )

class ListUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.User
        fields = (
            'id',
            'profile_image',
            'username',
            'name'
        )