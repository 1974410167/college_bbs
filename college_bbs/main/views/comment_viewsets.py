from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from college_bbs.common.data_fetch import user_configs, DataFetch
from college_bbs.common.pagination import BasePageNumberPagination
from college_bbs.common.tools import HandleViewsCount
from main.models import ParentComment, ChildComment, Post
from main.serializers.comment import ParentCommentSerializers, ChildCommentSerializers, CreateParentCommentSer
from college_bbs.common import views as custom_mixins
from django_filters import rest_framework as filters
from rest_framework.mixins import CreateModelMixin


class CommentsFilter(filters.FilterSet):
    class Meta:
        model = ParentComment
        fields = ['post_id']


class CommentViewSet(custom_mixins.DataFetchListModelMixin,
                     custom_mixins.DataFetchRetrieveModelMixin,
                     custom_mixins.AgreeCommentMixin,
                     CreateModelMixin,
                     GenericViewSet):

    queryset = ParentComment.objects.all().order_by("-create_time")
    pagination_class = BasePageNumberPagination
    serializer_class = ParentCommentSerializers
    configs = {"post_id__topic_id": ["name"], "post_id": ["title", "topic_id"]}
    configs.update(user_configs)
    redis_bitmap_agree_prefix = "parent_comment_agree"
    filterset_class = CommentsFilter

    def create(self, request, *args, **kwargs):
        ser = CreateParentCommentSer(data=request.data)
        ser.is_valid(raise_exception=True)
        post_id = ser.validated_data["post_id"]
        content = ser.validated_data["content"]
        obj = ParentComment.objects.create(post_id=post_id, content=content)
        res = ParentCommentSerializers(obj)
        return Response(res.data, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        post_id = request.query_params.get("post_id")
        if post_id:
            instance = Post.objects.filter(id=post_id).first()
            if instance:
                HandleViewsCount(instance, request).run()
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            data = serializer.data
            DataFetch(data, self.queryset.model, self.configs).main_loop()
            return self.get_paginated_response(data)

        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data
        DataFetch(data, self.queryset.model, self.configs).main_loop()
        return Response(data)

    @action(methods=["POST"], detail=True, url_path="agree_parent_comment")
    def agree_comment(self, request, pk):
        return super(CommentViewSet, self).agree(request, pk)


class ChildCommentsFilter(filters.FilterSet):
    class Meta:
        model = ChildComment
        fields = ['parent_comment_id', 'comment_id']


class ChildCommentViewSet(custom_mixins.DataFetchListModelMixin,
                          CreateModelMixin,
                          GenericViewSet):

    queryset = ChildComment.objects.all().order_by("-create_time")
    pagination_class = BasePageNumberPagination
    serializer_class = ChildCommentSerializers
    configs = {"comment_id__create_user_id": ["name"]}
    configs.update(user_configs)
    filterset_class = ChildCommentsFilter

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
