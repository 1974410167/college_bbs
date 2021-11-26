from college_bbs.common.serializers import BaseModelSerializer
from main.models import Post


class PostSerializers(BaseModelSerializer):

    class Meta(BaseModelSerializer.Meta):
        model = Post
        fields = "__all__"
