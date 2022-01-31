from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet

from college_bbs.common.data_fetch import user_configs
from college_bbs.common.pagination import BasePageNumberPagination
from main.models import ParentComment, ChildComment
from main.serializers.comment import ParentCommentSerializers, ChildCommentSerializers
from college_bbs.common import views as custom_mixins
from django_filters import rest_framework as filters


class CommentsFilter(filters.FilterSet):
    class Meta:
        model = ParentComment
        fields = ['post_id']


class CommentViewSet(custom_mixins.DataFetchListModelMixin,
                     custom_mixins.DataFetchRetrieveModelMixin,
                     custom_mixins.AgreeCommentMixin,
                     GenericViewSet):

    queryset = ParentComment.objects.all().order_by("-create_time")
    pagination_class = BasePageNumberPagination
    serializer_class = ParentCommentSerializers
    configs = {"post_id__topic_id": ["name"], "post_id": ["title", "topic_id"]}
    configs.update(user_configs)
    redis_bitmap_agree_prefix = "parent_comment_agree"
    filterset_class = CommentsFilter

    @action(methods=["POST"], detail=True, url_path="agree_parent_comment")
    def agree_comment(self, request, pk):
        return super(CommentViewSet, self).agree(request, pk)


class ChildCommentsFilter(filters.FilterSet):
    class Meta:
        model = ChildComment
        fields = ['parent_comment_id', 'comment_id']


class ChildCommentViewSet(custom_mixins.DataFetchListModelMixin,
                          GenericViewSet):

    queryset = ChildComment.objects.all().order_by("-create_time")
    pagination_class = BasePageNumberPagination
    serializer_class = ChildCommentSerializers
    configs = {"comment_id__create_user_id": ["name"]}
    configs.update(user_configs)
    filterset_class = ChildCommentsFilter
