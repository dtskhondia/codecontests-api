from rest_framework import generics
from .models import Contest
from .serializers import ContestSerializer
from . import services

class ContestList(generics.ListAPIView):
    """This is view for Contests."""
    services.load_contests()
    queryset = Contest.objects.all().order_by('startTime', 'endTime')
    serializer_class = ContestSerializer
    