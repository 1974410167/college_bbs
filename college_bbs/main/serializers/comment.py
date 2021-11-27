from college_bbs.common.serializers import BaseModelSerializer
from main.models import ParentComment


class ParentCommentSerializers(BaseModelSerializer):

    class Meta(BaseModelSerializer.Meta):
        model = ParentComment
        fields = "__all__"
