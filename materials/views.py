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
    return render(request, "materials/material.html", { "task_type" : task_type , "theme" : theme})

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
    
def materials_page(request):
    return render(request, "materials/materials.html")

@api_view(['GET'])
def materials(request):
    sections = Section.objects.all()
    serializer = SectionListSerializer(sections, many=True)
    return Response(serializer.data)