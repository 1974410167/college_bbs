from college_bbs.common.serializers import BaseModelSerializer
from main.models import ParentComment
from rest_framework import serializers


class ParentCommentSerializers(BaseModelSerializer):

    class Meta(BaseModelSerializer.Meta):
        model = ParentComment
        fields = "__all__"


class AgreeCommentSerializers(serializers.Serializer):
    agree_comment = serializers.BooleanField(help_text="是否赞同， True赞同， False取消赞同")
