from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from user.serializers.login_ser import UserLoginSerializers


class UserLogin(APIView):
    authentication_classes = ()
    permission_classes = ()

    def post(self, request):
        """

        """
        ser = UserLoginSerializers(data=request.data)
        ser.is_valid(raise_exception=True)
        data = ser.validated_data
        print(data)
        return Response({"mes": "注册成功"}, status=status.HTTP_201_CREATED)
