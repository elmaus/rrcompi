# from django.urls import path
# from . import views

# urlpattern = [
#     path('', views.home, name="web-home")
# ]

from django.urls import path, re_path
from .views import *


urlpatterns = [
    path('', home, name="web-home"),
    path('login/', web_login, name='web-login'),
    path('logout/', web_logout, name='web-logout'),
    path('login-redirect/',  login_redirect, name='web-login-redirect')
]