"""Serializers"""
from rest_framework import serializers
from .models import Contest

class ContestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contest
        fields = ('id', 'name', 'startTime', 'endTime', 'site', 'url')
    