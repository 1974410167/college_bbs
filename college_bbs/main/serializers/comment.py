from college_bbs.common.serializers import BaseModelSerializer, AgreeBaseSerializer
from main.models import ParentComment
from rest_framework import serializers


class ParentCommentSerializers(AgreeBaseSerializer):

    redis_bitmap_agree_prefix = "parent_comment_agree"

    class Meta(BaseModelSerializer.Meta):
        model = ParentComment
        fields = "__all__"


class AgreeSerializers(serializers.Serializer):
    agree = serializers.BooleanField(help_text="是否赞同， True赞同， False取消赞同")


class BadSerializers(serializers.Serializer):
    bad = serializers.BooleanField(help_text="是否踩， True踩， False取消踩")
