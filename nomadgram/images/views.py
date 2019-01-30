from rest_framework.views import APIView
from rest_framework.response import Response
# 장고 상태코드를 한 번 가지고 와보자
from rest_framework import status
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

        return Response(serializer.data)


class LikeImage(APIView):
    # 규칙은 데이터베이스에서 뭔가 변화면 post request가 되어야 함
    # Tip : 잠시만 post 를 get으로 바꾸고 urls에 입력한 id를 variable로 입력하여 정상적으로 작동하는지 확인
    # request 다음에 id(url에서 id를 보내고 있기 때문?)를 넣는 것을 잊으면 안됨!! 에러 발생
    def get(self, request, id, format=None):

        user = request.user

        # 이미지가 없을 때는 404 에러를 원함 그래서 try & catch 를 사용할거임
        try : 
            found_image = models.Image.objects.get(id = id)
        except models.Image.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


        # 이미 좋아요를 한 경우의 처리
        try:
            preexisting_like = models.Like.objects.get(
                creator=user,
                image=found_image
            )
            preexisting_like.delete()
            return Response(status=status.HTTP_204_NO_CONTENT) #204 : 내용이 없다는 뜻


        except models.Like.DoesNotExist:
            new_like = models.Like.objects.create(
                creator=user,
                image=found_image
            )

            new_like.save()

            return Response(status=status.HTTP_201_CREATED)