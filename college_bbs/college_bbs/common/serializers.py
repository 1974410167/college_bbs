from rest_framework import serializers


class BaseModelSerializer(serializers.ModelSerializer):
    class Meta:
        read_only_fields = ('create_time', 'update_time', 'create_user_id')
