from django.conf import settings
from django.db import models
from django.contrib.auth.hashers import make_password

from college_bbs.common.models import BaseRegisterModel


class UserProfile(BaseRegisterModel):

    class Meta(BaseRegisterModel.Meta):
        db_table = 'user_userprofile'
        verbose_name = "用户信息管理"
        verbose_name_plural = "用户信息管理"

    user = models.OneToOneField(settings.AUTH_USER_MODEL, verbose_name="账号", on_delete=models.CASCADE)
    name = models.CharField(verbose_name="姓名", max_length=100, help_text="姓名", null=True)
    email = models.CharField(verbose_name="邮箱", max_length=100, help_text="邮箱", null=True)
    phone = models.CharField(verbose_name="手机号", max_length=11, help_text="手机号", null=True)
    password = models.CharField(verbose_name="密码", max_length=255, help_text="密码", null=True)
    circle_url = models.TextField(verbose_name="头像", null=True)

    def save(self, *args, **kwargs):
        self.password = make_password(password=self.password)
        return super(UserProfile, self).save(*args, **kwargs)
