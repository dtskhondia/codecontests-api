from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^contests/$', views.ContestList.as_view()),
]