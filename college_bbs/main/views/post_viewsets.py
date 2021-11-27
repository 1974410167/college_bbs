from rest_framework.viewsets import GenericViewSet

from college_bbs.common.data_fetch import user_configs
from college_bbs.common.pagination import BasePageNumberPagination
from college_bbs.common import views as custom_mixins
from main.models import Post
from main.serializers.post import PostSerializers


class PostViewSet(custom_mixins.DataFetchListModelMixin,
                  custom_mixins.DataFetchRetrieveModelMixin,
                  GenericViewSet):

    queryset = Post.objects.all().order_by("-create_time")
    pagination_class = BasePageNumberPagination
    serializer_class = PostSerializers
    model = Post
    configs = {"topic_id": ["name"]}
    configs.update(user_configs)
