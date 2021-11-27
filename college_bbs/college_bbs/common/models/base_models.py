from django.db import models
from college_bbs.common.models.deletion import ModelOnDeleteMixin
from user.authentication import _auth_ctx


def get_create_user_id():
    if hasattr(_auth_ctx, 'user'):
        return _auth_ctx.user.userprofile.id
    return 0


class BaseModel(ModelOnDeleteMixin, models.Model):
    class Meta:
        abstract = True

    class ForeignKeyConstraint:
        fields = {
            'create_user_id': {"to_model": "user.UserProfile"},
        }

    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    create_user_id = models.BigIntegerField(verbose_name='创建人 ID', default=get_create_user_id)

    def delete(self):
        self.on_delete()
        self.save()


class BaseRegisterModel(ModelOnDeleteMixin, models.Model):
    class Meta:
        abstract = True

    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    def delete(self):
        self.on_delete()
        self.save()
