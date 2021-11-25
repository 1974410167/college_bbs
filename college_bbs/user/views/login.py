from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from user.models import UserProfile
from user.models.api_token import ApiToken, get_token_expires
from user.serializers.login_ser import UserLoginSerializers


class UserLogin(APIView):
    authentication_classes = ()
    permission_classes = ()

    def post(self, request):
        """
        登录
        """
        ser = UserLoginSerializers(data=request.data)
        ser.is_valid(raise_exception=True)
        data = ser.validated_data
        user_objs = UserProfile.objects.filter(**data).first()
        token, _ = ApiToken.objects.get_or_create(user=user_objs.user)
        if token.is_expired():
            token.delete()
            token, _ = ApiToken.objects.get_or_create(user=user_objs.user)
        token.set_max_age(days=30)
        token.save()
        data = {
            'token': token.key,
            'expires': get_token_expires(token),
        }
        return Response(data, status=status.HTTP_201_CREATED)
