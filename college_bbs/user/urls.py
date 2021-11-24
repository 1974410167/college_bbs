from django.conf.urls import url

from user.views.login import UserLogin
from user.views.register import UserRegister

urlpatterns = [
    # Auth
    url(r'register/', UserRegister.as_view(), name='register'),
    url(r'login/', UserLogin.as_view(), name='login'),
]
