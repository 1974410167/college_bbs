from django.conf.urls import url
from django.urls import include
from rest_framework import routers

from main.views.comment_viewsets import CommentViewSet
from main.views.post_viewsets import PostViewSet
from main.views.topic_viewsets import TopicViewSet


router = routers.SimpleRouter()
router.register(r'topics', TopicViewSet, basename='topics')
router.register(r'posts', PostViewSet, basename='posts')
router.register(r'comments', CommentViewSet, basename='comments')


urlpatterns = [
    # main
    url(r'^', include(router.urls)),
]
