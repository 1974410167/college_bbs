from rest_framework import mixins
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from college_bbs.common.pagination import BasePageNumberPagination
from main.models import Topic
from main.serializers.topic import TopicSerializers


class TopicViewSet(mixins.ListModelMixin,
                   mixins.RetrieveModelMixin,
                   GenericViewSet):

    queryset = Topic.objects.all().order_by("-host_number")
    pagination_class = BasePageNumberPagination
    serializer_class = TopicSerializers

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
