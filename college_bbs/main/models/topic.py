from django.db import models

from college_bbs.common.models import BaseModel


class Topic(BaseModel):
    """
    话题
    """

    class Meta(BaseModel.Meta):
        db_table = 'topic'

    name = models.CharField(verbose_name="话题名字", max_length=255, null=True)
    description = models.TextField(verbose_name="话题描述", null=True)
    host_number = models.BigIntegerField(verbose_name="热度", default=0)

    def __str__(self):
        return self.name
