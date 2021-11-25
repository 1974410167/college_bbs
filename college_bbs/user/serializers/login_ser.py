from django.db.models import Q
from rest_framework import serializers
from user.models import UserProfile
from django.contrib.auth.hashers import check_password


class UserLoginSerializers(serializers.Serializer):
    email = serializers.EmailField(help_text="邮箱", required=False)
    phone = serializers.CharField(help_text="手机号", required=False)
    password = serializers.CharField(help_text="密码")
    login_field = {"email": None}

    def validate_email(self, value):
        if value:
            self.login_field["email"] = value
            if not UserProfile.objects.filter(email=value).exists():
                raise serializers.ValidationError("邮箱不存在")
        return value

    def validate_phone(self, value):
        if value:
            self.login_field["phone"] = value
            if not UserProfile.objects.filter(phone=value).exists():
                raise serializers.ValidationError("手机号不存在")
        return value

    def validate_password(self, value):
        if value and len(value) < 6:
            raise serializers.ValidationError("密码长度大于等于6")
        obj = UserProfile.objects.filter(**self.login_field).first()
        if obj:
            password = obj.password
            if not check_password(value, password):
                raise serializers.ValidationError("密码错误")
            return password
        raise serializers.ValidationError("邮箱或手机号不存在")
