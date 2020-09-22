import json
from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse
from django.urls import reverse
from django.db import IntegrityError
from django.utils.safestring import SafeString

from .models import Supersection, Section, Theme, Literature, Requirement, Theory, Problem, Olympiad, OlympEvent, OlympFile
from django.db.models import Max
from django.core.files.storage import FileSystemStorage

# Create your views here.
def index(request):
    return render(request, 'upho/index.html')

def materials(request):
    # Query for requested requirements, themes, sections and supersections
    requirements = Requirement.objects.all()
    themes = Theme.objects.all()
    sections = Section.objects.all()
    supersections = Supersection.objects.all()

    # All disabled materials that are without any content yet
    disabled_materials = [ material.title for material in Supersection.objects.all() if (Theory.objects.filter(theme__section__supersection=material).exists() or Problem.objects.filter(theme__section__supersection=material).exists() )==False ] + [ material.title for material in Section.objects.all() if (Theory.objects.filter(theme__section=material).exists() or Problem.objects.filter(theme__section=material).exists() )==False ] + [ material.title for material in Theme.objects.all() if (Theory.objects.filter(theme=material).exists() or Problem.objects.filter(theme=material).exists() )==False ]

    return render(request, 'upho/materials.html', { "requirements" : requirements, "themes" : themes, "themes_list" : SafeString({ section.title : [element.serialize() for element in themes.filter(section=section)] for section in sections}), "sections_list" : SafeString({supersection.title : [element.serialize() for element in sections.filter(supersection=supersection)] for supersection in supersections}), "supersections_list" : SafeString([element.serialize() for element in supersections]),"disabled_materials" : SafeString(disabled_materials)})

def material(request, theme_id, task = "problems"):
    # Query for requested theme
    theme = get_object_or_404(Theme, pk=theme_id)

    #Query for requested material. ADD EXCEPT!!!!???
    if (task == "theory"):
        material = {
            'chosen' : {
            "novice" : [{"literature" : literature.serialize(), "tasks" : ', '.join([ f"{task.start_page}-{task.end_page}" for task in Theory.objects.filter(theme__id=theme_id, difficulty=0, literature=literature) ])} for literature in Literature.objects.filter(theory__theme__id = theme_id, theory__difficulty = 0).distinct()],
            "advanced" : [{"literature" : literature.serialize(), "tasks" : ', '.join([ f"{task.start_page}-{task.end_page}" for task in Theory.objects.filter(theme__id=theme_id, difficulty=1, literature=literature) ])} for literature in Literature.objects.filter(theory__theme__id = theme_id, theory__difficulty = 1).distinct()],
            "expert" : [{"literature" : literature.serialize(), "tasks" : ', '.join([ f"{task.start_page}-{task.end_page}" for task in Theory.objects.filter(theme__id=theme_id, difficulty=2, literature=literature) ])} for literature in Literature.objects.filter(theory__theme__id = theme_id, theory__difficulty = 2).distinct()]
            }, "all" : []
        }
    elif (task == "problems"):
         material = {
            'chosen' : {
            "novice" : [{"literature" : literature.serialize(), "tasks" : ', '.join([ f"{task.number}" for task in Problem.objects.filter(theme__id=theme_id, difficulty=0, literature=literature) ])} for literature in Literature.objects.filter(problem__theme__id = theme_id, problem__difficulty = 0).distinct()],
            "advanced" : [{"literature" : literature.serialize(), "tasks" : ', '.join([ f"{task.number}" for task in Problem.objects.filter(theme__id=theme_id, difficulty=1, literature=literature) ])} for literature in Literature.objects.filter(problem__theme__id = theme_id, problem__difficulty = 1).distinct()],
            "expert" : [{"literature" : literature.serialize(), "tasks" : ', '.join([ f"{task.number}" for task in Problem.objects.filter(theme__id=theme_id, difficulty=2, literature=literature) ])} for literature in Literature.objects.filter(problem__theme__id = theme_id, problem__difficulty = 2).distinct()]
            }, "all" : [{"literature" : literature.serialize(), "tasks" : ', '.join([ f"{task.number}" for task in Problem.objects.filter(theme__id=theme_id, difficulty=None, literature=literature) ])} for literature in Literature.objects.filter(problem__theme__id = theme_id, problem__difficulty = None).distinct()]
        }
        
    # Return theme contents
    return render(request, "upho/material.html", { "task" : task , "material" : SafeString(material), "theme" : theme, "previous" :  None if theme.order <= 1 else Theme.objects.get(order=theme.order - 1), "next" : None if theme.order == max([element.order for element in Theme.objects.all()]) else Theme.objects.get(order=theme.order + 1) })   



def olympiads(request, olymp_type='national', static_location=''):
    olympiad = Olympiad.objects.get(olymp_type=olymp_type)

    # Default static location for regional
    if (olymp_type == 'regional' and static_location == ''):
        static_location = 'KYIV'

    # All options for olympiad (each has at least one corresponding olympiad file)
    years = {tour : list(OlympEvent.objects.filter(olympiad=olympiad, olympfile__tour=tour, location__contains=static_location).order_by('-year').values_list('year', flat=True).distinct()) for tour in list(OlympFile.objects.filter(event__olympiad=olympiad, event__location__contains=static_location).values_list('tour', flat=True).distinct())}
    grades = {tour : list(OlympFile.objects.filter(event__olympiad=olympiad, event__location__contains=static_location, tour=tour).order_by('-grade').values_list('grade', flat=True).distinct()) for tour in list(OlympFile.objects.filter(event__olympiad=olympiad, event__location__contains=static_location).values_list('tour', flat=True).distinct())}
    tours = [{ "tour" : tour, "readable" : dict(OlympFile.TOUR_CHOICES)[tour] } for tour in list(OlympFile.objects.filter(event__olympiad=olympiad).values_list('tour', flat=True).distinct()) ]
    locations = { year : dict(OlympEvent.LOCATION_CHOICES)[OlympEvent.objects.get(olympiad=olympiad, year=year).location] for year in list(OlympEvent.objects.filter(olympiad=olympiad, location__contains=static_location).values_list('year', flat=True).distinct()) }
    olymp_options = {"years" : years, "grades" : grades, "tours" : tours, "locations" : locations}

    # Information about all files in structured way
    olymp_files ={ olymp_files :  {tour : {f"{grade}" : list(OlympEvent.objects.filter(olympiad=olympiad, location__contains=static_location, olympfile__tour=tour, olympfile__grade=grade, olympfile__solutions=False if olymp_files=='problems' else True).values_list('year', flat=True).distinct()) for grade in list(OlympFile.objects.filter(event__olympiad=olympiad, event__location__contains=static_location, tour=tour).values_list('grade', flat=True).distinct()) } for tour in list(OlympFile.objects.filter(event__olympiad=olympiad, event__location__contains=static_location).values_list('tour', flat=True).distinct()) } for olymp_files in ['problems', 'solutions'] }

    # Info about olympiad
    olymp_info = { "olymp_type" : olymp_type, "olymp_name" : Olympiad.objects.get(olymp_type=olymp_type).name , "static_location" : { "name" : static_location.lower(), "readable" : "" if static_location=="" else dict(OlympEvent.LOCATION_CHOICES)[static_location.upper()] } }
    
    # List of regional locations (each has at least one corresponding olympiad file)
    regional_locations = [{ "name" : location, "readable" : dict(OlympEvent.LOCATION_CHOICES)[location] } for location in list(OlympEvent.objects.filter(olympiad__olymp_type="regional").values_list('location', flat=True).distinct()) ]

    context = {"olymp_info" : olymp_info, "olymp_options" : SafeString(olymp_options) , "olymp_files" : SafeString(olymp_files), "regional_locations" : SafeString(regional_locations)}
    return render(request, f"upho/olympiad.html", context)

def literature(request, literature_type='theory'):
    return render(request, "upho/literature.html", { "type" : literature_type, "literature" : SafeString([ element.serialize() for element in Literature.objects.filter(literature_type=literature_type) ]),"supersections_list" : SafeString([element.serialize() for element in Supersection.objects.all()]) })


# To do
def ipho(request):
    return render(request, "upho/ipho.html")
