import json
from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse
from django.urls import reverse
from django.db import IntegrityError
from django.utils.safestring import SafeString

from .models import Supersection, Section, Theme, Literature, Requirement, Theory, Problem, TaskSet
from django.db.models import Max
from django.core.files.storage import FileSystemStorage
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from rest_framework import generics
from .serializers import TaskSetSerializer

# Create your views here.

def materials(request):
    # Query for requested requirements, themes, sections and supersections
    requirements = Requirement.objects.all()
    themes = Theme.objects.all()
    sections = Section.objects.all()
    supersections = Supersection.objects.all()

    # All disabled materials that are without any content yet
    disabled_materials = [ material.title for material in Supersection.objects.all() if (Theory.objects.filter(theme__section__supersection=material).exists() or Problem.objects.filter(theme__section__supersection=material).exists() )==False ] + [ material.title for material in Section.objects.all() if (Theory.objects.filter(theme__section=material).exists() or Problem.objects.filter(theme__section=material).exists() )==False ] + [ material.title for material in Theme.objects.all() if (Theory.objects.filter(theme=material).exists() or Problem.objects.filter(theme=material).exists() )==False ]

    return render(request, 'materials/materials.html', { "requirements" : requirements, "themes" : themes, "themes_list" : SafeString({ section.title : [element.serialize() for element in themes.filter(section=section)] for section in sections}), "sections_list" : SafeString({supersection.title : [element.serialize() for element in sections.filter(supersection=supersection)] for supersection in supersections}), "supersections_list" : SafeString([element.serialize() for element in supersections]),"disabled_materials" : SafeString(disabled_materials)})

def material_page(request, theme_id, task_type = "problems"):
    # Query for requested theme
    theme = get_object_or_404(Theme, pk=theme_id)

    return render(request, "materials/material.html", { "task_type" : task_type , "theme" : theme })

def literature(request, literature_type='theory'):
    return render(request, "materials/literature.html", { "type" : literature_type, "literature" : SafeString([ element.serialize() for element in Literature.objects.filter(literature_type=literature_type) ]),"supersections_list" : SafeString([element.serialize() for element in Supersection.objects.all()]) })

class TaskSetList(generics.ListAPIView):
    queryset = TaskSet.objects.all()
    serializer_class = TaskSetSerializer

    def get_queryset(self):
        theme_id = self.kwargs['theme_id']
        task_type = self.kwargs['task_type']
        return TaskSet.objects.filter(theme_id=theme_id, literature__literature_type=task_type)

# To do
def ipho(request):
    return render(request, "materials/ipho.html")