from rest_framework import generics
from rest_framework import mixins
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Contest
from .serializers import ContestSerializer
from . import services
import requests

class ContestList(generics.ListAPIView): 
    if 1==1:
        print(1)
    services.load_contests()
    queryset = Contest.objects.all().order_by('startTime','endTime')
    serializer_class = ContestSerializer
    