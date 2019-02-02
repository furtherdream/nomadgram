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
    def post(self, request, id, format=None):

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
            # 이미 좋아요를 한 경우에는 별다른 반응 없음 : 수정하지 않음
            return Response(status=status.HTTP_304_NOT_MODIFIED)


        except models.Like.DoesNotExist:
            new_like = models.Like.objects.create(
                creator=user,
                image=found_image
            )

            new_like.save()

            return Response(status=status.HTTP_201_CREATED)


class UnlikeImage(APIView):

    def delete(self, request, id, format=None):

        user = request.user

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
            return Response(status=status.HTTP_304_NOT_MODIFIED)


class CommentOnImage(APIView):

    def post(self, request, id, format=None):

        # 댓글을 단 사람을 알아내기 위해
        user = request.user
        # 이미지가 없는 경우에는 이전에 like 작업 했던 것처럼 try catch로 코딩해준다.
        try:
            found_image = models.Image.objects.get(id = id)
        except models.Image.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


        # 시리얼라이즈는 이미지를 가져오고 보여주는 것 외에도 이미지를 저장하는지를 체크하기도 함
        # 그냥 보여주는 것 외에도 우리가 무언가를 생성할 때도 도움을 줌
        serializer = serializers.CommentSerializer(data=request.data)

        # 우리가 지금 작업한 것은 시리얼라이즈를 저장하려고 한 것이고, 이것이 유효한 것을 보여주려 함
        # 이 시리얼라이즈가 유효한 이유는 "message" 만 받으면 되는 것이기 때문에 {"message" : "hello"} 형태로 post 하니 유효하다
        if serializer.is_valid():
            # 그리고 빈 것을 저장하면 안 되니 해당 값을 모델에 붙여놓음
            serializer.save(creator=user, image=found_image)

            return Response(data=serializer.data, status=status.HTTP_201_CREATED)

        else:

            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Comment(APIView):

    def delete(self, request, id, format=None):

        # 다른 사람이 쓴 댓글을 삭제할 수 있으면 안된다. 
        # 생성자와 user가 같은 경우에만 삭제 할 수 있도록 해보자!!
        user = request.user

        try:
            comment = models.Comment.objects.get(id=id, creator=user)
            comment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        except models.Comment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class Search(APIView):

    def get(self, request, farmat=None):

        hashtags = request.query_params.get('hashtags', None)

        # request.query_params를 통해 파라미터로 만듦, 아무것도 없을 경우 None을 보냄
        # if로 None이 아닐경우 아래처럼 해쉬 태그를 검색되게 만들고, None 일 경우는 오류코드 보냄
        if hashtags is not None : 

            hashtags = hashtags.split(",")

            images = models.Image.objects.filter(tags__name__in=hashtags).distinct()

            serializer = serializers.CountImageSerializer(images, many=True)

            return Response(data=serializer.data, status=status.HTTP_200_OK)

        else :
            return Response(status=status.HTTP_400_BAD_REQUEST)