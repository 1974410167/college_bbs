from django.conf.urls import url
from django.urls import include
from rest_framework import routers

from main.views.comment_viewsets import CommentViewSet, ChildCommentViewSet
from main.views.post_viewsets import PostViewSet
from main.views.topic_viewsets import TopicViewSet
from main.views.user_center import UserCenterViewSets


router = routers.SimpleRouter()
router.register(r'topics', TopicViewSet, basename='topics')
router.register(r'posts', PostViewSet, basename='posts')
router.register(r'comments', CommentViewSet, basename='comments')
router.register(r'child_comments', ChildCommentViewSet, basename='child_comments')


urlpatterns = [
    # main
    url(r'^', include(router.urls)),
    url(r"user_center/", UserCenterViewSets.as_view())
]
