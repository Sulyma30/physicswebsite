import re

from rest_framework import serializers
from .models import Theme, Literature, Problem, TaskSet

class ThemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Theme
        fields = ['id', 'full_title', 'title', 'order']

class TaskSetSerializer(serializers.ModelSerializer):
    tasks = serializers.StringRelatedField(many=True)

    class Meta:
        model = TaskSet
        fields = ['literature', 'difficulty', 'tasks']
