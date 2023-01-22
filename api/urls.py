from django.urls import re_path
from . import views

urlpatterns = [
    re_path(r'^contests/$', views.ContestList.as_view()),
]
