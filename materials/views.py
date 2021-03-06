import json
from django.shortcuts import get_object_or_404, render
from django.utils.safestring import SafeString

from .models import Supersection, Section, Theme, Literature, Requirement, Theory, Problem, TaskSet
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import TaskSetSerializer, SectionListSerializer, LiteratureSerializer

# Create your views here.

def material_page(request, theme_id, task_type = "problems"):
    theme = get_object_or_404(Theme, pk=theme_id)
    try:
        next_theme = Theme.objects.get(order=theme.order + 1)
    except Theme.DoesNotExist:
        next_theme = None
    try:
        previous_theme = Theme.objects.get(order=theme.order - 1)
    except Theme.DoesNotExist:
        previous_theme = None
    return render(request, "materials/material.html", { "task_type" : task_type , "theme" : theme, "next_theme" : next_theme, "previous_theme" : previous_theme})

@api_view(['GET'])
def material(request, theme_id, task_type='problems'):
    theme = get_object_or_404(Theme, pk=theme_id)
    taskSets = TaskSet.objects.filter(theme=theme, literature__literature_type=task_type)
    serializer = TaskSetSerializer(taskSets, many=True)
    return Response(serializer.data)

def literature_page(request, literature_type='theory'):
    return render(request, "materials/literature.html", { "type" : literature_type })

@api_view(['GET'])
def literature(request, literature_type='theory'):
    print('ok')
    literature = Literature.objects.filter(literature_type=literature_type)
    serializer = LiteratureSerializer(literature, many=True)
    return Response(serializer.data)
    
def materials_page(request, selected_type='', selected_title=''):
    return render(request, "materials/materials.html", {'selected_type' : selected_type, 'selected_title' : selected_title})

@api_view(['GET'])
def materials(request):
    sections = Section.objects.all()
    serializer = SectionListSerializer(sections, many=True)
    return Response(serializer.data)