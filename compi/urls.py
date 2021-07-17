# from django.urls import path
# from . import views

# urlpattern = [
#     path('', views.home, name="web-home")
# ]

from django.urls import path, re_path
from .views import *


urlpatterns = [
    path('competition/', home, name='compi-home'),
    path('scoresheet_main/', scoresheet_main, name='compi-scoresheet-main'),
    path('scoresheet_list/<int:id>', scoresheet_list, name='compi-scoresheet-list'),
    path('scoresheet/<int:entry_id>',  scoresheet, name='compi-scoresheet'),
    path('register-contender/', register_contender, name='compi-register-contender'),
    path('register-judge/', register_judge, name='compi-register-judge'),
    path('entry-form/', entry_form, name='compi-entry-form'),
    path('result/<int:id>', competition_result, name='compi-result')
]