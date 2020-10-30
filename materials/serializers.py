from rest_framework import serializers
from .models import Theme, Literature, Problem, TaskSet, Section

class ThemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Theme
        fields = ['id', 'full_title', 'title', 'order']

class SectionListSerializer(serializers.ModelSerializer):
    themes = serializers.SerializerMethodField()
    supersection = serializers.StringRelatedField()

    class Meta:
        model = Section
        fields = ['title', 'supersection', 'themes']
    
    def get_themes(self, instance):
        theme_set = instance.themes.all().order_by('order')
        return ThemeSerializer(theme_set, many=True).data

class TaskSetSerializer(serializers.ModelSerializer):
    tasks = serializers.StringRelatedField(many=True)

    class Meta:
        model = TaskSet
        fields = ['literature', 'difficulty', 'tasks']
