from rest_framework.decorators import action
from rest_framework.response import Response
from college_bbs.common.data_fetch import DataFetch
from college_bbs.common.exception import RepeatAgreeError, AgreeNotFoundError
from college_bbs.common.redis_conn import CONN
from main.serializers.comment import AgreeCommentSerializers


class DataFetchListModelMixin:
    """
    List a queryset.
    """

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            data = serializer.data
            DataFetch(data, self.queryset.model, self.configs).main_loop()
            return self.get_paginated_response(data)

        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data
        DataFetch(data, self.queryset.model, self.configs).main_loop()
        return Response(data)


class DataFetchRetrieveModelMixin:
    """
    Retrieve a model instance.
    """
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        DataFetch(data, self.queryset.model, self.configs).main_loop()
        return Response(data)


class AgreeCommentMixin:

    # 使用action扩展资源的http方法
    @action(methods=["POST"], detail=True, url_path="agree")
    def agree_comment(self, request, pk):
        ser = AgreeCommentSerializers(data=request.data)
        ser.is_valid(raise_exception=True)
        data = ser.validated_data
        obj = self.get_object()
        redis_bit_key = obj.id
        user_id = request.user.userprofile.id
        is_agree = CONN.getbit(redis_bit_key, user_id)
        res = {
            "message": "",
            "id": pk,
            "views_count": 0,
        }
        if data.get("agree_comment"):
            if is_agree == 1:
                return Response(RepeatAgreeError("你已赞同过此答案")())
            CONN.setbit(redis_bit_key, user_id, 1)
            res["message"] = "赞同成功"

        elif not data.get("agree_comment"):
            if is_agree == 0:
                return Response(AgreeNotFoundError("你还未赞同过此评论")())
            CONN.setbit(redis_bit_key, user_id, 0)
            res["message"] = "已取消赞同"

        views_count = CONN.bitcount(redis_bit_key)
        res["views_count"] = views_count
        return Response(res)
