
from college_bbs.common.serializers import BadAndAgreeBaseSerializer
from main.models import Post


class PostSerializers(BadAndAgreeBaseSerializer):

    redis_bitmap_agree_prefix = "post_agree"
    redis_bitmap_bad_prefix = "post_bad"

    class Meta(BadAndAgreeBaseSerializer.Meta):
        model = Post
        fields = "__all__"

