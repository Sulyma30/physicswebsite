from rest_framework import serializers
from .models import Olympiad, OlympEvent, OlympFile

class OlympiadFileSerializer(serializers.ModelSerializer):
    tour = serializers.CharField(source='get_tour_display')
    class Meta:
        model = OlympFile
        fields = ['tour', 'grade', 'problems', 'solutions']

class OlympiadEventSerializer(serializers.ModelSerializer):
    files = serializers.SerializerMethodField()
    location = serializers.StringRelatedField()
    class Meta:
        model = OlympEvent
        fields = ['year','location', 'files']
    
    def get_files(self, instance):
        file_set = instance.files.all().order_by('-tour', '-grade')
        return OlympiadFileSerializer(file_set, many=True).data