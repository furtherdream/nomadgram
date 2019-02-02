from django.urls import path
from . import views

app_name = "images"
urlpatterns = [
    path("", view=views.Feed.as_view(), name="feed"),
    # comment -> comments로 바꿈 : 내가 post를 보낼 때마다 생성되도록
    path("<int:id>/like/", view=views.LikeImage.as_view(), name="like_image"),
    path("<int:id>/unlike/", view=views.UnlikeImage.as_view(), name="unlike_image"),
    path("<int:id>/comments/", view=views.CommentOnImage.as_view(), name="comment_image"),
    path("<int:image_id>/comments/<int:comment_id>", view=views.ModerateComments.as_view(), name="moderate_comment"),
    path("comments/<int:id>/", view=views.Comment.as_view(), name="comment"),
    path("search/", view=views.Search.as_view(), name="search")
]