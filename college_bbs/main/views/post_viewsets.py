from rest_framework import mixins
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from college_bbs.common.data_fetch import DataFetch
from college_bbs.common.pagination import BasePageNumberPagination
from main.models import Post, Topic
from main.serializers.post import PostSerializers
from user.models import UserProfile


class PostViewSet(mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  GenericViewSet):

    queryset = Post.objects.all().order_by("-create_time")
    pagination_class = BasePageNumberPagination
    serializer_class = PostSerializers
    configs = {"topic_id": [Topic, ["name"]], "create_user_id": [UserProfile, ["name"], "user"]}

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        DataFetch(data, self.configs)
        return Response(data)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            data = serializer.data
            DataFetch(data, self.configs)
            return self.get_paginated_response(data)

        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data
        DataFetch(data, self.configs)
        return Response(data)
