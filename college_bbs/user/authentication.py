# -*- coding: utf-8 -*-

import threading
from rest_framework.authentication import TokenAuthentication


_auth_ctx = threading.local()


class ExpiringTokenAuthentication(TokenAuthentication):
    def get_model(self):
        from user.models.api_token import ApiToken
        return ApiToken

    def _get_auth_token(self, key):
        user, token = super(ExpiringTokenAuthentication, self).authenticate_credentials(key)
        return user, token

    def authenticate_credentials(self, key):
        user, token = self._get_auth_token(key)

        setattr(_auth_ctx, 'user', user)
        setattr(user, 'name', user.userprofile.name)

        return user, token
