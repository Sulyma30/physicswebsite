from rest_framework import serializers
from .models import Theme, Literature, Problem, TaskSet, Section, Supersection

import re

class LiteratureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Literature
        fields = ['id', 'title', 'short_title', 'year', 'pdf', 'djvu']

class ThemeSerializer(serializers.ModelSerializer):
    requirements = serializers.StringRelatedField(many=True)
    class Meta:
        model = Theme
        fields = ['id', 'full_title', 'title', 'order', 'requirements']

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
    problem_tasks = serializers.StringRelatedField(many=True)
    theory_tasks = serializers.StringRelatedField(many=True)
    literature = LiteratureSerializer()

    class Meta:
        model = TaskSet
        fields = ['literature', 'difficulty', 'problem_tasks', 'theory_tasks']
    
    

    