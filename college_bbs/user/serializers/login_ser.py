from rest_framework import serializers
from user.models import UserProfile


class UserLoginSerializers(serializers.Serializer):
    email = serializers.EmailField(help_text="邮箱", required=False)
    phone = serializers.CharField(help_text="手机号", required=False)
    password = serializers.CharField(help_text="密码")

    def validate_email(self, value):
        if value:
            if not UserProfile.objects.filter(email=value).exists():
                raise serializers.ValidationError("")
            return value

    def validate_phone(self, value):
        if UserProfile.objects.filter(phone=value).exists():
            raise serializers.ValidationError("手机号已被注册")
        return value

    def validate_password(self, value):
        if value and len(value) < 6:
            raise serializers.ValidationError("密码长度大于等于6")
        return value

