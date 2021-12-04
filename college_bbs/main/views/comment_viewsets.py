from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet

from college_bbs.common.data_fetch import user_configs
from college_bbs.common.pagination import BasePageNumberPagination
from main.models import ParentComment
from main.serializers.comment import ParentCommentSerializers
from college_bbs.common import views as custom_mixins


class CommentViewSet(custom_mixins.DataFetchListModelMixin,
                     custom_mixins.DataFetchRetrieveModelMixin,
                     custom_mixins.AgreeCommentMixin,
                     GenericViewSet):

    queryset = ParentComment.objects.all().order_by("-create_time")
    pagination_class = BasePageNumberPagination
    serializer_class = ParentCommentSerializers
    configs = {"post_id__topic_id": ["name"], "post_id": ["title", "topic_id"]}
    configs.update(user_configs)

    # 使用action扩展资源的http方法
    @action(methods=["POST"], detail=True, url_path="agree_parent_comment")
    def agree_comment(self, request, pk):
        return super(CommentViewSet, self).agree_comment(request, pk)
