from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from college_bbs.common.pagination import BasePageNumberPagination
from main.models import Topic
from main.serializers.topic import TopicSerializers


class TopicViewSet(mixins.ListModelMixin,
                   mixins.RetrieveModelMixin,
                   GenericViewSet):

    queryset = Topic.objects.all().order_by("-create_time")
    pagination_class = BasePageNumberPagination
    serializer_class = TopicSerializers
