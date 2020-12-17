from rest_framework import serializers
from .models import Theme, Literature, Problem,Theory, TaskSet, Section, Supersection
from .problems import problems_list_zip

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
    tasks = serializers.SerializerMethodField()
    literature = LiteratureSerializer()

    class Meta:
        model = TaskSet
        fields = ['id', 'literature', 'difficulty', 'tasks']
    
    def get_tasks(self, instance):
        if instance.literature.literature_type == 'problems':
            problem_set = Problem.objects.filter(task_set=instance.id).values_list('number', flat=True)
            return problems_list_zip(problem_set)
        elif instance.literature.literature_type == 'theory':
            elements = Theory.objects.filter(task_set=instance.id)
            theory = []
            for element in elements:
                theory += [f"{element.start_page}-{element.end_page}"]
            return theory

    
