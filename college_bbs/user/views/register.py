from django.contrib.auth.models import User
from django.db import transaction
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from user.models import UserProfile
from user.serializers.register_ser import UserRegisterSerializers


class UserRegister(APIView):
    authentication_classes = ()
    permission_classes = ()

    def post(self, request):
        """
        注册
        """
        ser = UserRegisterSerializers(data=request.data)
        ser.is_valid(raise_exception=True)
        data = ser.validated_data
        with transaction.atomic():

            user = User.objects.create(**{"username": data.get("email") or data.get("phone"),
                                          "password": data.get("password")})
            data["user"] = user
            UserProfile.objects.create(**data)
        return Response({"mes": "注册成功"}, status=status.HTTP_201_CREATED)
