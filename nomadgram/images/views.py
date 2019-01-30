from rest_framework.views import APIView
from rest_framework.response import Response
from . import models, serializers

class Feed(APIView):

    def get(self, request, format=None):

        user = request.user

        following_users = user.following.all()

        image_list = []
        # 팔로잉하고 있는 유저의 가장 최신의 두개의 피드만 불러올것임
        for following_user in following_users:
            
             user_images = following_user.images.all()[:2]
             
             for image in user_images:

                image_list.append(image)
        
        sorted_list = sorted(
            image_list, key=lambda image: image.created_at, reverse=True)

        serializer = serializers.ImageSerializer(sorted_list, many=True)


        return Response(serializer.data)
