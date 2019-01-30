from rest_framework.views import APIView
from rest_framework.response import Response
from . import models, serializers

class Feed(APIView):

    def get(self, request, format=None):

        user = request.user

        following_users = user.following.all()

        # 팔로잉하고 있는 유저의 가장 최신의 두개의 피드만 불러올것임
        # for following_user in following_users:
            
        print(following_users)

        return Response(status=200)