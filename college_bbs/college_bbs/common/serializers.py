from rest_framework import serializers
from college_bbs.common.redis_conn import CONN
from user.authentication import _auth_ctx


class BaseModelSerializer(serializers.ModelSerializer):
    class Meta:
        read_only_fields = ('create_time', 'update_time', 'create_user_id')


def get_redis_bitmap_key(id: int, prefix: str):
    return prefix + str(id)


class AgreeBaseSerializer(BaseModelSerializer):
    is_agree = serializers.SerializerMethodField()

    def get_is_agree(self, obj):
        redis_bit_key = get_redis_bitmap_key(obj.id, self.redis_bitmap_agree_prefix)
        user_id = _auth_ctx.user.userprofile.id
        is_agree = CONN.getbit(redis_bit_key, user_id)
        return is_agree


class BadAndAgreeBaseSerializer(AgreeBaseSerializer):
    is_bad = serializers.SerializerMethodField()

    def get_is_bad(self, obj):
        redis_bit_key = get_redis_bitmap_key(obj.id, self.redis_bitmap_bad_prefix)
        user_id = _auth_ctx.user.userprofile.id
        is_bad = CONN.getbit(redis_bit_key, user_id)
        return is_bad
