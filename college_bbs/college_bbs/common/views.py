from rest_framework.decorators import action
from rest_framework.response import Response
from college_bbs.common.data_fetch import DataFetch
from college_bbs.common.exception import RepeatAgreeError, AgreeNotFoundError
from college_bbs.common.redis_conn import CONN
from main.serializers.comment import AgreeSerializers, BadSerializers


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


class AgreeMixin:

    # 使用action扩展资源的http方法
    @action(methods=["POST"], detail=True, url_path="agree")
    def agree(self, request, pk):
        ser = AgreeSerializers(data=request.data)
        ser.is_valid(raise_exception=True)
        data = ser.validated_data
        obj = self.get_object()
        redis_bit_key = get_redis_bitmap_key(obj.id, self.redis_bitmap_agree_prefix)

        user_id = request.user.userprofile.id
        is_agree = CONN.getbit(redis_bit_key, user_id)
        res = {
            "message": "",
            "id": pk,
            "agree_count": 0,
        }
        if data.get("agree"):
            if is_agree == 1:
                return Response(RepeatAgreeError("你已赞同过此条内容")())
            CONN.setbit(redis_bit_key, user_id, 1)
            res["message"] = "赞同成功"

        elif not data.get("agree"):
            if is_agree == 0:
                return Response(AgreeNotFoundError("你还未赞同过此条内容")())
            CONN.setbit(redis_bit_key, user_id, 0)
            res["message"] = "已取消赞同"

        agree_count = CONN.bitcount(redis_bit_key)
        res["agree_count"] = agree_count
        return Response(res)


class BadPostMixin:

    def bad(self, request, pk):
        ser = BadSerializers(data=request.data)
        ser.is_valid(raise_exception=True)
        data = ser.validated_data
        obj = self.get_object()
        redis_bit_key = get_redis_bitmap_key(obj.id, self.redis_bitmap_bad_prefix)

        user_id = request.user.userprofile.id
        is_bad = CONN.getbit(redis_bit_key, user_id)
        res = {
            "message": "",
            "id": pk,
        }
        if data.get("bad"):
            if is_bad == 1:
                return Response(RepeatAgreeError("你已踩过此条内容")())
            CONN.setbit(redis_bit_key, user_id, 1)
            res["message"] = "踩成功"

        elif not data.get("bad"):
            if is_bad == 0:
                return Response(AgreeNotFoundError("你还未踩过此条内容")())
            CONN.setbit(redis_bit_key, user_id, 0)
            res["message"] = "已踩"

        return Response(res)


class AgreeCommentMixin(AgreeMixin):
    pass


class AgreePostMixin(AgreeMixin):
    pass


def get_redis_bitmap_key(id: int, prefix: str):
    return prefix + str(id)
