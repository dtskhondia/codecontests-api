from rest_framework import generics
from .models import Contest
from .serializers import ContestSerializer
from . import services


class ContestList(generics.ListAPIView):
    """This is view for Contests."""
    services.load_contests()
    serializer_class = ContestSerializer
    queryset = Contest.objects.all().order_by('startTime', 'endTime')
