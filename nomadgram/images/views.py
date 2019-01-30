from rest_framework.views import APIView
from rest_framework.response import Response
from . import models, serializers

class Feed(APIView):

    def get(self, request, format=None):

        user = request.user

        following_users = user.following.all()

        image_list = []

        # (request)유저가 팔로잉하는 유저 리스트를 얻어야 하고, 
        # 해당 팔로워가 가지고 있는 이미지를 불러옴 (Image 모델에서 related_name="images")
        for following_user in following_users:

            # 팔로잉하고 있는 유저의 가장 최신의 두개의 피드만 불러올것임
            user_images = following_user.images.all()[:2]
             
            for image in user_images:

                image_list.append(image)        

        # key=lambda x : x.created_at 을 이용해서 get_key를 대체할 수 있음
        sorted_list = sorted(image_list, key=lambda image: image.created_at, reverse=True)

        serializer = serializers.ImageSerializer(sorted_list, many=True)

        print(following_users)
        print(image_list)
        return Response(serializer.data)