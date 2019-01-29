# 시리얼라이저를 생성했으니 이제 view 를 생성해보자.

# 우리가 만들고 테스트해 볼 view는 데이터베이스에 있는 모든 이미지를 볼 수 있는 view 인데 이건 사실 좋지 못한 뷰이다.
# 왜?? 사진이 많이 있는데, 많은 사람들이 동일한 request를 보내면 DB가 뻗어버림 : 지금은 테스트로 만들지만 실제로는 이렇게 만들지 않음
# view는 디폴트로 import 를 하고 우리가 템플릿을 사용하고 싶을 때 render를 사용함
# 여기선 어떤 템플릿도 쓰지 않고, 그냥 장고 api를 위해 사용할 뿐
# 그래서 아래의 코드를 삭제하고 2개의 클래스를 불러 올 것임.
# from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
# 엘리먼트를 가져오고, 보여주고, method를 관리하는 멋진 클래스임
from . import models, serializers


class ListAllImages(APIView):

    # APIView는 우리가 사용한 http request에 따라 각기 다른 function을 사용할 거임 (이번엔 get만 사용함)
    # self 는 이미 정의된 variable이야. 파이썬에는 self attribute가 있음
    # request 클라이언트가 오브젝트를 요청. 그래서 클라이언트에 접근 권한이 있고, 오브젝트를 얻는 것임 => get, post, delete 상관없음
    # format은 json, xml이 될 수 잇는데 지금은 None으로 지정 (default는 Json)
    def get(self, request, format=None):

        # 모든 이미지를 불러온다. 장고에서 오브젝트를 불러오는 것은 굉장히 쉬움
        # 오브젝트는 좋은 펑션을 가지고 있음 예를 들어 all() 같은!!
        all_images = models.Image.objects.all()
        
        # 위의 것은 파이썬 오브젝트라서 시리얼라이즈를 이용해서 변형해야겠지?
        serializer = serializers.ImageSerializer(all_images, many=True)

        # return은 클래스의 마지막 문장인 셈이다.
        # Response 역시 많은 method를 가지고 있다. 지금은 data를 사용할 거임
        return Response(data=serializer.data)


class ListAllComments(APIView):

    def get(self, request, format=None):

        all_comments = models.Comment.objects.all()

        serializer = serializers.CommentSerializer(all_comments, many=True)

        return Response(data=serializer.data)



class ListAllLikes(APIView):

    def get(self, request, format=None):

        all_likes = models.Like.objects.all()

        serializer = serializers.LikeSerializer(all_likes, many=True)

        return Response(data=serializer.data)

        # 여기까지 작성해도 정상 동작하지 않음! 왜?? urls에 뷰를 연결해야 하니까!!