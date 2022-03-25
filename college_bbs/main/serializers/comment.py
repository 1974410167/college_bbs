from college_bbs.common.serializers import BaseModelSerializer, AgreeBaseSerializer
from main.models import ParentComment, ChildComment
from rest_framework import serializers


class ParentCommentSerializers(AgreeBaseSerializer):

    redis_bitmap_agree_prefix = "parent_comment_agree"

    class Meta(BaseModelSerializer.Meta):
        model = ParentComment
        fields = "__all__"


class CreateParentCommentSer(serializers.Serializer):

    post_id = serializers.IntegerField(help_text="文章id")
    content = serializers.CharField(help_text="内容", max_length=125)


class AgreeSerializers(serializers.Serializer):
    agree = serializers.BooleanField(help_text="是否赞同， True赞同， False取消赞同")


class BadSerializers(serializers.Serializer):
    bad = serializers.BooleanField(help_text="是否踩， True踩， False取消踩")


class ChildCommentSerializers(BaseModelSerializer):

    class Meta(BaseModelSerializer.Meta):
        model = ChildComment
        fields = "__all__"
