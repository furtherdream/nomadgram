from rest_framework import serializers
# rest_framework를 불러오고
from . import models

# 시리얼라이저는 모델과 같은 필드가 있음. 해당 필드만 가져오고 싶다고 입력할 수 있
# 그 전에 메타클래스를 줘야함 (meta class : Extra Information Class - 설정하는 클래스) 
class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Image
        fields = '__all__'
    

class CommentSerializer(serializers.ModelSerializer):

    image = ImageSerializer()

    class Meta:
        model = models.Comment
        fields = '__all__'


class LikeSerializer(serializers.ModelSerializer):

    image = ImageSerializer()

    class Meta:
        model = models.Like
        fields = '__all__'