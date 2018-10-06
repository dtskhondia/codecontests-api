from .models import Contest
from rest_framework import serializers

class ContestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contest
        fields = ('name','startTime','endTime','site')
    