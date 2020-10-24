from rest_framework import serializers
from .models import Olympiad, OlympEvent, OlympFile

class OlympiadFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = OlympFile
        fields = ['tour', 'grade', 'solutions']
        order = ['-grade']

class OlympiadEventSerializer(serializers.ModelSerializer):
    files = OlympiadFileSerializer(many=True)
    class Meta:
        model = OlympEvent
        fields = ['year','location', 'files']