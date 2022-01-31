from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from college_bbs.common.data_fetch import user_configs, DataFetch
from college_bbs.common.pagination import BasePageNumberPagination
from college_bbs.common import views as custom_mixins
from college_bbs.common.tools import HandleViewsCount, sync_pageviews
from main.models import Post
from main.serializers.post import PostSerializers
from django_filters import rest_framework as filters


class PostsFilter(filters.FilterSet):
    class Meta:
        model = Post
        fields = ['topic_id']


class PostViewSet(custom_mixins.DataFetchListModelMixin,
                  custom_mixins.DataFetchRetrieveModelMixin,
                  custom_mixins.AgreePostMixin,
                  custom_mixins.BadPostMixin,
                  GenericViewSet):

    queryset = Post.objects.all().order_by("-create_time")
    pagination_class = BasePageNumberPagination
    serializer_class = PostSerializers
    configs = {"topic_id": ["name"]}
    configs.update(user_configs)
    redis_bitmap_agree_prefix = "post_agree"
    redis_bitmap_bad_prefix = "post_bad"
    filterset_class = PostsFilter

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

    @action(methods=["POST"], detail=True, url_path="agree_posts")
    def agree_post(self, request, pk):
        return super(PostViewSet, self).agree(request, pk)

    @action(methods=["POST"], detail=True, url_path="bad_posts")
    def bad_post(self, request, pk):
        return super(PostViewSet, self).bad(request, pk)
