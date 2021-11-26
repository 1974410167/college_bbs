from college_bbs.common.serializers import BaseModelSerializer
from main.models import Topic


class TopicSerializers(BaseModelSerializer):

    class Meta(BaseModelSerializer.Meta):
        model = Topic
        fields = "__all__"
