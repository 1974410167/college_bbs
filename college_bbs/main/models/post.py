from django.db import models
from college_bbs.common.models import BaseModel


class Post(BaseModel):
    """
    帖子
    """
    class ForeignKeyConstraint:
        fields = {
            'topic_id': {"to_model": "main.Topic"},
        }

    class Meta(BaseModel.Meta):
        db_table = 'post'

    title = models.CharField(verbose_name='问题标题', max_length=255)
    content = models.TextField(verbose_name='问题内容')
    answer_count = models.BigIntegerField(verbose_name='回答数量', default=0)
    views_count = models.BigIntegerField(verbose_name='浏览量', default=0)
    topic_id = models.BigIntegerField(verbose_name="话题id", null=True)
