from django.db import models

# Create your models here.
from college_bbs.common.models.deletion import ModelOnDeleteMixin


class BaseModel(ModelOnDeleteMixin, models.Model):
    class Meta:
        abstract = True

    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    create_user_id = models.BigIntegerField(verbose_name='创建人 ID', default=0)

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
