from rest_framework import serializers
from .models import Olympiad, OlympEvent, OlympFile

class OlympiadFileSerializer(serializers.ModelSerializer):
    tour = serializers.SerializerMethodField()
    class Meta:
        model = OlympFile
        fields = ['tour', 'grade', 'problems', 'solutions']
    
    def get_tour(self, instance):
        return instance.get_tour_display()

class OlympiadEventSerializer(serializers.ModelSerializer):
    files = serializers.SerializerMethodField()
    location = serializers.SerializerMethodField()
    class Meta:
        model = OlympEvent
        fields = ['year','location', 'files']
    
    def get_files(self, instance):
        file_set = instance.files.all().order_by('-tour', '-grade')
        return OlympiadFileSerializer(file_set, many=True).data
    
    def get_location(self, instance):
        return instance.get_location_display()