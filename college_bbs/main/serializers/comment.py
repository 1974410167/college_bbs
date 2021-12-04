from college_bbs.common.serializers import BaseModelSerializer
from main.models import ParentComment
from rest_framework import serializers
from user.authentication import _auth_ctx
from college_bbs.common.redis_conn import CONN


class ParentCommentSerializers(BaseModelSerializer):
    is_agree = serializers.SerializerMethodField()

    class Meta(BaseModelSerializer.Meta):
        model = ParentComment
        fields = "__all__"

    def get_is_agree(self, obj):
        redis_bit_key = obj.id
        user_id = _auth_ctx.user.userprofile.id
        is_agree = CONN.getbit(redis_bit_key, user_id)
        return is_agree


class AgreeCommentSerializers(serializers.Serializer):
    agree_comment = serializers.BooleanField(help_text="是否赞同， True赞同， False取消赞同")
