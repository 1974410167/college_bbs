
from college_bbs.common.serializers import BadAndAgreeBaseSerializer
from main.models import Post
from rest_framework import serializers


class PostSerializers(BadAndAgreeBaseSerializer):

    redis_bitmap_agree_prefix = "post_agree"
    redis_bitmap_bad_prefix = "post_bad"

    class Meta(BadAndAgreeBaseSerializer.Meta):
        model = Post
        fields = "__all__"


class AddPostSer(serializers.Serializer):

    content = serializers.CharField(help_text="文章内容")
    topic = serializers.CharField(help_text="话题名字")

