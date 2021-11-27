from college_bbs.common.models import BaseModel
from django.db import models


class BaseComment(models.Model):
    """
    评论基类
    """
    class Meta:
        abstract = True

    like_count = models.BigIntegerField(verbose_name='赞同数', default=0)
    content = models.TextField(verbose_name='评论内容', null=True)


class ParentComment(BaseComment, BaseModel):
    """
    评论
    """
    class Meta(BaseModel.Meta):
        db_table = 'parent_comment'

    class ForeignKeyConstraint:
        fields = {
            'post_id': {"to_model": "main.Post"},
        }
        fields.update(BaseModel.ForeignKeyConstraint.fields)

    post_id = models.BigIntegerField(verbose_name='帖子id', null=True)
    comment_number = models.BigIntegerField(verbose_name="回复数", default=0)


class ChildComment(BaseComment, BaseModel):
    """
    评论的回复
    """
    class Meta(BaseModel.Meta):
        db_table = 'child_comment'

    class ForeignKeyConstraint:
        fields = {
            'comment_id': {"to_model": "main.ChildComment"},
            'parent_comment_id': {"to_model": "main.ParentComment"},
        }
        fields.update(BaseModel.ForeignKeyConstraint.fields)


    parent_comment_id = models.BigIntegerField(verbose_name='评论id', null=True)
    comment_id = models.BigIntegerField(verbose_name='评论id', null=True)
