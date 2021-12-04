from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from college_bbs.common.data_fetch import user_configs, DataFetch
from college_bbs.common.pagination import BasePageNumberPagination
from college_bbs.common import views as custom_mixins
from college_bbs.common.tools import HandleViewsCount, sync_pageviews
from main.models import Post
from main.serializers.post import PostSerializers


class PostViewSet(custom_mixins.DataFetchListModelMixin,
                  custom_mixins.DataFetchRetrieveModelMixin,
                  GenericViewSet):

    queryset = Post.objects.all().order_by("-create_time")
    pagination_class = BasePageNumberPagination
    serializer_class = PostSerializers
    configs = {"topic_id": ["name"]}
    configs.update(user_configs)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        views_count = HandleViewsCount(instance, request).run()
        serializer = self.get_serializer(instance)
        data = serializer.data
        data["views_count"] = views_count
        DataFetch(data, self.queryset.model, self.configs).main_loop()
        return Response(data)

    def list(self, request, *args, **kwargs):
        sync_pageviews(queryset=self.queryset)
        return super(PostViewSet, self).list(request, *args, **kwargs)
